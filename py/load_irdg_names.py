from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
logging.info("Head of load_irdg_names() called")

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

def load_irdg_names(active_ltm, irType, irDgPart):
    #'DevIP' 'IrType' 'IrDgPart'
    logging.info("load_irdg_names.py parms\n DevIP: " + active_ltm + "\niRule or Data Group: " + irType +  "\nPartition: " + irDgPart + "\n") 

    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    
    strReturn = ''

    logging.info("iRule/Data Group Modification process has been initiated.") 

    #Create a iRule/Data Group
    try:
        if irType == "iRule":
            ir_list = mr.tm.ltm.rules.get_collection()
            i=0
            ir_list_len = len(ir_list)-1
            for air in ir_list:
                if ir_list_len != i: 
                    strReturn += air.name + '|'
                else:
                    strReturn += air.name
                i = i+1
        elif irType == "Data Group":
            dg_list = mr.tm.ltm.data_group.internals.get_collection()
            i=0
            dg_list_len = len(dg_list)-1
            for adg in dg_list:
                if dg_list_len != i:
                    strReturn += adg.name + '|'
                else:
                    strReturn += adg.name
                i = i+1
    except Exception as e:
        logging.info("iRule/Data Group Exception - Retrieving iRule/Data Group names")
        logging.info("Error Details: " + str(e))
        return json.dumps(strReturn)
    
    logging.info("Retrieved names: " + strReturn)
    logging.info("Name retrieving for iRule/Data Group has been completed")
                    
    return json.dumps(strReturn)

if __name__ == "__main__":
    print load_irdg_names(sys.argv[1], sys.argv[2], sys.argv[3])
