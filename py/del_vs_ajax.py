from f5.bigip import ManagementRoot
from f5.bigip.contexts import TransactionContextManager
import sys
import logging
import json
import build_std_names
import getpass

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)


def check_vsname_conflict(mr, std_poolname):
    
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

def del_vs_ajax(active_ltm, vs_name, partition):
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    
    idx = 1
    strReturn = {str(idx) : 'VS Deletion Report'}
    idx += 1
    
    logging.info(str(active_ltm) + " VS Name:" + str(vs_name) + " Partition:" + partition )
    logging.info("Before VS Deletion - VS Name:" + str(vs_name) + " Partition:" + partition)
    
    logging.info("VS Deletion process has been initiated. VS Name: " + vs_name) 
    try:
        loaded_vs = mr.tm.ltm.virtuals.virtual.load(name=vs_name, partition=partition)
        loaded_vs.delete()
    except Exception as e:
        logging.info("Exception during Virtual Server deletion")
        strReturn[str(idx)] = "Exception fired!: " + str(e)
        idx += 1
        logging.info("Virtual Server deletion exception fired: " + str(e))
        return json.dumps(strReturn)

    strReturn[str(idx)] = "VS (" + vs_name + ") has been deleted successfully"
    idx += 1
    
    return json.dumps(strReturn)


if __name__ == "__main__":
    print del_vs_ajax(sys.argv[1], sys.argv[2], sys.argv[3])
