from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

def check_profileName_conflict(mr, prfName, prfDftFrom):
    srcAffPrfNames = mr.tm.ltm.persistence.source_addrs.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for srcAffPrfName in srcAffPrfNames:
        if srcAffPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  
    
# 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 
# 'timeout', 'mask', 'mapProxies', 'overrideConnectionLimit'		
def new_srcAffProfile_build(active_ltm, prfName, prfDplyOrChg, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, timeout, mask, mapProxies, overrideConnectionLimit):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    output = ''

    logging.info("new_srcAffProfile_build.py Parms \nDevIP: " + active_ltm + "\nProfile name: " + prfName + "\nProfile Deploy or Change: " + prfDplyOrChg + "\nDefaults-from: " + defaultsFrom + "\n") 
    idx = 1

    if prfDplyOrChg == 'new_profile':
        
        logging.info("Profile Creation process has been initiated. Source Address Persistence Profile Name: " + prfName)
        
        strReturn = {str(idx) : 'Source Address Persistence Profile Creation Report'}
        idx += 1
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logging.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logging.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.persistence.source_addrs.source_addr.create(name=prfName, partition='Common', \
                    defaultsFrom=defaultsFrom, matchAcrossServices=matchAcrossServices, matchAcrossVirtuals=matchAcrossVirtuals, \
                    matchAcrossPools=matchAcrossPools, hashAlgorithm=hashAlgorithm, timeout=timeout, mask=mask, mapProxies=mapProxies, \
                    overrideConnectionLimit=overrideConnectionLimit)
        except Exception as e:
            logging.info("Exception during Source Address Persistence Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Source Address Persistence Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile':
        strReturn = {str(idx) : 'Source Address Persistence Profile Modification Report'}
        idx += 1

        logging.info("Profile Modification process has been initiated. Source Address Persistence Profile Name: " + prfName)
            
        # Load Source Affinity profile settings of a given Source Affinity profile name
        try:
            aSrcAffPrf = mr.tm.ltm.persistence.source_addrs.source_addr.load(name=prfName, partition='Common')
        except Exception as e:
            logging.info("Exception during Source Affinity Profile loading")
            strReturn[str(idx)] = "Exception fired during Source Affinity Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during Source Affinity Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # Save the update DNS profile settings
        aSrcAffPrf.defaultsFrom = defaultsFrom
        aSrcAffPrf.matchAcrossServices = matchAcrossServices
        aSrcAffPrf.matchAcrossVirtuals = matchAcrossVirtuals
        aSrcAffPrf.matchAcrossPools = matchAcrossPools
        aSrcAffPrf.hashAlgorithm = hashAlgorithm
        aSrcAffPrf.timeout = timeout
        aSrcAffPrf.mask = mask
        aSrcAffPrf.mapProxies = mapProxies
        aSrcAffPrf.overrideConnectionLimit = overrideConnectionLimit
        
        strReturn[str(idx)] = "Source Affinity Profile settings have been saved!"
        idx += 1
        
        try:
            aSrcAffPrf.update()
        except Exception as e:
            strReturn[str(idx)] = "Exception fired during Source Affinity profile update() (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Source Affinity Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    
    if prfDplyOrChg == 'new_profile':      
        strReturn[str(idx)] = "Source Address Persistence Profile (" + prfName + ") has been created"
        idx += 1
        logging.info("Source Address Persistence Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "Source Address Persistence Profile modification(" + prfName + ") has been completed"
        idx += 1
        logging.info("Source Address Persistence Profile modification has been completed")
        
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_srcAffProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12])
