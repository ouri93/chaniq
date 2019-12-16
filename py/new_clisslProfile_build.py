from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

def check_profileName_conflict(mr, prfName, prfDftFrom):
    clisslPrfNames = mr.tm.ltm.profile.client_ssls.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for clisslPrfName in clisslPrfNames:
        if clisslPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

def new_clisslProfile_build(active_ltm, prfName, prfDplyOrChg, defaultsFrom, cert, key, chain, ciphers, proxySsl, proxySslPassthrough, renegotiation, renegotiatePeriod, renegotiateSize, renegotiateMaxRecordDelay, secureRenegotiation, maxRenegotiationsPerMinute, serverName, sniDefault, sniRequire):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    output = ''

    logging.info("new_clisslProfile_build.py Parms DevIP: " + active_ltm + " Profile name: " + prfName + " Profile Deploy or Change: " + prfDplyOrChg + " Defaults-from: " + defaultsFrom) 
    idx = 1

    if prfDplyOrChg == 'new_profile':
        strReturn = {str(idx) : 'ClientSSL Profile Creation Report'}
        idx += 1
    
        logging.info("Profile Creation process has been initiated. ClientSSL Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logging.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logging.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.profile.client_ssls.client_ssl.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, cert=cert, key=key, \
                    chain=chain, ciphers=ciphers, proxySsl=proxySsl, proxySslPassthrough=proxySslPassthrough, renegotiation=renegotiation, \
                    renegotiatePeriod=renegotiatePeriod, renegotiateSize=renegotiateSize, renegotiateMaxRecordDelay=renegotiateMaxRecordDelay, secureRenegotiation=secureRenegotiation, \
                    maxRenegotiationsPerMinute=maxRenegotiationsPerMinute, serverName=serverName, sniDefault=sniDefault, sniRequire=sniRequire)
        except Exception as e:
            logging.info("Exception during ClientSSL Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("ClientSSL Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile':
        strReturn = {str(idx) : 'ClientSSL Profile Modification Report'}
        idx += 1
    
        logging.info("Profile Modification process has been initiated. ClientSSL Profile Name: " + prfName)
        
        # Load Client SSL profile settings of a given Client SSL profile name
        #  'defaultsFrom', 'cert', 'key', 'chain', 'ciphers', 'proxySsl', 'proxySslPassthrough',
        #  'renegotiation', 'renegotiatePeriod', 'renegotiateSize', 'renegotiateMaxRecordDelay',
        #  'secureRenegotiation', 'maxRenegotiationsPerMinute', 'serverName', 'sniDefault',
        #  'sniRequire'    
        try:
            aClisslPrf = mr.tm.ltm.profile.client_ssls.client_ssl.load(name=prfName, partition='Common')
        except Exception as e:
            logging.info("Exception during Client SSL Profile loading")
            strReturn[str(idx)] = "Exception fired during Client SSL Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during Client SSL Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # Save the update Client SSL profile settings
        aClisslPrf.defaultsFrom = defaultsFrom
        aClisslPrf.cert = cert
        aClisslPrf.key = key
        aClisslPrf.chain = chain
        aClisslPrf.ciphers = ciphers
        aClisslPrf.proxySsl = proxySsl
        aClisslPrf.proxySslPassthrough = proxySslPassthrough
        aClisslPrf.renegotiation = renegotiation
        aClisslPrf.renegotiatePeriod = renegotiatePeriod
        aClisslPrf.renegotiateSize = renegotiateSize
        aClisslPrf.renegotiateMaxRecordDelay = renegotiateMaxRecordDelay
        aClisslPrf.secureRenegotiation = secureRenegotiation
        aClisslPrf.maxRenegotiationsPerMinute = maxRenegotiationsPerMinute
        aClisslPrf.serverName = serverName
        aClisslPrf.sniDefault = sniDefault
        aClisslPrf.sniRequire = sniRequire        
                
        strReturn[str(idx)] = "Client SSL Profile settings have been saved!"
        idx += 1
        
        try:
            aClisslPrf.update()
        except Exception as e:
            strReturn[str(idx)] = "Exception fired during Client SSL profile update() (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Client SSL Profile Modification exception fired: " + str(e))
            return json.dumps(strReturn)
    if prfDplyOrChg == 'new_profile':                
        strReturn[str(idx)] = "ClientSSL Profile (" + prfName + ") has been created"
        idx += 1
        logging.info("ClientSSL Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "ClientSSL Profile Modification(" + prfName + ") has been completed"
        idx += 1
        logging.info("ClientSSL Profile Modification has been completed")

    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_clisslProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14], sys.argv[15], sys.argv[16], sys.argv[17], sys.argv[18], sys.argv[19])
