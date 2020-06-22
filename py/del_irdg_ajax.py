from f5.bigip import ManagementRoot
import sys
import logging
import json
import traceback
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

logger.info("Head of del_irdg_ajax() called")


def del_irdg_ajax(active_ltm, irDgName, irOrDg, dgType):
    #'DevIP' 'IrDgName' 'IrType' 'IrCode' 'IrDgType' 'IrDgData'
    logger.info("del_irdg_ajax.py parms\n DevIP: " + active_ltm + "\niRule/Data Group Name: " + irDgName + "\nConfig Type: " + irOrDg + "\nDG Type: " + dgType + "\n") 

    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    
    idx = 1
    strReturn = {str(idx) : 'iRule/Data Group Deletion Report'}
    
    idx += 1
 
    #Update a iRule/Data Group configuration
    try:
        if irOrDg == "iRule":
            loaded_ir = mr.tm.ltm.rules.rule.load(name=irDgName)
            loaded_ir.delete()
        elif irOrDg == "Data Group":
            loaded_dg = mr.tm.ltm.data_group.internals.internal.load(name=irDgName)
            loaded_dg.delete()
    except Exception as e:
        logger.info("iRule/Data Group Deletion Exception")
        strReturn[str(idx)] = "iRule/Data Group Deletion Exception fired! (" + irDgName + "): " + str(e)
        idx += 1
        logger.info("Exception during iRule/Data Group Deletion has been fired: " + str(e))
        logger.info(traceback.format_exc())
        return json.dumps(strReturn)
    
    strReturn[str(idx)] = irOrDg + " iRule/Data Group (" + irDgName + ") deletion has been completed successfully"
    idx += 1
    logger.info("iRule/Data Group deletion has been completed successfully")
                    
    
    for keys, values in strReturn.items():
        logger.info("Key: " + keys + " Value: " + values)

    return json.dumps(strReturn)

if __name__ == "__main__":
    print del_irdg_ajax(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
