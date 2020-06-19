from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass
import loadStdNames
import chaniq_util

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def check_profileName_conflict(mr, prfName, prfDftFrom):
    hashPrfNames = mr.tm.ltm.persistence.hashs.get_collection()
    logger.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for hashPrfName in hashPrfNames:
        if hashPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logger.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  
def isNeedUpdate(loadedPrf, modContent, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, hashOffset, hashLength, hashStartPattern, hashEndPattern, hashBufferLimit, timeout, rule, overrideConnectionLimit):
    cnt = 0

    if chaniq_util.isStrPropModified(loadedPrf, 'defaultsFrom', defaultsFrom):
        modContent['defaultsFrom'] = defaultsFrom
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'matchAcrossServices', matchAcrossServices):
        modContent['matchAcrossServices'] = matchAcrossServices
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'matchAcrossVirtuals', matchAcrossVirtuals):
        modContent['matchAcrossVirtuals'] = matchAcrossVirtuals
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'matchAcrossPools', matchAcrossPools):
        modContent['matchAcrossPools'] = matchAcrossPools
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'hashAlgorithm', hashAlgorithm):
        modContent['hashAlgorithm'] = hashAlgorithm
        cnt = cnt + 1 
    if chaniq_util.isIntPropModified(loadedPrf, 'hashOffset', hashOffset, 0):
        modContent['hashOffset'] = int(hashOffset)
        cnt = cnt + 1 
    if chaniq_util.isIntPropModified(loadedPrf, 'hashLength', hashLength, 0):
        modContent['hashLength'] = int(hashLength)
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'hashStartPattern', hashStartPattern):
        modContent['hashStartPattern'] = hashStartPattern
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'hashEndPattern', hashEndPattern):
        modContent['hashEndPattern'] = hashEndPattern
        cnt = cnt + 1 
    if chaniq_util.isIntPropModified(loadedPrf, 'hashBufferLimit', hashBufferLimit, 0):
        modContent['hashBufferLimit'] = int(hashBufferLimit)
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'timeout', timeout):
        modContent['timeout'] = timeout
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'rule', rule):
        modContent['rule'] = rule
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'overrideConnectionLimit', overrideConnectionLimit):
        modContent['overrideConnectionLimit'] = overrideConnectionLimit
        cnt = cnt + 1 
                                                                                          
    if cnt > 0: return True
    else: return False      

# defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, hashOffset, hashLength, hashStartPattern, hashEndPattern, hashBufferLimit, timeout, rule, overrideConnectionLimit		
def new_hashProfile_build(active_ltm, prfName, prfDplyOrChg, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, hashOffset, hashLength, hashStartPattern, hashEndPattern, hashBufferLimit, timeout, rule, overrideConnectionLimit):
    #logger.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    output = ''
    
    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logger.info("new_hashProfile_build()- Use Standard Global naming : " + useGlobalNaming )
    
    logger.info("new_hashProfile_build.py Parms \nDevIP: " + active_ltm + "\nProfile name: " + prfName + "\nProfile Deploy or Change: " + prfDplyOrChg + "\nDefaults-from: " + defaultsFrom + "\n") 

    idx = 1

    if prfDplyOrChg == 'new_profile':    
        strReturn = {str(idx) : 'Hash Persistence Profile Creation Report'}
        idx += 1

        if useGlobalNaming == '1':
            prfName = loadStdNames.get_std_name(active_ltm, 'SHARED', 'PROFILE', 'HASH_PERSISTENCE', prfName)
                
        logger.info("Profile Creation process has been initiated. Hash Persistence Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logger.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logger.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.persistence.hashs.hash.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, matchAcrossServices=matchAcrossServices, matchAcrossVirtuals=matchAcrossVirtuals, matchAcrossPools=matchAcrossPools, hashAlgorithm=hashAlgorithm, hashOffset=hashOffset, hashLength=hashLength, hashStartPattern=hashStartPattern, hashEndPattern=hashEndPattern, hashBufferLimit=hashBufferLimit, timeout=timeout, rule=rule, overrideConnectionLimit=overrideConnectionLimit)
        except Exception as e:
            logger.info("Exception during Hash Persistence Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logger.info("Hash Persistence Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    if prfDplyOrChg == 'chg_profile':
        
        modContent = {}
        
        strReturn = {str(idx) : 'Hash Persistence Profile Modification Report'}
        idx += 1
    
        logger.info("Profile Modification process has been initiated. Hash Persistence Profile Name: " + prfName)

        # Load Hash Persistence profile settings of a given Hash profile name
        try:
            loadedPrf = mr.tm.ltm.persistence.hashs.hash.load(name=prfName, partition='Common')
        except Exception as e:
            logger.info("Exception during Hash Persistence Profile loading")
            strReturn[str(idx)] = "Exception fired during Hash Persistence Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logger.info("Exception fired during Hash Persistence Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, hashOffset, hashLength, 
        # hashStartPattern, hashEndPattern, hashBufferLimit, timeout, rule, overrideConnectionLimit
        # Save the update DNS profile settings
        '''
        loadedPrf.defaultsFrom = defaultsFrom
        loadedPrf.matchAcrossServices = matchAcrossServices
        loadedPrf.matchAcrossVirtuals = matchAcrossVirtuals
        loadedPrf.matchAcrossPools = matchAcrossPools
        loadedPrf.hashAlgorithm = hashAlgorithm
        loadedPrf.hashOffset = hashOffset
        loadedPrf.hashLength = hashLength
        loadedPrf.hashStartPattern = hashStartPattern
        loadedPrf.hashEndPattern = hashEndPattern
        loadedPrf.hashBufferLimit = hashBufferLimit
        loadedPrf.timeout = timeout
        loadedPrf.rule = rule
        loadedPrf.overrideConnectionLimit = overrideConnectionLimit
        '''

        if isNeedUpdate(loadedPrf, modContent, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, hashOffset, hashLength, hashStartPattern, hashEndPattern, hashBufferLimit, timeout, rule, overrideConnectionLimit):        
            strReturn[str(idx)] = "Hash Persistence Profile settings have been saved!"
            idx += 1
            
            try:
                #loadedPrf.update()
                loadedPrf.modify(**modContent)
            except Exception as e:
                strReturn[str(idx)] = "Exception fired during Hash Persistence profile update() (" + prfName + "): " + str(e)
                idx += 1
                logger.info("Hash Persistence Profile creation exception fired: " + str(e))
                return json.dumps(strReturn)
        else:
            logger.info("No Hash Persistence Profile modification is needed")
            strReturn[str(idx)] = "No Hash Persistence Profile modification is needed (" + prfName + "): "
            idx += 1
            
    if prfDplyOrChg == 'new_profile':
        strReturn[str(idx)] = "Hash Persistence Profile (" + prfName + ") has been created"
        idx += 1
        logger.info("Hash Persistence Profile has been created")
    elif prfDplyOrChg == 'chg_profile':  
        strReturn[str(idx)] = "Hash Persistence Profile modificaiton(" + prfName + ") has been completed"
        idx += 1
        logger.info("Hash Persistence Profile modification has been completed")
        
    for keys, values in strReturn.items():
        logger.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logger.info('main called: param1: ')
    print new_hashProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14], sys.argv[15], sys.argv[16])
