from f5.bigip import ManagementRoot
import sys
import logging
import json
import build_std_names
import getpass
import loadStdNames

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


def check_poolname_conflict(mr, std_poolname):
    
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

def build_pools(active_ltm, vs_dnsname, vs_port, vs_env, vs_poolmon, pool_membername, pool_memberip, pool_memberport, pool_membermon):
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    
    membernames = json.loads(pool_membername)
    memberips = json.loads(pool_memberip)
    memberports = json.loads(pool_memberport)
    membermons = json.loads(pool_membermon)
    
    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logger.info("build_pools()- Use Standard Global naming : " + useGlobalNaming )
        
    idx = 1
    strReturn = {str(idx) : 'Pool Creation Report'}
    
    idx += 1

    if useGlobalNaming == '1':
        std_poolname = loadStdNames.get_std_name(active_ltm, 'LOCAL', 'POOL', '', vs_dnsname)
    else:
        #std_poolname = build_std_names.build_std_pool_name(str(vs_env), str(vs_dnsname), str(vs_port))
        std_poolname = str(vs_dnsname)

    logger.info("Pool Creation process has been initiated. Pool Name: " + std_poolname) 
    
    if check_poolname_conflict(mr, std_poolname):
        strReturn.update({str(idx) : 'Pool Name conflict'})
        idx += 1
        return json.dumps(strReturn)
    logger.info("No Pool name conflict. Now creating a pool")
    #Create a pool
    mypool = mr.tm.ltm.pools.pool.create(name=std_poolname, partition='Common', loadBalancingMode='least-connections-member', monitor='/Common/'+vs_poolmon)
    mypool_1 = mr.tm.ltm.pools.pool.load(name=std_poolname, partition='Common')
    
    #for membername, memberip, memberport, membermon in map(None, membernames, memberips, memberports, membermons):
    for membername, memberip, memberport, membermon in zip(membernames, memberips, memberports, membermons):
        logger.info("Member Name: " + membername + " IP: " + memberip + " port: " + memberport + " mon: " + membermon)
        # Pool member creation issue - Calling Pool creation method too fast??
        if useGlobalNaming == '1':
            membername = loadStdNames.get_std_name(active_ltm, 'LOCAL', 'NODE', '', membername)
                    
        if (str(membermon) == 'Inherit'):
            poolm = mypool_1.members_s.members.create(name=membername+':'+memberport, partition='Common', address=memberip, monitor=vs_poolmon )
            logger.info("Inherit")
        else:
            poolm = mypool_1.members_s.members.create(name=membername+':'+memberport, partition='Common', address=memberip, monitor=membermon )
            logger.info("Standard TCP")
            
        logger.info("Member Name: " + membername + " IP: " + memberip + " Port: " + memberport + " Monitor: " + membermon + " Pool Monitor: " + vs_poolmon)
        strReturn[str(idx)] = 'Member(' + membername + ' IP:' + memberip + ':' + memberport + ' Monitor: ' + membermon + ') has been created'
        idx += 1
    return json.dumps(strReturn)


if __name__ == "__main__":
    print build_pools(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])
