from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

def check_profileName_conflict(mr, prfName, prfDftFrom):
    sslPrfNames = mr.tm.ltm.persistence.ssls.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for sslPrfName in sslPrfNames:
        if sslPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

# 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools', 'timeout', 'overrideConnectionLimit'		
def new_sslProfile_build(active_ltm, prfName, prfDplyOrChg, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, timeout, overrideConnectionLimit):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    output = ''

    logging.info("new_sslProfile_build.py Parms \nDevIP: " + active_ltm + "\nProfile name: " + prfName + "\nProfile Deploy or Change: " + prfDplyOrChg + "\nDefaults-from: " + defaultsFrom + "\n") 

    idx = 1
    
    if prfDplyOrChg == 'new_profile':     
        strReturn = {str(idx) : 'SSL Persistence Profile Creation Report'}
    
        idx += 1
    
        logging.info("Profile Creation process has been initiated. SSL Persistence Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logging.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logging.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.persistence.ssls.ssl.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, matchAcrossServices=matchAcrossServices, matchAcrossVirtuals=matchAcrossVirtuals, matchAcrossPools=matchAcrossPools, timeout=timeout, overrideConnectionLimit=overrideConnectionLimit)
        except Exception as e:
            logging.info("Exception during SSL Persistence Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("SSL Persistence Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile':
        strReturn = {str(idx) : 'SSL Persistence Profile Modification Report'}
        idx += 1
    
        logging.info("Profile Modification process has been initiated. SSL Persistence Profile Name: " + prfName)
        
        # Load SSL Persistence profile settings of a given Hash profile name
        try:
            aSSLPrf = mr.tm.ltm.persistence.ssls.ssl.load(name=prfName, partition='Common')
        except Exception as e:
            logging.info("Exception during SSL Persistence Profile loading")
            strReturn[str(idx)] = "Exception fired during SSL Persistence Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during SSL Persistence Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools', 'timeout', 'overrideConnectionLimit'
        aSSLPrf.defaultsFrom = defaultsFrom
        aSSLPrf.matchAcrossServices = matchAcrossServices
        aSSLPrf.matchAcrossVirtuals = matchAcrossVirtuals
        aSSLPrf.matchAcrossPools = matchAcrossPools
        aSSLPrf.timeout = timeout
        aSSLPrf.overrideConnectionLimit = overrideConnectionLimit
        
        strReturn[str(idx)] = "SSL Persistence Profile settings have been saved!"
        idx += 1
        
        try:
            aSSLPrf.update()
        except Exception as e:
            strReturn[str(idx)] = "Exception fired during SSL Persistence profile update() (" + prfName + "): " + str(e)
            idx += 1
            logging.info("SSL Persistence Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    
    if prfDplyOrChg == 'new_profile': 
        strReturn[str(idx)] = "SSL Persistence Profile (" + prfName + ") has been created"
        idx += 1
        logging.info("SSL Persistence Profile has been created")
    elif prfDplyOrChg == 'chg_profile': 
        strReturn[str(idx)] = "SSL Persistence Profile Modification(" + prfName + ") has been completed."
        idx += 1
        logging.info("SSL Persistence Profile modification has been completed.")

        
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_sslProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])
