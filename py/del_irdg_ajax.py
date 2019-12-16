from f5.bigip import ManagementRoot
import sys
import logging
import json
import traceback
import getpass

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
logging.info("Head of del_irdg_ajax() called")


def del_irdg_ajax(active_ltm, irDgName, irOrDg, dgType):
    #'DevIP' 'IrDgName' 'IrType' 'IrCode' 'IrDgType' 'IrDgData'
    logging.info("del_irdg_ajax.py parms\n DevIP: " + active_ltm + "\niRule/Data Group Name: " + irDgName + "\nConfig Type: " + irOrDg + "\nDG Type: " + dgType + "\n") 

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
        logging.info("iRule/Data Group Deletion Exception")
        strReturn[str(idx)] = "iRule/Data Group Deletion Exception fired! (" + irDgName + "): " + str(e)
        idx += 1
        logging.info("Exception during iRule/Data Group Deletion has been fired: " + str(e))
        logging.info(traceback.format_exc())
        return json.dumps(strReturn)
    
    strReturn[str(idx)] = irOrDg + " iRule/Data Group (" + irDgName + ") deletion has been completed successfully"
    idx += 1
    logging.info("iRule/Data Group deletion has been completed successfully")
                    
    
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)

    return json.dumps(strReturn)

if __name__ == "__main__":
    print del_irdg_ajax(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
