from f5.bigip import ManagementRoot
import sys
import logging
import json
import traceback
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


def update_irdg_config(active_ltm, irDgName, irType, irCode, irDgType, irDgData):
    #'DevIP' 'IrDgName' 'IrType' 'IrCode' 'IrDgType' 'IrDgData'
    logger.info("update_irdg_config.py parms\n DevIP: " + active_ltm + "\niRule/Data Group Name: " + irDgName + "\nConfig Type: " + irType + "\niRule Code: " + irCode + "\nDG Type: " + irDgType + "\nDG Data: " + irDgData + "\n") 

    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    
    idx = 1
    strReturn = {str(idx) : 'iRule/Data Group Configuration Update Report'}
    
    idx += 1
 
    #Update a iRule/Data Group configuration
    try:
        if irType == "iRule":
            loaded_ir = mr.tm.ltm.rules.rule.load(name=irDgName)
            loaded_ir.update(name=irDgName, partition='Common', apiAnonymous=irCode)
        elif irType == "Data Group":
            loaded_dg = mr.tm.ltm.data_group.internals.internal.load(name=irDgName)
            new_records = []
            arrRecords = irDgData.split(',');
            for arrRecord in arrRecords:
                aRecord = arrRecord.split(':=')
                if len(aRecord) == 2:
                    logger.info("name: " + aRecord[0] + " Value: " + aRecord[1])
                    nr = [{'name':str(aRecord[0]), 'data':str(aRecord[1])}]
                else:
                    nr = [{'name':str(aRecord[0]), 'data':""}]
                new_records.extend(nr)
            # When updating Data Group, do not specify type.. it causes an error in some reason
            loaded_dg.update(name=irDgName, partition='Common', records=new_records)

    except Exception as e:
        logger.info("iRule/Data Group updating Exception")
        strReturn[str(idx)] = "iRule/Data Group updating Exception fired! (" + irDgName + "): " + str(e)
        idx += 1
        logger.info("Exception during iRule/Data Group Configuration update has been fired: " + str(e))
        logger.info(traceback.format_exc())
        return json.dumps(strReturn)
    
    strReturn[str(idx)] = irType + " iRule/Data Group (" + irDgName + ") configuration has been updated"
    idx += 1
    logger.info("iRule/Data Group configuration has been updated")
                    
    
    for keys, values in strReturn.items():
        logger.info("Key: " + keys + " Value: " + values)

    return json.dumps(strReturn)

if __name__ == "__main__":
    print update_irdg_config(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
