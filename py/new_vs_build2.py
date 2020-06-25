from f5.bigip import ManagementRoot
from f5.bigip.contexts import TransactionContextManager
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

def new_vs_build2(active_ltm, vs_dnsname, vs_dest, vs_port, vs_desc, vs_env, vs_tcpprofile, vs_persistence, vs_redirect, vs_type, vs_httpprofile, vs_sslclient, vs_sslserver, vs_irule, vs_snatpool, vs_policy, vs_poolname):
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logger.info("new_vs_build2()- Use Standard Global naming : " + useGlobalNaming )
        
    idx = 1
    strReturn = {str(idx) : 'VS Creation Report'}
    idx += 1
    
    logger.info(str(active_ltm) + " VS DNS:" + str(vs_dnsname) + " VS DEST:" + str(vs_dest) + " VS PORT:" + str(vs_port) + " VS DESC:" + str(vs_desc) + " VS Env.:" + str(vs_env) + " VS TCP Prf:" + str(vs_tcpprofile) + " VS Persist:" + str(vs_persistence) + " VS Redirect:" + str(vs_redirect) + " VS Type:" + str(vs_type) + " VS HTTP Prf:" + str(vs_httpprofile) + " VS Clientssl:" + str(vs_sslclient) + " VS Serverssl:" + str(vs_sslserver) + " VS iRule: " + str(vs_irule) + " VS SNATPOOL: " + str(vs_snatpool) + " VS Policy: " + str(vs_policy) + " VS Pool Name: " + str(vs_poolname) )
    logger.info("Before VS Build - Env Name: " + str(vs_env) + " DNS name: " + str(vs_dnsname) + " Port: " + str(vs_port))

    if useGlobalNaming == '1':
        std_vsname = loadStdNames.get_std_name(active_ltm, 'LOCAL', 'VIRTUAL_SERVER', '', vs_dnsname)
    else:
        std_vsname = str(vs_dnsname)
                
    #std_vsname = build_std_names.build_std_vs_name(str(vs_env), str(vs_dnsname), str(vs_port))
    #std_poolname = build_std_names.build_std_pool_name(str(vs_env), str(vs_dnsname), str(vs_port))
    
    logger.info("VS Creation process has been initiated. VS Name: " + std_vsname) 
    try:    
        fieldNames = {"name":std_vsname, "description":vs_desc, "ip":vs_dest, "port":vs_port, "ipProtocol":"tcp", "pool":vs_poolname, \
        "protocolProfileClient":vs_tcpprofile, "httpProfile":vs_httpprofile, "oneConnectProfile":"none", "sslProfileClient":vs_sslclient, \
        "sslProfileServer":vs_sslserver, "rules":vs_irule, "sourceAddressTranslation":vs_snatpool, "persistence":vs_persistence,  "policies":vs_policy}
        
        logger.info("Protocol Profile: " + fieldNames["protocolProfileClient"] + " HTTP Profie: " + fieldNames["httpProfile"] + \
                     " SSL Client Profile: " + fieldNames["sslProfileClient"] + " SSL Server Profile: " + fieldNames["sslProfileServer"] +   \
                     " iRule: " + fieldNames["rules"] +   " Persistence: " + fieldNames["persistence"] +   " Policy: " + fieldNames["policies"])  

        myvirtual = mr.tm.ltm.virtuals.virtual.create(name=fieldNames["name"], description=fieldNames["description"],  \
                    destination="%s:%s" % (fieldNames["ip"], fieldNames["port"]),  ipProtocol=fieldNames["ipProtocol"], \
                    pool=fieldNames["pool"])

        # Create the profiles. When a virtual server is created which has a TCP 
        # base protocol then it is automatically assigned the base "tcp" profile.
        # This profile cannot be removed without assigning some other TCP profile.
        # To do this you have to wrap the deletion of the "tcp" profile and the
        # creation of the of the other TCP profile in a transaction.
        tx = mr.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            profiles = myvirtual.profiles_s
            if fieldNames["protocolProfileClient"] != "none":
                p1 = profiles.profiles.load(partition="Common",name="tcp")
                p1.delete()
                myvirtual.profiles_s.profiles.create(partition="Common", name=fieldNames["protocolProfileClient"])

            if fieldNames["httpProfile"] != "none":
                myvirtual.profiles_s.profiles.create(partition="Common", name=fieldNames["httpProfile"])
    
            if fieldNames["oneConnectProfile"] != "none":
                myvirtual.profiles_s.profiles.create(partition="Common", name=fieldNames["oneConnectProfile"])
    
            if fieldNames["sslProfileClient"] != "none":
                myvirtual.profiles_s.profiles.create(partition="Common", name=fieldNames["sslProfileClient"])
    
            if fieldNames["sslProfileServer"] != "none":
                myvirtual.profiles_s.profiles.create(partition="Common", name=fieldNames["sslProfileServer"])

        strReturn[str(idx)] = 'Protocol/HTTP/OneConnect/Client and Server SSL Profile has been updated'
        idx += 1

        # Update the virtual server with the iRules. The iRules have to be a list.
        if fieldNames["rules"] != 'none':
            rules = []
            for rule in fieldNames["rules"].split():
                rules.append(rule)

            myvirtual.rules = rules
            myvirtual.update()

        # Update the virtual server with the Snatpool. The Snatpool have to be a dictionary.
        # When you add snatpool to a Virtual Server during Virtual Server creation, BIG-IP takes 'snatpool'.
        # However when you need to update snatpool with a specific virtual server, you should use 'sourceAddressTranslation' with dictionary format.
        if fieldNames["sourceAddressTranslation"] != 'none':
            vssnatpool = {'pool':'', 'type':'snat'}
            vssnatpool['pool'] = '/Common/' + fieldNames["sourceAddressTranslation"]
            
            myvirtual.sourceAddressTranslation = vssnatpool 
            myvirtual.update()

        # Update the virtual server with the persistence profile. The iRules 
        # have to be a list. But we will never have more than one.
        if fieldNames["persistence"] != 'none':
            persistence = []
            for persistenceProfile in fieldNames["persistence"].split():
                persistence.append(persistenceProfile)
    
            myvirtual.persist = persistence
            myvirtual.update()
    
        # Update the virtual server with the policy. 
        policies = myvirtual.policies_s
        if fieldNames["policies"] != 'none':
            myvirtual.policies_s.policies.create(partition="Common", name=fieldNames["policies"])
            
        strReturn[str(idx)] = 'iRule/Persistence/SnatPool/Policy Profile has been updated'
        idx += 1
        strReturn[str(idx)] = 'Requested Virtual Server (' + std_vsname + ')  has been succssfully created'
        idx += 1
        
    except Exception as e:
        logger.info("Exception during Virtual Server creation-update")
        strReturn[str(idx)] = "Exception fired!: " + str(e)
        idx += 1
        logger.info("Virtual Server creation-update exception fired: " + str(e))
        return json.dumps(strReturn)

    return json.dumps(strReturn)


if __name__ == "__main__":
    print new_vs_build2(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14], sys.argv[15], sys.argv[16], sys.argv[17])
