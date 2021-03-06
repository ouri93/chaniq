from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def load_snatpool_names(active_ltm):
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    
    strReturn = []
    
    logger.info("Snatpool Name loading process has been initiated.")
    
    try:
        snatp_list = mr.tm.ltm.snatpools.get_collection()
        for aSnat in snatp_list:
            strReturn.append(aSnat.name)
            strReturn.append(aSnat.partition)
    except Exception as e:
        logger.info("Exception during collecting Snatpool names")
        logger.info(str(e))
        strReturn.append("FAIL")
        strReturn.append(str(e))
        return json.dumps(strReturn)

    return json.dumps(strReturn)


if __name__ == "__main__":
    print load_snatpool_names(sys.argv[1])
