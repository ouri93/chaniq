from f5.bigip import ManagementRoot
import sys
import logging
import json
import build_std_names
import getpass


logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)


def get_pool_config(active_ltm, pName, pPartition):

    # Return Data Format
    # pool_name|pool_partition|pool_monitor|pool_LB|pool_lessthan@pm_name|pm_ip|pm_port|pm_ratio|pm_mon|pm_pri_group@pm_name|pm_ip|pm_port|pm_ratio|pm_mon|pm_pri_group...
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')

    output = ''

    idx = 1
    strReturn = {str(idx) : 'Pool Configuration Loading Report'}
   
    # Load pool configuration
    try:
        pLoaded = mr.tm.ltm.pools.pool.load(partition=pPartition, name=pName)
    except Exception as e:
        logging.info("Exception fired during loading Pool(" + pName + ") configuration")
        strReturn[str(idx)] = "Exception fired!: " + str(e)
        idx += 1
        logging.info("Loading Pool configuration exception fired: " + str(e))
        return json.dumps(strReturn)
    
    try:
        splitMon = (pLoaded.monitor).split('/')[2].strip()
    except Exception as e:
        logging.info("Pool monitor is not defined:" + str(e))
        splitMon = 'none'
    # In some reason, BIG-IP system adds a space at the end of pool monitor name. To remove spaces, use strip() method.
    # e.g. "/Common/https ", "/Common/tcp "
    output += pLoaded.name + '|' + pLoaded.partition + '|' + splitMon + '|' + pLoaded.loadBalancingMode + '|' + str(pLoaded.minActiveMembers) 
    
    # Load pool member configuration
    try:
        pList = mr.tm.ltm.pools.get_collection()
        for aPool in pList:
            if aPool.name == pName:
                for member in aPool.members_s.get_collection():
                    splitName = (member.name).split(':')
                    if member.monitor != 'default':
                        splitMon = (member.monitor).split('/')[2].strip()
                    else:
                        splitMon = 'default'
                    output += '@' + splitName[0] + "|" + member.address + "|" + splitName[1] + "|" + str(member.ratio) + "|" + splitMon + "|" + str(member.priorityGroup)
    except Exception as e:
        logging.info("Exception fired during loading Pool members configuration")
        strReturn[str(idx)] = "Exception fired!: " + str(e)
        idx += 1
        logging.info("Loading Pool members configuration exception fired: " + str(e))
        return json.dumps(strReturn)

    logging.info('get_pool_config.py => output in get_pool_config(): %s' % output)
    return output

if __name__ == "__main__":
    print get_pool_config(sys.argv[1], sys.argv[2], sys.argv[3])
