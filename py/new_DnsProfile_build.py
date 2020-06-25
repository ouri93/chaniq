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
    dnsPrfNames = mr.tm.ltm.profile.dns_s.get_collection()
    logger.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for httpPrfName in dnsPrfNames:
        if httpPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logger.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

def isNeedUpdate(loadedPrf, modContent, prfDftFrom, prfHwValid, prfHwRespCache, prfDnsExp, prfGtm, prfUnhandledAct, prfUseBind, prfZoneXfr, prfDnsSecurity, prfRecursion):
    cnt = 0
    # Set HTTP profile values
    # # Issue Track: #1
    if chaniq_util.isStrPropModified(loadedPrf, 'defaultsFrom', prfDftFrom):
        modContent['proxyType'] = prfDftFrom
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'enableHardwareQueryValidation', prfHwValid):
        modContent['enableHardwareQueryValidation'] = prfHwValid
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'enableHardwareResponseCache', prfHwRespCache):
        modContent['enableHardwareResponseCache'] = prfHwRespCache
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'enableDnsExpress', prfDnsExp):
        modContent['enableDnsExpress'] = prfDnsExp
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'enableGtm', prfGtm):
        modContent['enableGtm'] = prfGtm
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'unhandledQueryAction', prfUnhandledAct):
        modContent['unhandledQueryAction'] = prfUnhandledAct
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'useLocalBind', prfUseBind):
        modContent['useLocalBind'] = prfUseBind
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'processXfr', prfZoneXfr):
        modContent['processXfr'] = prfZoneXfr
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'enableDnsFirewall', prfDnsSecurity):
        modContent['enableDnsFirewall'] = prfDnsSecurity
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'processRd', prfRecursion):
        modContent['processRd'] = prfRecursion
        cnt = cnt + 1

    if cnt > 0: return True
    else: return False
                		
def new_DnsProfile_build(active_ltm, prfName, prfDplyOrChg, prfDftFrom, prfHwValid, prfHwRespCache, prfDnsExp, prfGtm, prfUnhandledAct, prfUseBind, prfZoneXfr, prfDnsSecurity, prfRecursion):
    #logger.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    output = ''

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logger.info("new_DnsProfile_build()- Use Standard Global naming : " + useGlobalNaming )

    logger.info("new_DnsProfile_build.py Parms \nDevIP: " + active_ltm + "\nProfile name: " + prfName + "\nProfile Deploy or Change: " + prfDplyOrChg + "\nDefaults-from: " + prfDftFrom) 

    idx = 1
    
    #logger.info("ProxyType before change: " + prfPxyType)
    if prfDplyOrChg == 'new_profile':    
        strReturn = {str(idx) : 'DNS Profile Creation Report'}

        idx += 1

        if useGlobalNaming == '1':
            prfName = loadStdNames.get_std_name(active_ltm, 'SHARED', 'PROFILE', 'SERVICE_DNS', prfName)    
            
        logger.info("Profile Creation process has been initiated. Profile Name: " + prfName + "\n")
    
        if check_profileName_conflict(mr, prfName, prfDftFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logger.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logger.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.profile.dns_s.dns.create(name=prfName, partition='Common', defaultsFrom=prfDftFrom, enableHardwareQueryValidation=prfHwValid, enableHardwareResponseCache=prfHwRespCache, enableDnsExpress=prfDnsExp, enableGtm=prfGtm, unhandledQueryAction=prfUnhandledAct , useLocalBind=prfUseBind, processXfr=prfZoneXfr, enableDnsFirewall=prfDnsSecurity, processRd=prfRecursion)
        except Exception as e:
            logger.info("Exception during DNS Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logger.info("DNS Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    
        strReturn[str(idx)] = "DNS Profile (" + prfName + ") has been created"
        idx += 1
        logger.info("DNS Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        modContent = {}        
        strReturn = {str(idx) : 'DNS Profile Modification Report'}

        idx += 1
        
        logger.info("Profile Modification process has been initiated. Profile Name: " + prfName + "\n")
        
        # Load DNS profile settings of a given DNS profile name
        try:
            loadedPrf = mr.tm.ltm.profile.dns_s.dns.load(name=prfName, partition='Common')
        except Exception as e:
            logger.info("Exception during DNS Profile loading")
            strReturn[str(idx)] = "Exception fired during DNS Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logger.info("Exception fired during DNS Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # Save the update DNS profile settings
        '''
        loadedPrf.defaultsFrom = prfDftFrom
        loadedPrf.enableHardwareQueryValidation = prfHwValid
        loadedPrf.enableHardwareResponseCache = prfHwRespCache
        loadedPrf.enableDnsExpress = prfDnsExp
        loadedPrf.enableGtm = prfGtm
        loadedPrf.unhandledQueryAction = prfUnhandledAct
        loadedPrf.useLocalBind = prfUseBind
        loadedPrf.processXfr = prfZoneXfr
        loadedPrf.enableDnsFirewall = prfDnsSecurity
        loadedPrf.processRd = prfRecursion
        '''
        
        if isNeedUpdate(loadedPrf, modContent, prfDftFrom, prfHwValid, prfHwRespCache, prfDnsExp, prfGtm, prfUnhandledAct, prfUseBind, prfZoneXfr, prfDnsSecurity, prfRecursion):

            strReturn[str(idx)] = "DNS Profile settings have been saved!"
            idx += 1
            
            try:
                #loadedPrf.update()
                loadedPrf.modify(**modContent)
            except Exception as e:
                strReturn[str(idx)] = "Exception fired during DNS profile update() (" + prfName + "): " + str(e)
                idx += 1
                logger.info("DNS Profile creation exception fired: " + str(e))
                return json.dumps(strReturn)
        else:
            logger.info("No DNS Profile modification is needed")
            strReturn[str(idx)] = "No DNS Profile modification is needed (" + prfName + "): "
            idx += 1
            
    if prfDplyOrChg == 'new_profile': 
        strReturn[str(idx)] = "DNS Profile (" + prfName + ") has been created"
        idx += 1
        logger.info("DNS Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "DNS Profile modification has been completed"
        idx += 1
        logger.info("DNS Profile modification has been completed")
        
    for keys, values in strReturn.items():
        logger.info("Key: " + keys + " Value: " + values)
        
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logger.info('main called: param1: ')
    print new_DnsProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13])
