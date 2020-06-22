from f5.bigip import ManagementRoot
import logging
import sys
import json
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

# 'PhpFileName' 'DevIP' 'P_name' 'P_part' 'P_mon' 'P_LB' 'P_priGroup' 'P_lessthan' 'PM_names'
# 'PM_ips' 'PM_ports' 'PM_ratios' 'PM_mons' 'PM_priGroup'
def chg_pool_build(active_ltm, p_name, p_part, p_mon, p_LB, p_priGroup, p_priLessthan, pm_names, pm_ips, pm_ratios, pm_mons, pm_priGroups):
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    
    membernames = pm_names.split("|")
    memberips = pm_ips.split("|")
    memberratios = pm_ratios.split("|")
    membermons = pm_mons.split("|")
    memberprigrp = pm_priGroups.split("|")
    
    idx = 1
    strReturn = {str(idx) : 'Pool Configuration Modification Report'}
    idx += 1

    logger.info("Pool Configuration Modification process has been initiated. Pool Name: " + p_name)
    
    # Phase zero - Update pool properties
    try:
        p_loaded = mr.tm.ltm.pools.pool.load(partition=p_part, name=p_name)
        p_loaded.monitor = "/" + p_part + "/" + p_mon
        p_loaded.loadBalancingMode = p_LB
        if p_priGroup == 'Lessthan':
            p_loaded.minActiveMembers = p_priLessthan
        p_loaded.update()
    except Exception as e:
        logger.info("Exception during Pool configuration modification process")
        strReturn[str(idx)] = "Exception error: " + str(e)
        idx += 1
        logger.info("Pool configuration modification exception: " + str(e))
        return json.dumps(strReturn)

    logger.info("Pool configuration modification has been successfully completed.")
    strReturn[str(idx)] = "Pool configuration modification has been successfully completed."
    idx += 1
                
    # Phase one - Delete pool members if deleted from GUI
    strMemberNames = ','.join([str(x) for x in membernames])
    logger.info("Converted member names: " + strMemberNames)
    try:
        p_loaded = mr.tm.ltm.pools.pool.load(partition=p_part, name=p_name)
        for PMbrs in p_loaded.members_s.get_collection():
            #if membernames.find(PMbrs.name) != -1:
            logger.info("Pool member name from BIG-IP: " + PMbrs.name + "     Pool member name from Input: " + strMemberNames)
            if strMemberNames.find(PMbrs.name) < 0:
                logger.info("Not matching pool memebr name found: " + PMbrs.name)
                pm1 = p_loaded.members_s.members.load(partition=p_part, name=p_name)
                pm1.delete()
                logger.info("Pool member (" + p_name + ") has been successfully deleted")
    except Exception as e:
        logger.info("Exception during Pool member loading and deletion process")
        strReturn[str(idx)] = "Exception error: " + str(e)
        idx += 1
        logger.info("Pool member loading and deletion process exception: " + str(e))
        return json.dumps(strReturn)
    
    logger.info("Pool member deletion has been successfully completed.")
    strReturn[str(idx)] = "Pool member deletion has been successfully completed."
    idx += 1
    
    # Phase Two - Add new pool members or update existing pool members
    try:
        for i in range(len(membernames)-1):
            logger.info("Index: " + str(i) + "  Num of Pool members: " + str(len(membernames)-1) + "  First pool member name: " + membernames[i])
            # Update existing pool members
            if p_loaded.members_s.members.exists(partition=p_part, name=membernames[i]):
                pm1 = p_loaded.members_s.members.load(partition=p_part, name=membernames[i])
                logger.info("PM Ratio: " + str(pm1.ratio) + "  PM Mon: " + pm1.monitor + "  PM PriGroup: " + str(pm1.priorityGroup) + " ")
                pm1.ratio = int(memberratios[i])
                if membermons[i] == 'inherit':
                    pm1.monitor = 'default'
                else:
                    pm1.monitor = membermons[i]
                pm1.priorityGroup = int(memberprigrp[i])
                pm1.update()
            # Create new pool members
            else:
                if membermons[i] == 'inherit':
                    membermons[i] = 'default'
                p_loaded.members_s.members.create(name=membernames[i], partition=p_part, address=memberips[i], ratio=int(memberratios[i]), monitor=membermons[i], priorityGroup=int(memberprigrp[i]) )
    except Exception as e:
        logger.info("Exception during Pool member addition and modification process")
        strReturn[str(idx)] = "Exception error: " + str(e)
        idx += 1
        logger.info("Pool member addition and modification process exception: " + str(e))
        return json.dumps(strReturn)

    logger.info("Pool member addition and modification have been successfully completed.")    
    strReturn[str(idx)] = "Pool member addition and modification have been successfully completed."
    idx += 1    

    return json.dumps(strReturn)


if __name__ == "__main__":
    print chg_pool_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12])
