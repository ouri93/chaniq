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
    udpPrfNames = mr.tm.ltm.profile.udps.get_collection()
    logger.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for udpPrfName in udpPrfNames:
        if udpPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logger.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

def isNeedUpdate(loadedPrf, modContent, defaultsFrom, proxyMss, idleTimeout, ipTosToClient, linkQosToClient, datagramLoadBalancing, allowNoPayload, ipTtlMode, ipTtlV4, ipTtlV6, ipDfMode):
    cnt = 0

    if chaniq_util.isStrPropModified(loadedPrf, 'defaultsFrom', defaultsFrom):
        modContent['defaultsFrom'] = defaultsFrom
        cnt = cnt + 1  
    if chaniq_util.isIntPropModified(loadedPrf, 'ipTtlV4', ipTtlV4, 255):
        modContent['ipTtlV4'] = ipTtlV4
        cnt = cnt + 1  
    if chaniq_util.isIntPropModified(loadedPrf, 'ipTtlV6', ipTtlV6, 64):
        modContent['ipTtlV6'] = ipTtlV6
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'proxyMss', proxyMss):
        modContent['proxyMss'] = proxyMss
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'idleTimeout', idleTimeout):
        modContent['idleTimeout'] = idleTimeout
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'ipTosToClient', ipTosToClient):
        modContent['ipTosToClient'] = ipTosToClient
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'linkQosToClient', linkQosToClient):
        modContent['linkQosToClient'] = linkQosToClient
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'datagramLoadBalancing', datagramLoadBalancing):
        modContent['datagramLoadBalancing'] = datagramLoadBalancing
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'allowNoPayload', allowNoPayload):
        modContent['allowNoPayload'] = allowNoPayload
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'ipTtlMode', ipTtlMode):
        modContent['ipTtlMode'] = ipTtlMode
        cnt = cnt + 1  
    if chaniq_util.isStrPropModified(loadedPrf, 'ipDfMode', ipDfMode):
        modContent['ipDfMode'] = ipDfMode
        cnt = cnt + 1  

    if cnt > 0: return True
    else: return False    
    

#  'defaultsFrom', 'proxyMss', 'idleTimeout', 'ipTosToClient', 'linkQosToClient',
#  'datagramLoadBalancing', 'allowNoPayload', 'ipDfMode', 'ipTtlV4', 'ipTtlV6',
#  'ipDfMode'		
def new_udpProfile_build(active_ltm, prfName, prfDplyOrChg, defaultsFrom, proxyMss, idleTimeout, ipTosToClient, linkQosToClient, datagramLoadBalancing, allowNoPayload, ipTtlMode, ipTtlV4, ipTtlV6, ipDfMode):

    #logger.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    output = ''

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logger.info("new_udpProfile_build()- Use Standard Global naming : " + useGlobalNaming )
    
    logger.info("new_udpProfile_build.py Parms DevIP: " + active_ltm + " Profile name: " + prfName + " Profile Deploy or Change: " + prfDplyOrChg + " Defaults-from: " + defaultsFrom) 
    idx = 1
    if prfDplyOrChg == 'new_profile':
        strReturn = {str(idx) : 'UDP Profile Creation Report'}
    
        idx += 1

        if useGlobalNaming == '1':
            prfName = loadStdNames.get_std_name(active_ltm, 'SHARED', 'PROFILE', 'UDP_PROTOCOL', prfName)
                
        logger.info("Profile Creation process has been initiated. UDP Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logger.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logger.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.profile.udps.udp.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, proxyMss=proxyMss, idleTimeout=idleTimeout, ipTosToClient=ipTosToClient, linkQosToClient=linkQosToClient, datagramLoadBalancing=datagramLoadBalancing, allowNoPayload=allowNoPayload, ipTtlMode=ipTtlMode, ipTtlV4=ipTtlV4, ipTtlV6=ipTtlV6, ipDfMode=ipDfMode)
        except Exception as e:
            logger.info("Exception during UDP Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logger.info("UDP Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile': 
        
        modContent = {}
        
        strReturn = {str(idx) : 'UDP Profile Creation Report'}
        idx += 1
    
        logger.info("Profile Modification process has been initiated. UDP Profile Name: " + prfName)
        
        # Load UDP profile settings of a given UDP profile name
        #  'defaultsFrom', 'proxyMss', 'idleTimeout', 'ipTosToClient', 'linkQosToClient',
        #  'datagramLoadBalancing', 'allowNoPayload', 'ipDfMode', 'ipTtlV4', 'ipTtlV6',
        #  'ipDfMode'  
        try:
            loadedPrf = mr.tm.ltm.profile.udps.udp.load(name=prfName, partition='Common')
        except Exception as e:
            logger.info("Exception during UDP Profile loading")
            strReturn[str(idx)] = "Exception fired during UDP Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logger.info("Exception fired during UDP Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # Save the update UDP profile settings
        '''
        loadedPrf.defaultsFrom = defaultsFrom
        loadedPrf.proxyMss = proxyMss
        loadedPrf.idleTimeout = idleTimeout
        loadedPrf.ipTosToClient = ipTosToClient
        loadedPrf.linkQosToClient = linkQosToClient
        loadedPrf.datagramLoadBalancing = datagramLoadBalancing
        loadedPrf.allowNoPayload = allowNoPayload
        loadedPrf.ipDfMode = ipDfMode
        loadedPrf.ipTtlV4 = ipTtlV4
        loadedPrf.ipTtlV6 = ipTtlV6
        loadedPrf.ipDfMode = ipDfMode
        '''
                
        if isNeedUpdate(loadedPrf, modContent, defaultsFrom, proxyMss, idleTimeout, ipTosToClient, linkQosToClient, datagramLoadBalancing, allowNoPayload, ipTtlMode, ipTtlV4, ipTtlV6, ipDfMode):
            strReturn[str(idx)] = "UDP Profile settings have been saved!"
            idx += 1
            
            try:
                #loadedPrf.update()
                loadedPrf.modify(**modContent)
            except Exception as e:
                strReturn[str(idx)] = "Exception fired during UDP profile update() (" + prfName + "): " + str(e)
                idx += 1
                logger.info("UDP Profile creation exception fired: " + str(e))
                return json.dumps(strReturn)
        else:
            logger.info("No UDP Profile modification is needed")
            strReturn[str(idx)] = "No UDP Profile modification is needed (" + prfName + "): "
            idx += 1      
                        
    if prfDplyOrChg == 'new_profile':
        strReturn[str(idx)] = "UDP Profile (" + prfName + ") has been created"
        idx += 1
        logger.info("UDP Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "UDP Profile Modification(" + prfName + ") has been completed"
        idx += 1
        logger.info("UDP Profile Modification has been completed")

    for keys, values in strReturn.items():
        logger.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logger.info('main called: param1: ')
    print new_udpProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14])
