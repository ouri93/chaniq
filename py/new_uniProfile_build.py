from f5.bigip import ManagementRoot
import sys
import logging
import json

def check_profileName_conflict(mr, prfName, prfDftFrom):
    uniPrfNames = mr.tm.ltm.persistence.universals.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for uniPrfName in uniPrfNames:
        if uniPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

# 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','timeout', 'rule', 'overrideConnectionLimit'		
def new_uniProfile_build(prfDevIp, prfName, prfDplyOrChg, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, timeout, rule, overrideConnectionLimit):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (dev_ip, pf_type))
	
    mr = ManagementRoot(str(prfDevIp), 'admin', 'rlatkdcks')
    output = ''

    logging.info("new_uniProfile_build.py Parms \nDevIP: " + prfDevIp + "\nProfile name: " + prfName + "\nProfile Deploy or Change: " + prfDplyOrChg + "\nDefaults-from: " + defaultsFrom + "\n") 
	
    idx = 1
    
    if prfDplyOrChg == 'new_profile':      
        strReturn = {str(idx) : 'Universal Persistence Profile Creation Report'}
    
        idx += 1
    
        logging.info("Profile Creation process has been initiated. Universal Persistence Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logging.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logging.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.persistence.universals.universal.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, matchAcrossServices=matchAcrossServices, matchAcrossVirtuals=matchAcrossVirtuals, matchAcrossPools=matchAcrossPools, timeout=timeout, rule=rule, overrideConnectionLimit=overrideConnectionLimit)
        except Exception as e:
            logging.info("Exception during Universal Persistence Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Universal Persistence Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile':
        strReturn = {str(idx) : 'Universal Persistence Profile Modification Report'}
        idx += 1
    
        logging.info("Profile Modification process has been initiated. Universal Persistence Profile Name: " + prfName)
        
        # Load Universal Persistence profile settings of a given Universal Persistence profile name
        # 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','timeout', 'rule', 'overrideConnectionLimit'
        try:
            aUnivPrf = mr.tm.ltm.persistence.universals.universal.load(name=prfName, partition='Common')
        except Exception as e:
            logging.info("Exception during Universal Persistence Profile loading")
            strReturn[str(idx)] = "Exception fired during Universal Persistence Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during Universal Persistence Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools', 'timeout', 'overrideConnectionLimit'
        aUnivPrf.defaultsFrom = defaultsFrom
        aUnivPrf.matchAcrossServices = matchAcrossServices
        aUnivPrf.matchAcrossVirtuals = matchAcrossVirtuals
        aUnivPrf.matchAcrossPools = matchAcrossPools
        aUnivPrf.timeout = timeout
        aUnivPrf.rule = rule
        aUnivPrf.overrideConnectionLimit = overrideConnectionLimit
        
        strReturn[str(idx)] = "Universal Persistence Profile settings have been saved!"
        idx += 1

        try:
            aUnivPrf.update()
        except Exception as e:
            strReturn[str(idx)] = "Exception fired during Universal Persistence profile update() (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Universal Persistence Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
        
    if prfDplyOrChg == 'new_profile':  
        strReturn[str(idx)] = "Universal Persistence Profile (" + prfName + ") has been created"
        idx += 1
        logging.info("Universal Persistence Profile has been created")
    elif prfDplyOrChg == 'chg_profile':  
        strReturn[str(idx)] = "Universal Persistence Profile Modification(" + prfName + ") has been completed"
        idx += 1
        logging.info("Universal Persistence Profile modification has been completed")

        
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_uniProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])
