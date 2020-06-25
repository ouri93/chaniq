from f5.bigip import ManagementRoot
import sys
import logging
import json
import build_std_names
import getpass
import loadStdNames

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

logger.info("Head of new_irule_build() called")

def check_irulename_conflict(mr, std_irname):
    irnames = mr.tm.ltm.rules.get_collection()
    logger.info("check_irulename_conflict() STD Name: " + std_irname + "\n")
    
    bitout = 0
    
    for air in irnames:
        if air.exists(name=std_irname):
            bitout = bitout | (1 << 0)
    

    #logger.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

# Only support Internal Data Group
def check_datagroupname_conflict(mr, std_irname):
    dgnames = mr.tm.ltm.data_group.internals.get_collection()
    logger.info("check_datagroupname_conflict() STD Name: " + std_irname + "\n")
    
    bitout = 0
    
    for adg in dgnames:
        if adg.exists(name=std_irname):
            bitout = bitout | (1 << 0)
    

    #logger.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

def check_irname_conflict(mr, std_irname, irType, irDgType):
    
    logger.info("new_irule_build() - check_irname_conflict() iRule/Data Group name: " + std_irname + " Config Type: " + irType + " DataGroup Type: " + irDgType)
    
    byIrType = {
        "iRule": check_irulename_conflict,
        "Data Group": check_datagroupname_conflict
    }
    
    return byIrType[irType](mr, std_irname)

def new_irule_build(active_ltm, irDgName, irEnv, irType, irCode, irDgType, irDgData):
    logger.info("new_irule_build.py parms\n DevIP: " + active_ltm + "\niRule/Data Group Name: " + irDgName + "\nEnv: " + irEnv + "\nConfig Type: " + irType + "\niRule Code: " + irCode + "\nDG Type: " + irDgType + "\nDG Data: " + irDgData + "\n") 

    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logger.info("new_irule_build()- Use Standard Global naming : " + useGlobalNaming )
        
    idx = 1
    strReturn = {str(idx) : 'iRule/Data Group Creation Report'}
    
    idx += 1

    if useGlobalNaming == '1':
        logger.info("new_irule_build()- Standard Global naming process starts!" )
        if irType == 'iRule':
            std_irname = loadStdNames.get_std_name(active_ltm, 'SHARED', 'IRULE', '', irDgName)
        elif irType == 'Data Group':
            std_irname = loadStdNames.get_std_name(active_ltm, 'SHARED', 'DATA_GROUP', '', irDgName)
        
    #std_irname = build_std_names.build_std_ir_name(str(irEnv), str(irDgName), str(irType))
    logger.info("iRule/Data Group Creation process has been initiated. iRule/Data Group Name: " + std_irname) 
    
    if check_irname_conflict(mr, std_irname, irType, irDgType):
        strReturn.update({str(idx) : 'iRule/Data Group Name conflict'})
        logger.info("iRule/Data Group name conflict.")
        idx += 1
        return json.dumps(strReturn)
    logger.info("No iRule/Data Group name conflict. Now creating a iRule/Data Group")
    
    #Create a iRule/Data Group
    try:
        if irType == "iRule":
            myir = mr.tm.ltm.rules.rule.create(name=std_irname, partition='Common', apiAnonymous=irCode)
        elif irType == "Data Group":
            new_records = []
            arrRecords = irDgData.split(',');
            for arrRecord in arrRecords:
                aRecord = arrRecord.split(':=')
                logger.info("name: " + aRecord[0] + " Value: " + aRecord[1])
                nr = [{'name':str(aRecord[0]), 'data':str(aRecord[1])}]
                new_records.extend(nr)
            if irDgType == "ip":
                mydg = mr.tm.ltm.data_group.internals.internal.create(name=std_irname, partition='Common', type='ip', records=new_records)
            elif irDgType == "string":
                mydg = mr.tm.ltm.data_group.internals.internal.create(name=std_irname, partition='Common', type='string', records=new_records)
            elif irDgType == "integer":
                mydg = mr.tm.ltm.data_group.internals.internal.create(name=std_irname, partition='Common', type='integer', records=new_records)
    except Exception as e:
        logger.info("iRule/Data Group Exception printing")
        strReturn[str(idx)] = "Exception fired! (" + std_irname + "): " + str(e)
        idx += 1
        logger.info("Exception during iRule/Data Group creation has been fired: " + str(e))
        return json.dumps(strReturn)
    
    strReturn[str(idx)] = irType + " iRule/Data Group (" + std_irname + ") has been created"
    idx += 1
    logger.info("iRule/Data Group has been created")
                    
    
    for keys, values in strReturn.items():
        logger.info("Key: " + keys + " Value: " + values)

    return json.dumps(strReturn)

if __name__ == "__main__":
    print new_irule_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
