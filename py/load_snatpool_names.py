from f5.bigip import ManagementRoot
import sys
import logging
import json

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

def load_snatpool_names(active_ltm):
    
    mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    
    strReturn = []
    
    logging.info("Snatpool Name loading process has been initiated.")
    
    try:
        snatp_list = mr.tm.ltm.snatpools.get_collection()
        for aSnat in snatp_list:
            strReturn.append(aSnat.name)
            strReturn.append(aSnat.partition)
    except Exception as e:
        logging.info("Exception during collecting Snatpool names")
        logging.info(str(e))
        strReturn.append("FAIL")
        strReturn.append(str(e))
        return json.dumps(strReturn)

    return json.dumps(strReturn)


if __name__ == "__main__":
    print load_snatpool_names(sys.argv[1])
