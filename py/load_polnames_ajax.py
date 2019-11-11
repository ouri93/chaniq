from f5.bigip import ManagementRoot
import sys
import logging
import json
import traceback

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
logging.info("Head of load_polnames_ajax() called")

def load_polnames_ajax(DevIp):
    #'DevIP' 'IrType' 'IrDgPart'
    logging.info("load_polnames_ajax.py parms\n DevIP: " + DevIp + "\n") 

    mr = ManagementRoot(str(DevIp), 'admin', 'rlatkdcks')
    
    key_idx = 1
    dictReturn = { key_idx: {'polType':'', 'name':'', 'partition':''}}

    logging.info("Loading Policy names has been initiated.") 

    #Retrieve cert/key configuration
    try:
        pollist = mr.tm.ltm.policys.get_collection()
        for apol in pollist:
            dictReturn[key_idx] = {'polType':apol.status,'name' : apol.name, 'partition' : apol.partition }
            key_idx =key_idx +1
    except Exception as e:
        logging.info("Policy Name get_collection Exception")
        logging.info("Error Details: " + str(e))
        logging.info(traceback.format_exc())
        dictReturn[key_idx] = {'polType':'FAIL', 'name' : "EXCEPTION", 'partition' : str(e) }
        return json.dumps(dictReturn)
            
    logging.info("Loading Policy names has been completed successfully")
    return json.dumps(dictReturn)

if __name__ == "__main__":
    print load_polnames_ajax(sys.argv[1])