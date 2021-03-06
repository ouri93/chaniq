from f5.bigip import ManagementRoot
import sys
import logging
import json
import traceback
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

logger.info("Head of del_certkey_ajax() called")

def del_certkey_ajax(active_ltm, certData):
    #'DevIP' 'IrType' 'IrDgPart'
    logger.info("del_certkey_ajax.py parms\n DevIP: " + active_ltm + "\n") 

    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    
    key_idx = 1
    dictReturn = { key_idx: {'name':'', 'result':'', 'message':''}}
    message = ''
    
    #logger.info("Before json_loads: " + certData + "\n")
    try:
        parsed_certData = json.loads(certData)
    except Exception as e:
        logger.info("Error Details: " + str(e))
    
    numOfRows = len(parsed_certData)
    
    for i in range(numOfRows):
        message =""
        message = message + "Cert/key deletion process has been started<br>"
        if i%4 == 0:
            certKeyName = parsed_certData[i]
            certKeyPart = parsed_certData[i+3]
            certName = certKeyName + ".crt"
            keyName = certKeyName + ".key"
            logger.info("Cert/Key Name: " + certKeyName + "Partition: " + certKeyPart + "\n")
            ##### Delete given certs and keys ####
            try:
                loaded_cert = mr.tm.sys.crypto.certs.cert.load(name=certName, partition=certKeyPart)
                loaded_cert.delete()
                
                loaded_key = mr.tm.sys.crypto.keys.key.load(name=keyName, partition=certKeyPart)
                loaded_key.delete()
            except Exception as e:
                logger.info("Error Details: " + str(e))
                message = message + str(e) + "<br>"
                logger.info("Exception during loading or deleting cert/key Cert/Key Name: " + certKeyName + " Result: FAIL Message: " + message + "\n")
                dictReturn[key_idx] = {'name':certKeyName, 'result':'FAIL', 'message':message}
                return json.dumps(dictReturn)
            message = message + "Cert and Key have been deleted successfully<br>"
            logger.info("Deleting cert/key has been completed successfully. Cert/Key Name: " + certKeyName + " Result: SUCCESS Message: " + message + "\n")
            dictReturn[key_idx] = {'name':certKeyName, 'result':'SUCCESS', 'message':message}
            key_idx = key_idx + 1
    '''
    key_idx = 1
    dictReturn = { key_idx: {'name':'', 'result':'', 'message':''}}

    logger.info("Deleting Cert/Key process has been initiated.") 

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
        logger.info("Cert get_collection Exception")
        logger.info("Error Details: " + str(e))
        logger.info(traceback.format_exc())
        dictReturn[key_idx] = {'name' : "Exception fired", 'commonName' : "Exception fired", 'expiration' : "Exception fired", 'partition' : "Exception fired" }
        return json.dumps(dictReturn)
            
    logger.info("Cert information has been collected successfully")
    '''
    return json.dumps(dictReturn)

if __name__ == "__main__":
    print del_certkey_ajax(sys.argv[1], sys.argv[2])