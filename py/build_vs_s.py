from f5.bigip import ManagementRoot
import sys
import logging
import json
import build_std_names
import getpass
import loadStdNames

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


def check_vsname_conflict(mr, std_poolname):
    
    logger.info("Build_pools - check_poolname_conflict() Pool name: " + std_poolname)
    
    pools = mr.tm.ltm.pools.get_collection()

    bitout = 0
        
    for pool in pools:
        if pool.exists(name=std_poolname):
            bitout = bitout | (1 << 0)
    
    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False

def build_vs_s(active_ltm, vs_dnsname, vs_dest, vs_port, vs_desc, vs_env, vs_tcpprofile, vs_persistence, vs_redirect, vs_type, vs_httpprofile, vs_sslclient, vs_sslserver, vs_irule, vs_snatpool, vs_policy):
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logger.info("build_vs_s()- Use Standard Global naming : " + useGlobalNaming )
        
    idx = 1
    strReturn = {str(idx) : 'VS Creation Report'}
    
    idx += 1
    logger.info(str(active_ltm) + " " + str(vs_dnsname) + " " + str(vs_dest) + " " + str(vs_port) + " " + str(vs_desc) + " " + str(vs_env) + " " + str(vs_tcpprofile) + " " + str(vs_persistence) + " " + str(vs_redirect) + " " + str(vs_type) + " " + str(vs_httpprofile) + " " + str(vs_sslclient) + " " + str(vs_sslserver) )
    logger.info("Before VS Build - Env Name: " + str(vs_env) + " DNS name: " + str(vs_dnsname) + " Port: " + str(vs_port))
    
    if useGlobalNaming == '1':
        std_vsname = loadStdNames.get_std_name(active_ltm, 'LOCAL', 'VIRTUAL_SERVER', '', vs_dnsname)
        std_poolname = loadStdNames.get_std_name(active_ltm, 'LOCAL', 'POOL', '', vs_dnsname)
            
    #std_vsname = build_std_names.build_std_vs_name(str(vs_env), str(vs_dnsname), str(vs_port))
    #std_poolname = build_std_names.build_std_pool_name(str(vs_env), str(vs_dnsname), str(vs_port))
    std_vsname = str(vs_dnsname)
    std_poolname = str(vs_dnsname)
    
    logger.info("VS Creation process has been initiated. VS Name: " + std_vsname) 
    
    try:
        #Create a VS
        myvs = mr.tm.ltm.virtuals.virtual.create(name=std_vsname, partition='Common', destination='/Common/'+vs_dest+':'+vs_port, \
                ipProtocol='tcp', pool='/Common/' + std_poolname)
        logger.info("VS Name: " + std_vsname + " Destination: " + vs_dest + ':' + vs_port + " Pool Name: " + std_poolname)
        #Load additional profiles
        
        loadedvs = mr.tm.ltm.virtuals.virtual.load(name=std_vsname)
        loadedvs.profiles = ['/Common/' + vs_httpprofile, '/Common/' + vs_sslclient, '/Common/' + vs_sslserver]
        loadedvs.update()
        loadedvs.rules = ['/Common/' + vs_irule]
        loadedvs.update()
        loadedvs.persist = ['/Common/' + vs_persistence]
        loadedvs.update()
        loadedvs.policys = ['/Common/' + vs_policy]
        loadedvs.update()
        loadedvs.snatpools = ['/Common/' + vs_snatpool]
        loadedvs.update()
        
        strReturn[str(idx)] = 'VS Name: ' + std_vsname + ' (Destination: ' + vs_dest + ':' + vs_port + ' Pool Name: ' + std_poolname + ') has been created'
        idx += 1
    except Exception, e:
        logger.error(err)
    return json.dumps(strReturn)


if __name__ == "__main__":
    print build_vs_s(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14], sys.argv[15], sys.argv[16])
