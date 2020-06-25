from f5.bigip import ManagementRoot
import sys
import logging
import json
import traceback
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

logger.info("Head of del_pol_ajax() called")

def del_pol_ajax(active_ltm, polData, polType):
    logger.info("del_pol_ajax.py parms\n DevIP: " + active_ltm + "\nPolicy Status: " + polType + "\n") 

    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    
    key_idx = 1
    dictReturn = { key_idx: {'name':'', 'polType':'', 'result':'', 'message':''}}
    message = ''
    
    #logger.info("Before json_loads: " + polData + "\n")
    try:
        parsed_polData = json.loads(polData)
    except Exception as e:
        logger.info("Error Details: " + str(e))
    
    numOfRows = len(parsed_polData)
    
    for i in range(numOfRows):
        message =""
        message = message + "Policy deletion process has been started<br>"
        if i%2 == 0:
            polName = parsed_polData[i]
            polPart = parsed_polData[i+1]
            logger.info("Policy Name: " + polName + " Partition: " + polPart + "\n")
            ##### Delete given Policies ####
            try:
                if polType == 'draft':
                    loaded_pol = mr.tm.ltm.policys.policy.load(name=polName, partition=polPart, subPath='Drafts')
                    loaded_pol.delete()
                elif polType == 'published':
                    loaded_pol = mr.tm.ltm.policys.policy.load(name=polName, partition=polPart)
                    loaded_pol.delete()
            except Exception as e:
                logger.info("Error Details: " + str(e))
                message = message + str(e) + "<br>"
                logger.info("Exception during deleting policy. Name: " + polName + " Result: FAIL Message: " + message + "\n")
                if polType == 'draft':
                    dictReturn[key_idx] = {'name':polName, 'polType': 'draft', 'result':'FAIL', 'message':message}
                elif polType == 'published':
                    dictReturn[key_idx] = {'name':polName, 'polType': 'published','result':'FAIL', 'message':message}
                return json.dumps(dictReturn)
            message = message + "Policy has been deleted successfully<br>"
            logger.info("Deleting Policies have been completed successfully. Policy Name: " + polName + " Result: SUCCESS Message: " + message + "\n")
            if polType=='draft':
                dictReturn[key_idx] = {'name':polName, 'polType': 'draft', 'result':'SUCCESS', 'message':message}
            elif polType == 'published':
                dictReturn[key_idx] = {'name':polName, 'polType': 'published', 'result':'SUCCESS', 'message':message}
            key_idx = key_idx + 1

    return json.dumps(dictReturn)

if __name__ == "__main__":
    print del_pol_ajax(sys.argv[1], sys.argv[2], sys.argv[3])