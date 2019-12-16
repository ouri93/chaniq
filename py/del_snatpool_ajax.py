from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

def del_snatpool_ajax(active_ltm, snatname, snatpart):
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    
    strReturn = []
    strReturn.append("Snatpool Deletion process has been initiated.")
    logging.info("Snatpool Deletion process has been initiated.")
    logging.info("snatname: " + snatname + " snat partition: " + snatpart)
    
    try:
        loaded_snatp = mr.tm.ltm.snatpools.snatpool.load(name=snatname, partition=snatpart)
        loaded_snatp.delete()
    except Exception as e:
        logging.info("Exception during deleting a Snatpool")
        logging.info(str(e))
        strReturn.append("FAIL")
        strReturn.append(str(e))
        return json.dumps(strReturn)
    
    strReturn.append("Snatpool deletion has been completed successfully.")
    logging.info("Snatpool deletion has been completed successfully.")
    return json.dumps(strReturn)


if __name__ == "__main__":
    print del_snatpool_ajax(sys.argv[1], sys.argv[2], sys.argv[3])
