from f5.bigip import ManagementRoot
import sys
import logging
import json
import build_std_names
import getpass
import loadStdNames

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)


def check_poolname_conflict(mr, std_poolname):
    
    logging.info("Build_pools - check_poolname_conflict() Pool name: " + std_poolname)
    
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

def new_pool_build2(active_ltm, vs_dnsname, vs_port, vs_env, vs_poolmon, pool_membername, pool_memberip, pool_memberport, pool_membermon):
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logging.info("new_pool_build2()- Use Standard Global naming : " + useGlobalNaming )
        
    membernames = pool_membername.split(":")
    memberips = pool_memberip.split(":")
    memberports = pool_memberport.split(":")
    membermons = pool_membermon.split(":")
    
    idx = 1
    strReturn = {str(idx) : 'Pool Creation Report'}
    
    idx += 1

    if useGlobalNaming == '1':
        std_poolname = loadStdNames.get_std_name(active_ltm, 'LOCAL', 'POOL', '', vs_dnsname)
    else:
        #std_poolname = build_std_names.build_std_pool_name(str(vs_env), str(vs_dnsname), str(vs_port))
        std_poolname = str(vs_dnsname)
        
    logging.info("Pool Creation process has been initiated. Pool Name: " + std_poolname)
        
    if check_poolname_conflict(mr, std_poolname):
        strReturn.update({str(idx) : 'Pool Name conflict'})
        idx += 1
        return json.dumps(strReturn)
    logging.info("No Pool name conflict. Now creating a pool")
    #Create a pool
    try:
        mypool = mr.tm.ltm.pools.pool.create(name=std_poolname, partition='Common', loadBalancingMode='least-connections-member', monitor='/Common/'+vs_poolmon)
    except Exception as e:
        logging.info("Exception during Pool creation")
        strReturn[str(idx)] = "Exception fired!: " + str(e)
        idx += 1
        logging.info("Pool creation exception fired: " + str(e))
        return json.dumps(strReturn)
    
    try:
        mypool_1 = mr.tm.ltm.pools.pool.load(name=std_poolname, partition='Common')
    
        #for membername, memberip, memberport, membermon in map(None, membernames, memberips, memberports, membermons):
        for membername, memberip, memberport, membermon in zip(membernames, memberips, memberports, membermons):
            logging.info("Member Name: " + membername + " IP: " + memberip + " port: " + memberport + " mon: " + membermon)
            # Pool member creation issue - Calling Pool creation method too fast??
            if useGlobalNaming == '1':
                membername = loadStdNames.get_std_name(active_ltm, 'LOCAL', 'NODE', '', membername)
                    
            if (str(membermon) == 'inherit'):
                poolm = mypool_1.members_s.members.create(name=membername+':'+memberport, partition='Common', address=memberip, monitor=vs_poolmon )
                logging.info("inherit")
            else:
                poolm = mypool_1.members_s.members.create(name=membername+':'+memberport, partition='Common', address=memberip, monitor=membermon )
                logging.info("Standard TCP")
                
            logging.info("Member Name: " + membername + " IP: " + memberip + " Port: " + memberport + " Monitor: " + membermon + " Pool Monitor: " + vs_poolmon)
            strReturn[str(idx)] = 'Member(' + membername + ' IP:' + memberip + ':' + memberport + ' Monitor: ' + membermon + ') has been created'
            idx += 1
    except Exception as e:
        logging.info("Exception during Pool creation update")
        strReturn[str(idx)] = "Exception fired!: " + str(e)
        idx += 1
        logging.info("Pool creation update exception fired: " + str(e))
        return json.dumps(strReturn)
    
    strReturn[str(idx)] = "Pool creation(" + std_poolname + ") has been completed"
    idx += 1
    return json.dumps(strReturn)


if __name__ == "__main__":
    print new_pool_build2(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])
