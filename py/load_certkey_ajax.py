from f5.bigip import ManagementRoot
import sys
import logging
import json
import traceback
import getpass

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
logging.info("Head of load_certkey_ajax() called")

def load_certkey_ajax(active_ltm):
    #'DevIP' 'IrType' 'IrDgPart'
    logging.info("load_certkey_ajax.py parms\n DevIP: " + active_ltm + "\n") 

    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    
    key_idx = 1
    dictReturn = { key_idx: {'name':'', 'commonName':'', 'expiration':'', 'partition':''}}

    logging.info("Loading Cert/Key process has been initiated.") 

    #Retrieve cert/key configuration
    try:
        certs=mr.tm.sys.crypto.certs.get_collection()
        for acert in certs:
            nameAndPath = (acert.fullPath).split('/')
            certkeyName = nameAndPath[2]
            certkeyCN = acert.commonName
            certkeyExp = acert.apiRawValues['expiration']
            certkeyPart = nameAndPath[1]
            dictReturn[key_idx] = {'name' : certkeyName, 'commonName' : certkeyCN, 'expiration' : certkeyExp, 'partition' : certkeyPart }
            key_idx = key_idx + 1
    except Exception as e:
        logging.info("Cert get_collection Exception")
        logging.info("Error Details: " + str(e))
        logging.info(traceback.format_exc())
        dictReturn[key_idx] = {'name' : "Exception fired", 'commonName' : "Exception fired", 'expiration' : "Exception fired", 'partition' : "Exception fired" }
        return json.dumps(dictReturn)
            
    logging.info("Cert information has been collected successfully")
    return json.dumps(dictReturn)

if __name__ == "__main__":
    print load_certkey_ajax(sys.argv[1])