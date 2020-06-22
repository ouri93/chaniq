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
    ocPrfNames = mr.tm.ltm.profile.one_connects.get_collection()
    logger.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for ocPrfName in ocPrfNames:
        if ocPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logger.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

def isNeedUpdate(loadedPrf, modContent, defaultsFrom, sourceMask, maxSize, maxAge, maxReuse, idleTimeoutOverride, limitType):
    cnt = 0
    
    if chaniq_util.isStrPropModified(loadedPrf, 'defaultsFrom', defaultsFrom):
        modContent['defaultsFrom'] = defaultsFrom
        cnt = cnt + 1  
    if chaniq_util.isIntPropModified(loadedPrf, 'maxSize', maxSize, 15000):
        modContent['maxSize'] = maxSize
        cnt = cnt + 1 
    if chaniq_util.isIntPropModified(loadedPrf, 'maxAge', maxAge, 86400):
        modContent['maxAge'] = maxAge
        cnt = cnt + 1 
    if chaniq_util.isIntPropModified(loadedPrf, 'maxSize', maxSize, 1000):
        modContent['maxSize'] = maxSize
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'sourceMask', sourceMask):
        modContent['sourceMask'] = sourceMask
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'idleTimeoutOverride', idleTimeoutOverride):
        modContent['idleTimeoutOverride'] = idleTimeoutOverride
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'limitType', limitType):
        modContent['limitType'] = limitType
        cnt = cnt + 1 
    
    if cnt > 0: return True
    else: return False    
    

#'defaultsFrom', 'sourceMask', 'maxSize', 'maxAge', 'maxReuse', 'idleTimeoutOverride', 'limitType'
def new_ocProfile_build(active_ltm, prfName, prfDplyOrChg, defaultsFrom, sourceMask, maxSize, maxAge, maxReuse, idleTimeoutOverride, limitType):
    #logger.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    output = ''

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logger.info("new_ocProfile_build()- Use Standard Global naming : " + useGlobalNaming )
    
    logger.info("new_ocProfile_build.py Parms DevIP: " + active_ltm + " Profile name: " + prfName + " Profile Deploy or Change: " + prfDplyOrChg + " Defaults-from: " + defaultsFrom) 

    idx = 1
    if prfDplyOrChg == 'new_profile':    
        strReturn = {str(idx) : 'OneConnect Profile Creation Report'}
        idx += 1

        if useGlobalNaming == '1':
            prfName = loadStdNames.get_std_name(active_ltm, 'SHARED', 'PROFILE', 'ONECONNECT', prfName)
                
        logger.info("Profile Creation process has been initiated. OneConnect Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logger.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logger.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.profile.one_connects.one_connect.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, sourceMask=sourceMask, \
                   maxSize=maxSize, maxAge=maxAge, maxReuse=maxReuse, idleTimeoutOverride=idleTimeoutOverride, limitType=limitType)
        except Exception as e:
            logger.info("Exception during OneConnect Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logger.info("OneConnect Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile':
        
        modContent = {}
        
        strReturn = {str(idx) : 'OneConnect Profile Modification Report'}
        idx += 1
    
        logger.info("Profile Modification process has been initiated. OneConnect Profile Name: " + prfName)
        
        # Load OneConnect profile settings of a given OneConnect profile name
        # 'defaultsFrom', 'sourceMask', 'maxSize', 'maxAge', 'maxReuse', 'idleTimeoutOverride', 'limitType'
        try:
            loadedPrf = mr.tm.ltm.profile.one_connects.one_connect.load(name=prfName, partition='Common')
        except Exception as e:
            logger.info("Exception during OneConnect Profile loading")
            strReturn[str(idx)] = "Exception fired during OneConnect Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logger.info("Exception fired during OneConnect Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # Save the update OneConnect profile settings
        '''
        loadedPrf.defaultsFrom = defaultsFrom
        loadedPrf.sourceMask = sourceMask
        loadedPrf.maxSize = maxSize
        loadedPrf.maxAge = maxAge
        loadedPrf.maxReuse = maxReuse
        loadedPrf.idleTimeoutOverride = idleTimeoutOverride
        loadedPrf.limitType = limitType
        '''

        if isNeedUpdate(loadedPrf, modContent, defaultsFrom, sourceMask, maxSize, maxAge, maxReuse, idleTimeoutOverride, limitType):
            strReturn[str(idx)] = "OneConnect Profile settings have been saved!"
            idx += 1
            
            try:
                #loadedPrf.update()
                loadedPrf.modify(**modContent)
            except Exception as e:
                strReturn[str(idx)] = "Exception fired during OneConnect profile loading (" + prfName + "): " + str(e)
                idx += 1
                logger.info("Exception fired during OneConnect profile loading: " + str(e))
                return json.dumps(strReturn)
        else:
            logger.info("No OneConnect Profile modification is needed")
            strReturn[str(idx)] = "No OneConnect Profile modification is needed (" + prfName + "): "
            idx += 1                  
    if prfDplyOrChg == 'new_profile':
        strReturn[str(idx)] = "OneConnect Profile(" + prfName + ") has been created"
        idx += 1
        logger.info("OneConnect Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "OneConnect Profile Modification(" + prfName + ") has been completd"
        idx += 1
        logger.info("OneConnect Profile Modification has been completed")

    for keys, values in strReturn.items():
        logger.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logger.info('main called: param1: ')
    print new_ocProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])
