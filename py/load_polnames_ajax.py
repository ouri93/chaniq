from f5.bigip import ManagementRoot
import sys
import logging
import json
import traceback
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

logger.info("Head of load_polnames_ajax() called")

def load_polnames_ajax(active_ltm):
    #'DevIP' 'IrType' 'IrDgPart'
    logger.info("load_polnames_ajax.py parms\n DevIP: " + active_ltm + "\n") 

    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    
    key_idx = 1
    dictReturn = { key_idx: {'polType':'', 'name':'', 'partition':''}}

    logger.info("Loading Policy names has been initiated.") 

    #Retrieve cert/key configuration
    try:
        pollist = mr.tm.ltm.policys.get_collection()
        for apol in pollist:
            dictReturn[key_idx] = {'polType':apol.status,'name' : apol.name, 'partition' : apol.partition }
            key_idx =key_idx +1
    except Exception as e:
        logger.info("Policy Name get_collection Exception")
        logger.info("Error Details: " + str(e))
        logger.info(traceback.format_exc())
        dictReturn[key_idx] = {'polType':'FAIL', 'name' : "EXCEPTION", 'partition' : str(e) }
        return json.dumps(dictReturn)
            
    logger.info("Loading Policy names has been completed successfully")
    return json.dumps(dictReturn)

if __name__ == "__main__":
    print load_polnames_ajax(sys.argv[1])