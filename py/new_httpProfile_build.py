from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass
import loadStdNames
import chaniq_util
from __builtin__ import True, False
from pickle import TRUE

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def check_profileName_conflict(mr, prfName, prfPxyType, prfDftFrom):
    httpPrfNames = mr.tm.ltm.profile.https.get_collection()
    logger.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for httpPrfName in httpPrfNames:
        if httpPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logger.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False

# Check if update is needed
#         
def isNeedUpdate(loadedPrf, modContent, prfPxyType, prfDftFrom, prfBscAuthRealm, prfFallbackHost, prfFallbackStsCode, prfHdrErase, prfHdrInsert, prfReqChunking, prfRespChunking, prfInstXFF, prfSrvAgtName):
    cnt = 0
    # Set HTTP profile values
    # # Issue Track: #1
    if chaniq_util.isStrPropModified(loadedPrf, 'proxyType', prfPxyType):
        modContent['proxyType'] = prfPxyType
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'defaultsFrom', prfDftFrom):
        modContent['defaultsFrom'] = prfDftFrom
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'basicAuthRealm', prfBscAuthRealm):
        modContent['basicAuthRealm'] = prfBscAuthRealm
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'fallbackHost', prfFallbackHost):
        modContent['fallbackHost'] = prfFallbackHost
        cnt = cnt + 1
    
    new_records = []
    arrRecords = prfFallbackStsCode.split(' ')
    for arrRecord in arrRecords:
        aRecord = arrRecord.split(':')
        logger.info("FallbackStatus Codes: " + arrRecord)
        nr = [str(arrRecord)]
        new_records.extend(nr)
    
    if chaniq_util.isListPropModified(loadedPrf, 'fallbackStatusCodes', new_records):
        modContent['fallbackStatusCodes'] = arrRecords
        cnt = cnt + 1
    
    if chaniq_util.isStrPropModified(loadedPrf, 'headerErase', prfHdrErase):
        modContent['headerErase'] = prfHdrErase
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'headerInsert', prfHdrInsert):
        modContent['headerInsert'] = prfHdrInsert
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'requestChunking', prfReqChunking):
        modContent['requestChunking'] = prfReqChunking
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'responseChunking', prfRespChunking):
        modContent['responseChunking'] = prfRespChunking
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'insertXforwardedFor', prfInstXFF):
        modContent['insertXforwardedFor'] = prfInstXFF
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'serverAgentName', prfSrvAgtName):
        modContent['serverAgentName'] = prfSrvAgtName
        cnt = cnt + 1
        
    if cnt > 0: return True
    else: return False
		
