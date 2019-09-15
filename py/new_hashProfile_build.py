from f5.bigip import ManagementRoot
import sys
import logging
import json

def check_profileName_conflict(mr, prfName, prfDftFrom):
    hashPrfNames = mr.tm.ltm.persistence.hashs.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for hashPrfName in hashPrfNames:
        if hashPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  
# defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, hashOffset, hashLength, hashStartPattern, hashEndPattern, hashBufferLimit, timeout, rule, overrideConnectionLimit		
def new_hashProfile_build(prfDevIp, prfName, prfDplyOrChg, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, hashOffset, hashLength, hashStartPattern, hashEndPattern, hashBufferLimit, timeout, rule, overrideConnectionLimit):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (dev_ip, pf_type))
	
    mr = ManagementRoot(str(prfDevIp), 'admin', 'rlatkdcks')
    output = ''

    logging.info("new_hashProfile_build.py Parms \nDevIP: " + prfDevIp + "\nProfile name: " + prfName + "\nProfile Deploy or Change: " + prfDplyOrChg + "\nDefaults-from: " + defaultsFrom + "\n") 

    idx = 1

    if prfDplyOrChg == 'new_profile':    
        strReturn = {str(idx) : 'Hash Persistence Profile Creation Report'}
        idx += 1
    
        logging.info("Profile Creation process has been initiated. Hash Persistence Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logging.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logging.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.persistence.hashs.hash.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, matchAcrossServices=matchAcrossServices, matchAcrossVirtuals=matchAcrossVirtuals, matchAcrossPools=matchAcrossPools, hashAlgorithm=hashAlgorithm, hashOffset=hashOffset, hashLength=hashLength, hashStartPattern=hashStartPattern, hashEndPattern=hashEndPattern, hashBufferLimit=hashBufferLimit, timeout=timeout, rule=rule, overrideConnectionLimit=overrideConnectionLimit)
        except Exception as e:
            logging.info("Exception during Hash Persistence Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Hash Persistence Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    if prfDplyOrChg == 'chg_profile':
        strReturn = {str(idx) : 'Hash Persistence Profile Modification Report'}
        idx += 1
    
        logging.info("Profile Modification process has been initiated. Hash Persistence Profile Name: " + prfName)

        # Load Hash Persistence profile settings of a given Hash profile name
        try:
            aHashPrf = mr.tm.ltm.persistence.hashs.hash.load(name=prfName, partition='Common')
        except Exception as e:
            logging.info("Exception during Hash Persistence Profile loading")
            strReturn[str(idx)] = "Exception fired during Hash Persistence Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during Hash Persistence Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, hashOffset, hashLength, 
        # hashStartPattern, hashEndPattern, hashBufferLimit, timeout, rule, overrideConnectionLimit
        # Save the update DNS profile settings
        aHashPrf.defaultsFrom = defaultsFrom
        aHashPrf.matchAcrossServices = matchAcrossServices
        aHashPrf.matchAcrossVirtuals = matchAcrossVirtuals
        aHashPrf.matchAcrossPools = matchAcrossPools
        aHashPrf.hashAlgorithm = hashAlgorithm
        aHashPrf.hashOffset = hashOffset
        aHashPrf.hashLength = hashLength
        aHashPrf.hashStartPattern = hashStartPattern
        aHashPrf.hashEndPattern = hashEndPattern
        aHashPrf.hashBufferLimit = hashBufferLimit
        aHashPrf.timeout = timeout
        aHashPrf.rule = rule
        aHashPrf.overrideConnectionLimit = overrideConnectionLimit
        
        strReturn[str(idx)] = "Hash Persistence Profile settings have been saved!"
        idx += 1
        
        try:
            aHashPrf.update()
        except Exception as e:
            strReturn[str(idx)] = "Exception fired during Hash Persistence profile update() (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Hash Persistence Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
        
    if prfDplyOrChg == 'new_profile':
        strReturn[str(idx)] = "Hash Persistence Profile (" + prfName + ") has been created"
        idx += 1
        logging.info("Hash Persistence Profile has been created")
    elif prfDplyOrChg == 'chg_profile':  
        strReturn[str(idx)] = "Hash Persistence Profile modificaiton(" + prfName + ") has been completed"
        idx += 1
        logging.info("Hash Persistence Profile modification has been completed")
        
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_hashProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14], sys.argv[15], sys.argv[16])
