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
    srcAffPrfNames = mr.tm.ltm.persistence.source_addrs.get_collection()
    logger.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for srcAffPrfName in srcAffPrfNames:
        if srcAffPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logger.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  
    
def isNeedUpdate(loadedPrf, modContent, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, timeout, mask, mapProxies, overrideConnectionLimit):
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
    if chaniq_util.isStrPropModified(loadedPrf, 'timeout', timeout):
        modContent['timeout'] = timeout
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'mask', mask):
        modContent['mask'] = mask
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'mapProxies', mapProxies):
        modContent['mapProxies'] = mapProxies
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'overrideConnectionLimit', overrideConnectionLimit):
        modContent['overrideConnectionLimit'] = overrideConnectionLimit
        cnt = cnt + 1     
        
    if cnt > 0: return True
    else: return False
        
# 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 
# 'timeout', 'mask', 'mapProxies', 'overrideConnectionLimit'		
def new_srcAffProfile_build(active_ltm, prfName, prfDplyOrChg, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, timeout, mask, mapProxies, overrideConnectionLimit):
    #logger.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    output = ''

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logger.info("new_srcAffProfile_build()- Use Standard Global naming : " + useGlobalNaming )
    
    logger.info("new_srcAffProfile_build.py Parms \nDevIP: " + active_ltm + "\nProfile name: " + prfName + "\nProfile Deploy or Change: " + prfDplyOrChg + "\nDefaults-from: " + defaultsFrom + "\n") 
    idx = 1

    if prfDplyOrChg == 'new_profile':

        if useGlobalNaming == '1':
            prfName = loadStdNames.get_std_name(active_ltm, 'SHARED', 'PROFILE', 'SOURCE_PERSISTENCE', prfName)
                    
        logger.info("Profile Creation process has been initiated. Source Address Persistence Profile Name: " + prfName)
        
        strReturn = {str(idx) : 'Source Address Persistence Profile Creation Report'}
        idx += 1
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logger.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logger.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.persistence.source_addrs.source_addr.create(name=prfName, partition='Common', \
                    defaultsFrom=defaultsFrom, matchAcrossServices=matchAcrossServices, matchAcrossVirtuals=matchAcrossVirtuals, \
                    matchAcrossPools=matchAcrossPools, hashAlgorithm=hashAlgorithm, timeout=timeout, mask=mask, mapProxies=mapProxies, \
                    overrideConnectionLimit=overrideConnectionLimit)
        except Exception as e:
            logger.info("Exception during Source Address Persistence Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logger.info("Source Address Persistence Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile':
        
        modContent = {}
        
        strReturn = {str(idx) : 'Source Address Persistence Profile Modification Report'}
        idx += 1

        logger.info("Profile Modification process has been initiated. Source Address Persistence Profile Name: " + prfName)
            
        # Load Source Affinity profile settings of a given Source Affinity profile name
        try:
            loadedPrf = mr.tm.ltm.persistence.source_addrs.source_addr.load(name=prfName, partition='Common')
        except Exception as e:
            logger.info("Exception during Source Affinity Profile loading")
            strReturn[str(idx)] = "Exception fired during Source Affinity Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logger.info("Exception fired during Source Affinity Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # Save the update DNS profile settings
        '''
        loadedPrf.defaultsFrom = defaultsFrom
        loadedPrf.matchAcrossServices = matchAcrossServices
        loadedPrf.matchAcrossVirtuals = matchAcrossVirtuals
        loadedPrf.matchAcrossPools = matchAcrossPools
        loadedPrf.hashAlgorithm = hashAlgorithm
        loadedPrf.timeout = timeout
        loadedPrf.mask = mask
        loadedPrf.mapProxies = mapProxies
        loadedPrf.overrideConnectionLimit = overrideConnectionLimit
        '''
        
        if isNeedUpdate(loadedPrf, modContent, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, timeout, mask, mapProxies, overrideConnectionLimit):
            strReturn[str(idx)] = "Source Affinity Profile settings have been saved!"
            idx += 1
            
            try:
                #loadedPrf.update()
                loadedPrf.modify(**modContent)
            except Exception as e:
                strReturn[str(idx)] = "Exception fired during Source Affinity profile update() (" + prfName + "): " + str(e)
                idx += 1
                logger.info("Source Affinity Profile creation exception fired: " + str(e))
                return json.dumps(strReturn)
        else:
            logger.info("No Source Address Persistence Profile modification is needed")
            strReturn[str(idx)] = "No Source Address Persistence Profile modification is needed (" + prfName + "): "
            idx += 1  
                        
    if prfDplyOrChg == 'new_profile':      
        strReturn[str(idx)] = "Source Address Persistence Profile (" + prfName + ") has been created"
        idx += 1
        logger.info("Source Address Persistence Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "Source Address Persistence Profile modification(" + prfName + ") has been completed"
        idx += 1
        logger.info("Source Address Persistence Profile modification has been completed")
        
    for keys, values in strReturn.items():
        logger.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logger.info('main called: param1: ')
    print new_srcAffProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12])
