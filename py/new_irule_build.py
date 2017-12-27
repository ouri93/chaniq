from f5.bigip import ManagementRoot
import sys
import logging
import json
import build_std_names

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
logging.info("Head of new_irule_build() called")

def check_irulename_conflict(mr, std_irname):
    irnames = mr.tm.ltm.rules.get_collection()
    logging.info("check_irulename_conflict() STD Name: " + std_irname + "\n")
    
    bitout = 0
    
    for air in irnames:
        if air.exists(name=std_irname):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

# Only support Internal Data Group
def check_datagroupname_conflict(mr, std_irname):
    dgnames = mr.tm.ltm.data_group.internals.get_collection()
    logging.info("check_datagroupname_conflict() STD Name: " + std_irname + "\n")
    
    bitout = 0
    
    for adg in dgnames:
        if adg.exists(name=std_irname):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

def check_irname_conflict(mr, std_irname, irType, irDgType):
    
    logging.info("new_irule_build() - check_irname_conflict() iRule/Data Group name: " + std_irname + " Monitor Type: " + irType + " DG Type: " + irDgType)
    
    byIrType = {
        "iRule": check_irulename_conflict,
        "Data Group": check_datagroupname_conflict
    }
    
    return byIrType[irType](mr, std_irname)

#def new_irule_build(active_ltm, vs_dnsname, vs_port, vs_env, vs_poolmon, pLBMethod):
def new_irule_build(irDevIp, irVsName, irVsPort, irEnv, irType, irCode, irDgType, irDgData):
    
    logging.info("new_irule_build.py parms DevIP: " + irDevIp + " VS Name: " + irVsName + " VS Port: " + irVsPort + " Env: " + irEnv + " Mon Code: " + irCode + " DG Type: " + irDgType + " DG Data: " + irDgData) 

    mr = ManagementRoot(str(irDevIp), 'admin', 'rlatkdcks')
    
    idx = 1
    strReturn = {str(idx) : 'iRule/Data Group Creation Report'}
    
    idx += 1
 
    std_irname = build_std_names.build_std_ir_name(str(irEnv), str(irVsName), str(irVsPort), str(irType))
    logging.info("iRule/Data Group Creation process has been initiated. iRule/Data Group Name: " + std_irname) 
    
    if check_irname_conflict(mr, std_irname, irType, irDgType):
        strReturn.update({str(idx) : 'iRule/Data Group Name conflict'})
        logging.info("iRule/Data Group name conflict.")
        idx += 1
        return json.dumps(strReturn)
    logging.info("No iRule/Data Group name conflict. Now creating a iRule/Data Group")
    
    #Create a iRule/Data Group
    try:
        if irType == "iRule":
            myir = mr.tm.ltm.rules.rule.create(name=std_irname, partition='Common', apiAnonymous=irCode)
        elif irType == "Data Group":
            new_records = []
            arrRecords = irDgData.split(',');
            for arrRecord in arrRecords:
                aRecord = arrRecord.split(':')
                logging.info("name: " + aRecord[0] + " Value: " + aRecord[1])
                nr = [{'name':str(aRecord[0]), 'data':str(aRecord[1])}]
                new_records.extend(nr)
            if irDgType == "Address":
                mydg = mr.tm.ltm.data_group.internals.internal.create(name=std_irname, partition='Common', type='ip', records=new_records)
            elif irDgType == "String":
                mydg = mr.tm.ltm.data_group.internals.internal.create(name=std_irname, partition='Common', type='string', records=new_records)
            elif irDgType == "Integer":
                mydg = mr.tm.ltm.data_group.internals.internal.create(name=std_irname, partition='Common', type='integer', records=new_records)
    except Exception as e:
        logging.info("iRule/Data Group Exception printing")
        strReturn[str(idx)] = "Exception fired! (" + std_irname + "): " + str(e)
        idx += 1
        logging.info("iRule/Data Group creation exception fired: " + str(e))
        return json.dumps(strReturn)
    
    strReturn[str(idx)] = irType + " iRule/Data Group (" + std_irname + ") has been created"
    idx += 1
    logging.info("iRule/Data Group has been created")
                    
    
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)

    return json.dumps(strReturn)

if __name__ == "__main__":
    print new_irule_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
