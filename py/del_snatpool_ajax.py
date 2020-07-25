from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def del_snatpool_ajax(active_ltm, snatname, snatpart):
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    
    strReturn = []
    strReturn.append("Snatpool Deletion process has been initiated.")
    logger.info("Snatpool Deletion process has been initiated.")
    logger.info("snatname: " + snatname + " snat partition: " + snatpart)
    
    try:
        loaded_snatp = mr.tm.ltm.snatpools.snatpool.load(name=snatname, partition=snatpart)
        loaded_snatp.delete()
    except Exception as e:
        logger.info("Exception during deleting a Snatpool")
        logger.info(str(e))
        strReturn.append("FAIL")
        strReturn.append(str(e))
        return json.dumps(strReturn)
    
    strReturn.append("Snatpool deletion has been completed successfully.")
    logger.info("Snatpool deletion has been completed successfully.")
    return json.dumps(strReturn)


if __name__ == "__main__":
    print del_snatpool_ajax(sys.argv[1], sys.argv[2], sys.argv[3])
