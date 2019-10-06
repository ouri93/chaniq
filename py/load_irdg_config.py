from f5.bigip import ManagementRoot
import sys
import logging
import json
import traceback

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
logging.info("Head of load_irdg_config() called")

def load_irdg_config(irDevIp, irType, irDgName):
    #'DevIP' 'IrType' 'IrDgPart'
    logging.info("load_irdg_config.py parms\n DevIP: " + irDevIp + "\niRule or Data Group: " + irType +  "\nName: " + irDgName + "\n") 

    mr = ManagementRoot(str(irDevIp), 'admin', 'rlatkdcks')
    
    dictReturn = {'name':''}

    logging.info("iRule/Data Group Modification process has been initiated.") 

    #Load a iRule/Data Group configuration
    try:
        if irType == "iRule":
            dictReturn["IrOrDg"] = irType
            ir_list = mr.tm.ltm.rules.get_collection()
            for aIR in ir_list:
                if aIR.name == irDgName:
                    dictReturn["name"] = aIR.name
                    dictReturn["apiAnonymous"] = aIR.apiAnonymous
        elif irType == "Data Group":
            dictReturn["IrOrDg"] = irType
            dg_list = mr.tm.ltm.data_group.internals.get_collection()
            for aDG in dg_list:
                if aDG.name == irDgName:
                    dictReturn["name"]= aDG.name
                    dictReturn["type"]= aDG.type
                    # 'records' value is a list with dictinary type value. e.g records = [{'data': 'HTTPS', 'name': 'HTTP'}, {'data': 'World', 'name': 'Hello'}]
                    dictReturn["records"]= aDG.records
    except Exception as e:
        logging.info("iRule/Data Group Exception - Retrieving iRule/Data Group configuration")
        logging.info("Error Details: " + str(e))
        logging.info(traceback.format_exc())
        return json.dumps(dictReturn)
    
    logging.info("Name retrieving for iRule/Data Group has been completed")
    return json.dumps(dictReturn)
'''
    if irType == "iRule":
        for keys,values in dictReturn.items():
            logging.info("Retrieved Key name: " + keys + "Retrieved Value: " + values)
     
    if irType == "Data Group":
        for keys,values in dictReturn.items():
            try:
                logging.info("Retrieved Key name: " + keys + "Retrieved Value: " + values)
            except Exception as e:
                logging.info("Error Details: " + str(e))
                logging.info(traceback.format_exc())
'''        

if __name__ == "__main__":
    print load_irdg_config(sys.argv[1], sys.argv[2], sys.argv[3])
