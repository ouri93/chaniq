from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass
import loadStdNames
import chaniq_util

def check_profileName_conflict(mr, prfName, prfDftFrom):
    logging.info("In check_profileName_conflict()\n")
    dstAffPrfNames = mr.tm.ltm.persistence.dest_addrs.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for dstAffPrfName in dstAffPrfNames:
        if dstAffPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  
def isNeedUpdate(loadedPrf, modContent, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, timeout, mask, overrideConnectionLimit):
    cnt = 0

    if chaniq_util.isStrPropModified(loadedPrf, 'defaultsFrom', defaultsFrom):
        modContent['defaultsFrom'] = defaultsFrom
        cnt = cnt + 1
    if chaniq_util.isStrPropModified(loadedPrf, 'matchAcrossServices', matchAcrossServices):
        modContent['matchAcrossServices'] = matchAcrossServices
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'matchAcrossVirtuals', matchAcrossVirtuals):
        modContent['matchAcrossVirtuals'] = matchAcrossVirtuals
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'matchAcrossPools', matchAcrossPools):
        modContent['matchAcrossPools'] = matchAcrossPools
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'hashAlgorithm', hashAlgorithm):
        modContent['hashAlgorithm'] = hashAlgorithm
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'timeout', timeout):
        modContent['timeout'] = timeout
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'mask', mask):
        modContent['mask'] = mask
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'overrideConnectionLimit', overrideConnectionLimit):
        modContent['overrideConnectionLimit'] = overrideConnectionLimit
        cnt = cnt + 1     
        
    if cnt > 0: return True
    else: return False
        		
def new_dstAffProfile_build(prfDevIp, prfName, prfDplyOrChg, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, timeout, mask, overrideConnectionLimit):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (dev_ip, pf_type))

    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(prfDevIp), 'admin', admpass)

    output = ''

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logging.info("new_dstAffProfile_build()- Use Standard Global naming : " + useGlobalNaming )
    
    logging.info("new_dstAffProfile_build.py Parms DevIP: " + prfDevIp + " Profile name: " + prfName + " Profile Deploy or Chnage: " + prfDplyOrChg + " Defaults-from: " + defaultsFrom) 
	
    idx = 1
    
    if prfDplyOrChg == 'new_profile':
        strReturn = {str(idx) : 'Destination Address Persistence Profile Creation Report'}
    
        idx += 1

        if useGlobalNaming == '1':
            prfName = loadStdNames.get_std_name(str(prfDevIp), 'SHARED', 'PROFILE', 'DESTINATION_PERSISTENCE', prfName)
                
        logging.info("Profile Creation process has been initiated. Destination Address Persistence Profile Name: " + prfName)
        prfPara1 = 'Common'
        if check_profileName_conflict(mr, prfName, prfPara1):
            logging.info("Before check_profileName_conflict() call\n")
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logging.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logging.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.persistence.dest_addrs.dest_addr.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, \
                    matchAcrossServices=matchAcrossServices, matchAcrossVirtuals=matchAcrossVirtuals, matchAcrossPools=matchAcrossPools, \
                    hashAlgorithm=hashAlgorithm, timeout=timeout, mask=mask, overrideConnectionLimit=overrideConnectionLimit)
        except Exception as e:
            logging.info("Exception during Destination Address Persistence Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Destination Address Persistence Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile':
        
        modContent = {}
                
        strReturn = {str(idx) : 'Destination Address Persistence Profile Modification Report'}
    
        idx += 1
    
        logging.info("Profile Modification process has been initiated. Destination Address Persistence Profile Name: " + prfName)
        
        # Load Destination Affinity profile settings of a given Destination Affinity profile name
        try:
            loadedPrf = mr.tm.ltm.persistence.dest_addrs.dest_addr.load(name=prfName, partition='Common')
        except Exception as e:
            logging.info("Exception during Destination Affinity Profile loading")
            strReturn[str(idx)] = "Exception fired during Destination Affinity Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during Destination Affinity Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        # Save the update DNS profile settings
        '''
        loadedPrf.defaultsFrom = defaultsFrom
        loadedPrf.matchAcrossServices = matchAcrossServices
        loadedPrf.matchAcrossVirtuals = matchAcrossVirtuals
        loadedPrf.matchAcrossPools = matchAcrossPools
        loadedPrf.hashAlgorithm = hashAlgorithm
        loadedPrf.timeout = timeout
        loadedPrf.mask = mask
        loadedPrf.overrideConnectionLimit = overrideConnectionLimit
        '''
        
        if isNeedUpdate(loadedPrf, modContent, defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, timeout, mask, overrideConnectionLimit):
            strReturn[str(idx)] = "Destination Affinity Profile settings have been saved!"
            idx += 1
            
            try:
                #loadedPrf.update()]
                loadedPrf.modify(**modContent)
            except Exception as e:
                strReturn[str(idx)] = "Exception fired during Destination Affinity profile update() (" + prfName + "): " + str(e)
                idx += 1
                logging.info("Destination Affinity Profile creation exception fired: " + str(e))
                return json.dumps(strReturn)
        else:
            logging.info("No Destination Address Persistence Profile modification is needed")
            strReturn[str(idx)] = "No No Destination Address Persistence Profile modification is needed (" + prfName + "): "
            idx += 1            
    if prfDplyOrChg == 'new_profile':     
        strReturn[str(idx)] = "Destination Address Persistence Profile(" + prfName + ") has been created"
        idx += 1
        logging.info("Destination Address Persistence Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "Destination Address Persistence Profile modification(" + prfName + ") has been completed"
        idx += 1
        logging.info("Destination Address Persistence Profile modification has been completed")

    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    print new_dstAffProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11])
