from f5.bigip import ManagementRoot
import sys
import logging
import json
import build_std_names

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
logging.info("Head of new_pool_build() called")

def check_poolname_conflict(mr, std_poolname):
    
    logging.info("new_pool_build() - check_poolname_conflict() Pool name: " + std_poolname)
    
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

#def new_pool_build(active_ltm, vs_dnsname, vs_port, vs_env, vs_poolmon, pLBMethod):
def new_pool_build(active_ltm, vs_dnsname, vs_port, vs_env, vs_poolmon, pLBMethod, pPriGroup, pPriGroupLessThan, pool_membername, pool_memberip, pool_memberport, pmMon, pmPriGroup):
    
    logging.info("new_pool_build.py parms DevIP: " + active_ltm + " Pool Name: " + vs_dnsname + " VS Port: " + vs_port + " Env: " + vs_env + " Pool Mon: " + vs_poolmon + " LB Method: " + pLBMethod + " Pri Group: " + pPriGroup + " Lessthan: " + pPriGroupLessThan + " PM Names: " + pool_membername + " PM IPs: " + pool_memberip + " PM Ports: " + pool_memberport + " PM Mons:" + pmMon + " PM Pri:" + pmPriGroup) 
     
    mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    
    # Passed Parameter format change from string to array = "srv1.xyz.com:srv2.xyz.com:" ==> [srv1.xyz.com, srv2.xyz.com]
    membernames = pool_membername.split(":")
    memberips = pool_memberip.split(":")
    memberports = pool_memberport.split(":")
    membermons = pmMon.split(":")
    memberPriGroups = pmPriGroup.split(":")
    
    logging.info(" Pool Member1: " + membernames[0] + " Pool Member2: " + membernames[1]) 
    
    
    idx = 1
    strReturn = {str(idx) : 'Pool Creation Report'}
    
    idx += 1
 
    std_poolname = build_std_names.build_std_pool_name(str(vs_env), str(vs_dnsname), str(vs_port))
    logging.info("Pool Creation process has been initiated. Pool Name: " + std_poolname) 
    
    if check_poolname_conflict(mr, std_poolname):
        strReturn.update({str(idx) : 'Pool Name conflict'})
        idx += 1
        return json.dumps(strReturn)
    logging.info("No Pool name conflict. Now creating a pool")
    
    #Create a pool
    try:
        if pPriGroup != 'Lessthan':
            mypool = mr.tm.ltm.pools.pool.create(name=std_poolname, partition='Common', loadBalancingMode=pLBMethod, monitor='/Common/'+vs_poolmon)
        else:
            mypool = mr.tm.ltm.pools.pool.create(name=std_poolname, partition='Common', loadBalancingMode=pLBMethod, monitor='/Common/'+vs_poolmon, minActiveMembers=pPriGroupLessThan)
            
        mypool_1 = mr.tm.ltm.pools.pool.load(name=std_poolname, partition='Common')
    except Exception as e:
        logging.info("Exception during building base Pool creation")
        strReturn[str(idx)] = "Exception fired!: " + str(e)
        idx += 1
        logging.info("Base Pool Creation has failed with the excpetion of " + str(e))
        return json.dumps(strReturn)
    
    strReturn[str(idx)] = "Base Pool has been created (Without pool members and Priority Group)"
    idx += 1
        
    #for membername, memberip, memberport, membermon in map(None, membernames, memberips, memberports, membermons):
    try:
        count = 1
        if pPriGroup != 'Lessthan':
            for membername, memberip, memberport, membermon in zip(membernames, memberips, memberports, membermons):
                if (membername == ''):
                    break
                logging.info("Count: " + str(count) + " Member Name: " + membername + " IP: " + memberip + " port: " + memberport + " mon: " + membermon)
                # Pool member creation issue - Calling Pool creation method too fast??
                if (str(membermon) == 'Inherit'):
                    poolm = mypool_1.members_s.members.create(name=membername+':'+memberport, partition='Common', address=memberip, monitor=vs_poolmon )
                    logging.info("Inherit")
                else:
                    poolm = mypool_1.members_s.members.create(name=membername+':'+memberport, partition='Common', address=memberip, monitor=membermon )
                    logging.info("Custom Pool monitor")
                    
                logging.info("Count: " + str(count) + " Member Name: " + membername + " IP: " + memberip + " Port: " + memberport + " Monitor: " + membermon + " Pool Monitor: " + vs_poolmon)
                strReturn[str(idx)] = 'Member(' + membername + ' IP:' + memberip + ':' + memberport + ' Monitor: ' + membermon + ') has been updated with the built pool'
                idx += 1
                count = count + 1
        else:
            for membername, memberip, memberport, membermon, memberPriGroup in zip(membernames, memberips, memberports, membermons, memberPriGroups):
                if (membername == ''):
                    break            
                logging.info("Count: " + str(count) + " Member Name: " + membername + " IP: " + memberip + " port: " + memberport + " mon: " + membermon + " PoolMember Priority: " + memberPriGroup)
                # Pool member creation issue - Calling Pool creation method too fast??
                if (str(membermon) == 'Inherit'):
                    poolm = mypool_1.members_s.members.create(name=membername+':'+memberport, partition='Common', address=memberip, monitor=vs_poolmon, priorityGroup=memberPriGroup )
                    logging.info("Inherit")
                else:
                    poolm = mypool_1.members_s.members.create(name=membername+':'+memberport, partition='Common', address=memberip, monitor=membermon, priorityGroup=memberPriGroup )
                    logging.info("Custom Pool Monitor")
        
                logging.info("Count: " + str(count) + " Member Name: " + membername + " IP: " + memberip + " Port: " + memberport + " Monitor: " + membermon + " Pool Monitor: " + vs_poolmon)
                strReturn[str(idx)] = 'Member(' + membername + ' IP:' + memberip + ':' + memberport + ' Monitor: ' + membermon + ') has been updated with the built pool'
                idx += 1
                count = count + 1
    except Exception as e:
        logging.info("Exception occurred during updating base Pool with pool properties")
        strReturn[str(idx)] = "Exception fired!: " + str(e)
        idx += 1
        logging.info("Base Pool update has failed with the exception of " + str(e))
        return json.dumps(strReturn)
                    
    strReturn[str(idx)] = 'Pool creation process has been completed successfully'
    idx += 1
    logging.info("Final strReturn:  Started")            
    
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)
    
    
if __name__ == "__main__":
    print new_pool_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13])
