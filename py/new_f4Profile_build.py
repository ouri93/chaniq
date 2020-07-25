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
    f4PrfNames = mr.tm.ltm.profile.fastl4s.get_collection()
    logger.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for f4PrfName in f4PrfNames:
        if f4PrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logger.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

def isNeedUpdate(loadedPrf, modContent, defaultsFrom, resetOnTimeout, reassembleFragments, idleTimeout, tcpHandshakeTimeout, tcpTimestampMode, tcpWscaleMode, looseInitialization, looseClose, tcpCloseTimeout, keepAliveInterval):
    cnt = 0

    if chaniq_util.isStrPropModified(loadedPrf, 'defaultsFrom', defaultsFrom):
        modContent['defaultsFrom'] = defaultsFrom
        cnt = cnt + 1     
    if chaniq_util.isStrPropModified(loadedPrf, 'resetOnTimeout', resetOnTimeout):
        modContent['resetOnTimeout'] = resetOnTimeout
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'reassembleFragments', reassembleFragments):
        modContent['reassembleFragments'] = reassembleFragments
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'idleTimeout', idleTimeout):
        modContent['idleTimeout'] = idleTimeout
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'tcpHandshakeTimeout', tcpHandshakeTimeout):
        modContent['tcpHandshakeTimeout'] = tcpHandshakeTimeout
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'tcpTimestampMode', tcpTimestampMode):
        modContent['tcpTimestampMode'] = tcpTimestampMode
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'tcpWscaleMode', tcpWscaleMode):
        modContent['tcpWscaleMode'] = tcpWscaleMode
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'looseInitialization', looseInitialization):
        modContent['looseInitialization'] = looseInitialization
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'looseClose', looseClose):
        modContent['looseClose'] = looseClose
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'tcpCloseTimeout', tcpCloseTimeout):
        modContent['tcpCloseTimeout'] = tcpCloseTimeout
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'keepAliveInterval', keepAliveInterval):
        modContent['keepAliveInterval'] = keepAliveInterval
        cnt = cnt + 1  
                
    if cnt > 0: return True
    else: return False    

# 'defaultsFrom', 'resetOnTimeout', 'reassembleFragments', 'idleTimeout',
# 'tcpHandshakeTimeout', 'tcpTimestampMode', 'tcpWscaleMode', 'looseInitialization',
# 'looseClose', 'tcpCloseTimeout', 'keepAliveInterval'		
def new_f4Profile_build(active_ltm, prfName, prfDplyOrChg, defaultsFrom, resetOnTimeout, reassembleFragments, idleTimeout, tcpHandshakeTimeout, tcpTimestampMode, tcpWscaleMode, looseInitialization, looseClose, tcpCloseTimeout, keepAliveInterval):
    #logger.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    output = ''

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logger.info("new_f4Profile_build()- Use Standard Global naming : " + useGlobalNaming )   
        
    logger.info("new_f4Profile_build.py Parms DevIP: " + active_ltm + " Profile name: " + prfName + " Profile Deploy or Change: " + prfDplyOrChg + " Defaults-from: " + defaultsFrom) 
	
    idx = 1
    if prfDplyOrChg == 'new_profile':  
        strReturn = {str(idx) : 'FastL4  Profile Creation Report'}
    
        idx += 1
        
        if useGlobalNaming == '1':
            prfName = loadStdNames.get_std_name(active_ltm, 'SHARED', 'PROFILE', 'FASTL4_PROTOCOL', prfName)     
    
        logger.info("Profile Creation process has been initiated. FastL4  Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logger.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logger.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.profile.fastl4s.fastl4.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, resetOnTimeout=resetOnTimeout,\
                     reassembleFragments=reassembleFragments, idleTimeout=idleTimeout, tcpHandshakeTimeout=tcpHandshakeTimeout, \
                     tcpTimestampMode=tcpTimestampMode, tcpWscaleMode=tcpWscaleMode, looseInitialization=looseInitialization, looseClose=looseClose, \
                     tcpCloseTimeout=tcpCloseTimeout, keepAliveInterval=keepAliveInterval)
        except Exception as e:
            logger.info("Exception during FastL4  Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logger.info("FastL4  Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile':
        
        modContent = {}
        
        strReturn = {str(idx) : 'FastL4  Profile Modification Report'}
        idx += 1
    
        logger.info("Profile Modification process has been initiated. FastL4 Profile Name: " + prfName)
        
        # Load FastL4 profile settings of a given FastL4 profile name
        # 'defaultsFrom', 'resetOnTimeout', 'reassembleFragments', 'idleTimeout',
        # 'tcpHandshakeTimeout', 'tcpTimestampMode', 'tcpWscaleMode', 'looseInitialization',
        # 'looseClose', 'tcpCloseTimeout', 'keepAliveInterval'    
        try:
            loadedPrf = mr.tm.ltm.profile.fastl4s.fastl4.load(name=prfName, partition='Common')
        except Exception as e:
            logger.info("Exception during FastL4 Profile loading")
            strReturn[str(idx)] = "Exception fired during FastL4 Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logger.info("Exception fired during FastL4 Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # Save the update FastL4 profile settings
        '''
        loadedPrf.defaultsFrom = defaultsFrom
        loadedPrf.resetOnTimeout = resetOnTimeout
        loadedPrf.reassembleFragments = reassembleFragments
        loadedPrf.idleTimeout = idleTimeout
        loadedPrf.tcpHandshakeTimeout = tcpHandshakeTimeout
        loadedPrf.tcpTimestampMode = tcpTimestampMode
        loadedPrf.tcpWscaleMode = tcpWscaleMode
        loadedPrf.looseInitialization = looseInitialization
        loadedPrf.looseClose = looseClose
        loadedPrf.tcpCloseTimeout = tcpCloseTimeout
        loadedPrf.keepAliveInterval = keepAliveInterval
        '''
        if isNeedUpdate(loadedPrf, modContent, defaultsFrom, resetOnTimeout, reassembleFragments, idleTimeout, tcpHandshakeTimeout, tcpTimestampMode, tcpWscaleMode, looseInitialization, looseClose, tcpCloseTimeout, keepAliveInterval):        
            strReturn[str(idx)] = "FastL4 Profile settings have been saved!"
            idx += 1
            
            try:
                #loadedPrf.update()
                loadedPrf.modify(**modContent)
            except Exception as e:
                strReturn[str(idx)] = "Exception fired during FastL4 profile update() (" + prfName + "): " + str(e)
                idx += 1
                logger.info("FastL4 Profile creation exception fired: " + str(e))
                return json.dumps(strReturn)
        else:
            logger.info("No FastL4 Profile modification is needed")
            strReturn[str(idx)] = "No FastL4 Profile modification is needed (" + prfName + "): "
            idx += 1              
    
    if prfDplyOrChg == 'new_profile':
        strReturn[str(idx)] = "FastL4 Profile(" + prfName + ") has been created"
        idx += 1
        logger.info("FastL4  Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "FastL4 Profile Modification(" + prfName + ") has been completed"
        idx += 1
        logger.info("FastL4  Profile Modification has been completed")
        
    for keys, values in strReturn.items():
        logger.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logger.info('main called: param1: ')
    print new_f4Profile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14])
