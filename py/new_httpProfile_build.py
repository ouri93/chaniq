from f5.bigip import ManagementRoot
import sys
import logging
import json

def check_profileName_conflict(mr, prfName, prfPxyType, prfDftFrom):
    httpPrfNames = mr.tm.ltm.profile.https.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for httpPrfName in httpPrfNames:
        if httpPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  
		
def new_httpProfile_build(prfDevIp, prfName, prfDplyOrChg, prfPxyType, prfDftFrom, prfBscAuthRealm, prfFallbackHost, prfFallbackStsCode, prfHdrErase,	prfHdrInsert, prfReqChunking, prfRespChunking, prfInstXFF, prfSrvAgtName):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (dev_ip, pf_type))
	
    # Default value set if no value is given
    if (prfInstXFF == ''):
         prfInstXFF='disabled'
         
         
    mr = ManagementRoot(prfDevIp, 'admin', 'rlatkdcks')
    output = ''

    logging.info("new_httpProfile_build.py Parms DevIP: " + prfDevIp \
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

    mr = ManagementRoot(str(prfDevIp), 'admin', 'rlatkdcks')
	
    idx = 1
    strReturn = {str(idx) : 'Profile Creation Report'}

    idx += 1
    #logging.info("ProxyType before change: " + prfPxyType)
    tmp = prfPxyType.split(":")
    #logging.info("ProxyType after change: tmp[0]: " + tmp[0])
    
    pxyLen = len(tmp)
    prfPxyType = tmp[0]
    if pxyLen == 2:
        dnsRzvName = tmp[1]
        logging.info("ProxyType: " + prfPxyType + " DNS Resolver name: " + dnsRzvName)
    #std_irname = build_std_names.build_std_ir_name(str(irEnv), str(irVsName), str(irVsPort), str(irType))
    logging.info("Profile Creation process has been initiated. Profile Name: " + prfName)

    if check_profileName_conflict(mr, prfName, prfPxyType, prfDftFrom):
        strReturn.update({str(idx) : 'Profile Name conflict'})
        logging.info("Profile name conflict.")
        idx += 1
        return json.dumps(strReturn)
    logging.info("No profile name conflict. Now creating the requested profile")
		
    try:
        new_records = []
        arrRecords = prfFallbackStsCode.split(' ')
        for arrRecord in arrRecords:
            aRecord = arrRecord.split(':')
            logging.info("FallbackStatus Codes: " + arrRecord)
            nr = [str(arrRecord)]
            new_records.extend(nr)
        if prfPxyType == 'explicit':
            proxyDict = {'dnsResolver': '/Common/' + dnsRzvName}
            #logging.info("DNS Resolver Full name: " + proxyDict['dnsResolver'])
            mydg = mr.tm.ltm.profile.https.http.create(name=prfName, partition='Common', proxyType=prfPxyType, defaultsFrom=prfDftFrom, basicAuthRealm=prfBscAuthRealm, fallbackHost=prfFallbackHost, fallbackStatusCodes=new_records, headerErase=prfHdrErase,	headerInsert=prfHdrInsert, requestChunking=prfReqChunking, responseChunking=prfRespChunking, insertXforwardedFor=prfInstXFF, serverAgentName=prfSrvAgtName, explicitProxy=proxyDict)
        else:
            mydg = mr.tm.ltm.profile.https.http.create(name=prfName, partition='Common', proxyType=prfPxyType, defaultsFrom=prfDftFrom, basicAuthRealm=prfBscAuthRealm, fallbackHost=prfFallbackHost, fallbackStatusCodes=new_records, headerErase=prfHdrErase, headerInsert=prfHdrInsert, requestChunking=prfReqChunking, responseChunking=prfRespChunking, insertXforwardedFor=prfInstXFF, serverAgentName=prfSrvAgtName)
    except Exception as e:
        logging.info("Exception during Profile creation")
        strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
        idx += 1
        logging.info("Profile creation exception fired: " + str(e))
        return json.dumps(strReturn)

    strReturn[str(idx)] = "HTTP Profile (" + prfName + ") has been created"
    idx += 1
    logging.info("HTTP Profile has been created")

    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_httpProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14])
