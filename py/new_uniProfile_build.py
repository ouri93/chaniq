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
    uniPrfNames = mr.tm.ltm.persistence.universals.get_collection()
    logger.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for uniPrfName in uniPrfNames:
        if uniPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logger.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

def isNeedUpdate(loadedPrf, modContent, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, timeout, rule, overrideConnectionLimit):
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
    
    

# 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','timeout', 'rule', 'overrideConnectionLimit'		
def new_uniProfile_build(active_ltm, prfName, prfDplyOrChg, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, timeout, rule, overrideConnectionLimit):
    #logger.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    output = ''

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logger.info("new_uniProfile_build()- Use Standard Global naming : " + useGlobalNaming )
    
    logger.info("new_uniProfile_build.py Parms \nDevIP: " + active_ltm + "\nProfile name: " + prfName + "\nProfile Deploy or Change: " + prfDplyOrChg + "\nDefaults-from: " + defaultsFrom + "\n") 
	
    idx = 1
    
    if prfDplyOrChg == 'new_profile':      
        strReturn = {str(idx) : 'Universal Persistence Profile Creation Report'}
    
        idx += 1

        if useGlobalNaming == '1':
            prfName = loadStdNames.get_std_name(active_ltm, 'SHARED', 'PROFILE', 'UNIVERSAL_PERSISTENCE', prfName)
                
        logger.info("Profile Creation process has been initiated. Universal Persistence Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logger.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logger.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.persistence.universals.universal.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, matchAcrossServices=matchAcrossServices, matchAcrossVirtuals=matchAcrossVirtuals, matchAcrossPools=matchAcrossPools, timeout=timeout, rule=rule, overrideConnectionLimit=overrideConnectionLimit)
        except Exception as e:
            logger.info("Exception during Universal Persistence Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logger.info("Universal Persistence Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile':
        
        modContent = {}
        
        strReturn = {str(idx) : 'Universal Persistence Profile Modification Report'}
        idx += 1
    
        logger.info("Profile Modification process has been initiated. Universal Persistence Profile Name: " + prfName)
        
        # Load Universal Persistence profile settings of a given Universal Persistence profile name
        # 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','timeout', 'rule', 'overrideConnectionLimit'
        try:
            loadedPrf = mr.tm.ltm.persistence.universals.universal.load(name=prfName, partition='Common')
        except Exception as e:
            logger.info("Exception during Universal Persistence Profile loading")
            strReturn[str(idx)] = "Exception fired during Universal Persistence Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logger.info("Exception fired during Universal Persistence Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools', 'timeout', 'overrideConnectionLimit'
        '''
        loadedPrf.defaultsFrom = defaultsFrom
        loadedPrf.matchAcrossServices = matchAcrossServices
        loadedPrf.matchAcrossVirtuals = matchAcrossVirtuals
        loadedPrf.matchAcrossPools = matchAcrossPools
        loadedPrf.timeout = timeout
        loadedPrf.rule = rule
        loadedPrf.overrideConnectionLimit = overrideConnectionLimit
        '''
        
        if isNeedUpdate(loadedPrf, modContent, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, timeout, rule, overrideConnectionLimit):
            strReturn[str(idx)] = "Universal Persistence Profile settings have been saved!"
            idx += 1
    
            try:
                #loadedPrf.update()
                loadedPrf.modify(**modContent)
            except Exception as e:
                strReturn[str(idx)] = "Exception fired during Universal Persistence profile update() (" + prfName + "): " + str(e)
                idx += 1
                logger.info("Universal Persistence Profile creation exception fired: " + str(e))
                return json.dumps(strReturn)
        else:
            logger.info("No Universal Persistence Profile modification is needed")
            strReturn[str(idx)] = "No SSLUniversalPersistence Profile modification is needed (" + prfName + "): "
            idx += 1             
        
    if prfDplyOrChg == 'new_profile':  
        strReturn[str(idx)] = "Universal Persistence Profile (" + prfName + ") has been created"
        idx += 1
        logger.info("Universal Persistence Profile has been created")
    elif prfDplyOrChg == 'chg_profile':  
        strReturn[str(idx)] = "Universal Persistence Profile Modification(" + prfName + ") has been completed"
        idx += 1
        logger.info("Universal Persistence Profile modification has been completed")

        
    for keys, values in strReturn.items():
        logger.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logger.info('main called: param1: ')
    print new_uniProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])