def new_httpProfile_build(active_ltm, prfName, prfDplyOrChg, prfPxyType, prfDftFrom, prfBscAuthRealm, prfFallbackHost, prfFallbackStsCode, prfHdrErase,	prfHdrInsert, prfReqChunking, prfRespChunking, prfInstXFF, prfSrvAgtName):
    #logger.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
    # Default value set if no value is given
    if (prfInstXFF == ''):
         prfInstXFF='disabled'
         
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    output = ''

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logger.info("new_httpProfile_build()- Use Standard Global naming : " + useGlobalNaming )
    
    logger.info("new_httpProfile_build.py Parms DevIP: " + active_ltm \
                 + " Profile name: " + prfName \
                 + " Defaults-from: " + prfDftFrom \
                 + " Profile Proxy Type: " + prfPxyType \
                 + " Profile Deploy or Change: " + prfDplyOrChg \
                 + " Basic Auth Realm: " + prfBscAuthRealm \
                 + " Fallback Host: " + prfFallbackHost \
                 + " Fallback on Error Codes: " + prfFallbackStsCode \
                 + " Request Header Erase: " + prfHdrErase \
                 + " Request Header Insert: " + prfHdrInsert \
                 + " Request Chunking: " + prfReqChunking \
                 + " Response Chunking: " + prfRespChunking \
                 + " Inser X-forwared-for: " + prfInstXFF \
                 + " Server Agent name: " + prfSrvAgtName ) 

    	
    # Process to build new HTTP profile
    if prfDplyOrChg == 'new_profile':
        logger.info("Profile Creation process has been initiated. Profile Name: " + prfName)
        
        idx = 1
        strReturn = {str(idx) : 'Profile Creation Report'}
    
        idx += 1
        #logger.info("ProxyType before change: " + prfPxyType)
        #prfPxyType has 'explicit:DNS_Resolver_name' format if HTTP proxy type is 'explicit'
        tmp = prfPxyType.split(":")
        #logger.info("ProxyType after change: tmp[0]: " + tmp[0])
        
        pxyLen = len(tmp)
        prfPxyType = tmp[0]
        # Only HTTP Explict Proxy type has the length of 2 ('explicit' and 'DNS_Resolver_name')
        if pxyLen == 2:
            dnsRzvName = tmp[1]
            logger.info("ProxyType: " + prfPxyType + " DNS Resolver name: " + dnsRzvName)
        #std_irname = build_std_names.build_std_ir_name(str(irEnv), str(irVsName), str(irVsPort), str(irType))

        if useGlobalNaming == '1':
            prfName = loadStdNames.get_std_name(active_ltm, 'SHARED', 'PROFILE', 'SERVICE_HTTP', prfName)
                
        if check_profileName_conflict(mr, prfName, prfPxyType, prfDftFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logger.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logger.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            new_records = []
            arrRecords = prfFallbackStsCode.split(' ')
            for arrRecord in arrRecords:
                aRecord = arrRecord.split(':')
                logger.info("FallbackStatus Codes: " + arrRecord)
                nr = [str(arrRecord)]
                new_records.extend(nr)
            if prfPxyType == 'explicit':
                proxyDict = {'dnsResolver': '/Common/' + dnsRzvName}
                #logger.info("DNS Resolver Full name: " + proxyDict['dnsResolver'])
                mydg = mr.tm.ltm.profile.https.http.create(name=prfName, partition='Common', proxyType=prfPxyType, defaultsFrom=prfDftFrom, basicAuthRealm=prfBscAuthRealm, fallbackHost=prfFallbackHost, fallbackStatusCodes=new_records, headerErase=prfHdrErase,	headerInsert=prfHdrInsert, requestChunking=prfReqChunking, responseChunking=prfRespChunking, insertXforwardedFor=prfInstXFF, serverAgentName=prfSrvAgtName, explicitProxy=proxyDict)
            else:
                mydg = mr.tm.ltm.profile.https.http.create(name=prfName, partition='Common', proxyType=prfPxyType, defaultsFrom=prfDftFrom, basicAuthRealm=prfBscAuthRealm, fallbackHost=prfFallbackHost, fallbackStatusCodes=new_records, headerErase=prfHdrErase, headerInsert=prfHdrInsert, requestChunking=prfReqChunking, responseChunking=prfRespChunking, insertXforwardedFor=prfInstXFF, serverAgentName=prfSrvAgtName)
        except Exception as e:
            logger.info("Exception during Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logger.info("Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    # Process to change an existing HTTP profile
    else:
        # modContent dictionary is used with modify(**modContent) to update only specified values
        # Issue Track: #1
        modContent = {}
        logger.info("HTTP profile modification process has been initiated. Profile Name: " + prfName)
        
        idx = 1
        strReturn = {str(idx) : 'Profile Modification Report'}
    
        idx += 1
        logger.info("ProxyType before change: " + prfPxyType)
        tmp = prfPxyType.split(":")
        logger.info("ProxyType after change: tmp[0]: " + tmp[0])

        try:
            # Loading profile of a given profile name
            loadedPrf = mr.tm.ltm.profile.https.http.load(name=prfName, partition='Common')
        except Exception as e:
            logger.info("Exception during loading HTTP Profile" + prfName)
            strReturn[str(idx)] = "HTTP Profile Loading Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            return json.dumps(strReturn)
        
        pxyLen = len(tmp)
        prfPxyType = tmp[0]
        if pxyLen == 2:
            dnsRzvName = tmp[1]
            logger.info("ProxyType: " + prfPxyType + " DNS Resolver name: " + dnsRzvName)

        if prfPxyType == 'explicit':
            proxyDict = {'dnsResolver': dnsRzvName}
            # loadedPrf.explicitProxy = proxyDict - Issue Track: #1
            modContent['explicitProxy'] = proxyDict
        
        '''
        # Set HTTP profile values
        # # Issue Track: #1
        #loadedPrf.proxyType = prfPxyType
        #loadedPrf.defaultsFrom = prfDftFrom
        #loadedPrf.basicAuthRealm = prfBscAuthRealm
        #loadedPrf.fallbackHost = prfFallbackHost
        modContent['proxyType'] = prfPxyType
        modContent['defaultsFrom'] = prfDftFrom
        modContent['basicAuthRealm'] = prfBscAuthRealm
        modContent['fallbackHost'] = prfFallbackHost
        
        new_records = []
        arrRecords = prfFallbackStsCode.split(' ')
        for arrRecord in arrRecords:
            aRecord = arrRecord.split(':')
            logger.info("FallbackStatus Codes: " + arrRecord)
            nr = [str(arrRecord)]
            new_records.extend(nr)
        
        # # Issue Track: #1    
        #loadedPrf.fallbackStatusCodes = arrRecords
        #loadedPrf.headerErase = prfHdrErase
        #loadedPrf.headerInsert = prfHdrInsert
        #loadedPrf.requestChunking = prfReqChunking
        #loadedPrf.responseChunking = prfRespChunking
        #loadedPrf.insertXforwardedFor = prfInstXFF
        #loadedPrf.serverAgentName = prfSrvAgtName

        modContent['fallbackStatusCodes'] = arrRecords
        modContent['headerErase'] = prfHdrErase
        modContent['headerInsert'] = prfHdrInsert
        modContent['requestChunking'] = prfReqChunking
        modContent['responseChunking'] = prfRespChunking
        modContent['insertXforwardedFor'] = prfInstXFF
        modContent['serverAgentName'] = prfSrvAgtName        
        '''

        # Issue Track: #1
        # Found which values have been modified
        if isNeedUpdate(loadedPrf, modContent, prfPxyType, prfDftFrom, prfBscAuthRealm, prfFallbackHost, prfFallbackStsCode, prfHdrErase, prfHdrInsert, prfReqChunking, prfRespChunking, prfInstXFF, prfSrvAgtName):    
                
            # Update HTTP profile        
            try:
                # # Issue Track: #1 
                #loadedPrf.update()
                loadedPrf.modify(**modContent)
            except Exception as e:
                logger.info("Exception during updating HTTP Profile modification")
                strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
                idx += 1
                logger.info("HTTP Profile modificaiton creation Exception fired: " + str(e))
                return json.dumps(strReturn)
        else:
            logger.info("No HTTP Profile modification is needed")
            strReturn[str(idx)] = "No HTTP Profile modification is needed (" + prfName + "): "
            idx += 1
        
    if prfDplyOrChg == 'new_profile':
        strReturn[str(idx)] = "HTTP Profile (" + prfName + ") has been created"
        logger.info("HTTP Profile has been created")
    else:
        strReturn[str(idx)] = "Modifying HTTP Profile (" + prfName + ") has been completed"
        logger.info("HTTP Profile modification has been completed")

    idx += 1

    for keys, values in strReturn.items():
        logger.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logger.info('main called: param1: ')
    print new_httpProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14])
