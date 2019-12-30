from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass
import loadStdNames

def check_profileName_conflict(mr, prfName, prfDftFrom):
    srvsslPrfNames = mr.tm.ltm.profile.server_ssls.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for srvsslPrfName in srvsslPrfNames:
        if srvsslPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  
		
def new_srvsslProfile_build(active_ltm, prfName, prfDplyOrChg, defaultsFrom, cert, key, chain, ciphers, proxySsl, proxySslPassthrough, renegotiation, renegotiatePeriod, renegotiateSize, secureRenegotiation, serverName, sniDefault, sniRequire):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (dev_ip, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    output = ''

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logging.info("new_srvsslProfile_build()- Use Standard Global naming : " + useGlobalNaming )
    
    logging.info("new_srvsslProfile_build.py Parms DevIP: " + active_ltm + " Profile name: " + prfName + " Profile Deploy or Change: " + prfDplyOrChg + " Defaults-from: " + defaultsFrom) 
    idx = 1

    if prfDplyOrChg == 'new_profile':
        strReturn = {str(idx) : 'ServerSSL Profile Creation Report'}
        idx += 1

        if useGlobalNaming == '1':
            prfName = loadStdNames.get_std_name(active_ltm, 'SHARED', 'PROFILE', 'SERVERSSL', prfName)
                
        logging.info("Profile Creation process has been initiated. ServerSSL Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logging.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logging.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.profile.server_ssls.server_ssl.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, cert=cert, \
                   key=key, chain=chain, ciphers=ciphers, proxySsl=proxySsl, proxySslPassthrough=proxySslPassthrough, renegotiation=renegotiation, \
                   renegotiatePeriod=renegotiatePeriod, renegotiateSize=renegotiateSize, secureRenegotiation=secureRenegotiation, serverName=serverName, \
                   sniDefault=sniDefault, sniRequire=sniRequire)
        except Exception as e:
            logging.info("Exception during ServerSSL Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("ServerSSL Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile':
        strReturn = {str(idx) : 'ServerSSL Profile Modification Report'}
        idx += 1
    
        logging.info("Profile Modification process has been initiated. ServerSSL Profile Name: " + prfName)
        
        # Load Server SSL profile settings of a given Server SSL profile name
        #  'defaultsFrom','cert', 'key', 'chain', 'ciphers', 'proxySsl',
        #  'proxySslPassthrough', 'renegotiation', 'renegotiatePeriod',
        #  'renegotiateSize', 'secureRenegotiation', 'serverName', 'sniDefault',
        ## 'sniRequire'  
        try:
            aSrvsslPrf = mr.tm.ltm.profile.server_ssls.server_ssl.load(name=prfName, partition='Common')
        except Exception as e:
            logging.info("Exception during Server SSL Profile loading")
            strReturn[str(idx)] = "Exception fired during Server SSL Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during Server SSL Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # Save the update Server SSL profile settings
        aSrvsslPrf.defaultsFrom = defaultsFrom
        aSrvsslPrf.cert = cert
        aSrvsslPrf.key = key
        aSrvsslPrf.chain = chain
        aSrvsslPrf.ciphers = ciphers
        aSrvsslPrf.proxySsl = proxySsl
        aSrvsslPrf.proxySslPassthrough = proxySslPassthrough
        aSrvsslPrf.renegotiation = renegotiation
        aSrvsslPrf.renegotiatePeriod = renegotiatePeriod
        aSrvsslPrf.renegotiateSize = renegotiateSize
        aSrvsslPrf.renegotiateMaxRecordDelay = renegotiateMaxRecordDelay
        aSrvsslPrf.secureRenegotiation = secureRenegotiation
        aSrvsslPrf.serverName = serverName
        aSrvsslPrf.sniDefault = sniDefault
        aSrvsslPrf.sniRequire = sniRequire        
                
        strReturn[str(idx)] = "Server SSL Profile settings have been saved!"
        idx += 1
        
        try:
            aSrvsslPrf.update()
        except Exception as e:
            strReturn[str(idx)] = "Exception fired during Server SSL profile update() (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Server SSL Profile Modification exception fired: " + str(e))
            return json.dumps(strReturn)
        
    if prfDplyOrChg == 'new_profile':        
        strReturn[str(idx)] = "ServerSSL Profile (" + prfName + ") has been created"
        idx += 1
        logging.info("ServerSSL Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "ServerSSL Profile Modification(" + prfName + ") has been completed"
        idx += 1
        logging.info("ServerSSL Profile Modification has been completed")
    
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_srvsslProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14], sys.argv[15], sys.argv[16], sys.argv[17])
