from f5.bigip import ManagementRoot
import sys
import logging
import json
import traceback

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
logging.info("Head of update_irdg_config() called")


def update_irdg_config(irDevIp, irDgName, irType, irCode, irDgType, irDgData):
    #'DevIP' 'IrDgName' 'IrType' 'IrCode' 'IrDgType' 'IrDgData'
    logging.info("update_irdg_config.py parms\n DevIP: " + irDevIp + "\niRule/Data Group Name: " + irDgName + "\nConfig Type: " + irType + "\niRule Code: " + irCode + "\nDG Type: " + irDgType + "\nDG Data: " + irDgData + "\n") 

    mr = ManagementRoot(str(irDevIp), 'admin', 'rlatkdcks')
    
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
                    logging.info("name: " + aRecord[0] + " Value: " + aRecord[1])
                    nr = [{'name':str(aRecord[0]), 'data':str(aRecord[1])}]
                else:
                    nr = [{'name':str(aRecord[0]), 'data':""}]
                new_records.extend(nr)
            # When updating Data Group, do not specify type.. it causes an error in some reason
            loaded_dg.update(name=irDgName, partition='Common', records=new_records)

    except Exception as e:
        logging.info("iRule/Data Group updating Exception")
        strReturn[str(idx)] = "iRule/Data Group updating Exception fired! (" + irDgName + "): " + str(e)
        idx += 1
        logging.info("Exception during iRule/Data Group Configuration update has been fired: " + str(e))
        logging.info(traceback.format_exc())
        return json.dumps(strReturn)
    
    strReturn[str(idx)] = irType + " iRule/Data Group (" + irDgName + ") configuration has been updated"
    idx += 1
    logging.info("iRule/Data Group configuration has been updated")
                    
    
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)

    return json.dumps(strReturn)

if __name__ == "__main__":
    print update_irdg_config(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
