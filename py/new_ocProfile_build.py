from f5.bigip import ManagementRoot
import sys
import logging
import json

def check_profileName_conflict(mr, prfName, prfDftFrom):
    ocPrfNames = mr.tm.ltm.profile.one_connects.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for ocPrfName in ocPrfNames:
        if ocPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  
		
#'defaultsFrom', 'sourceMask', 'maxSize', 'maxAge', 'maxReuse', 'idleTimeoutOverride', 'limitType'
def new_ocProfile_build(prfDevIp, prfName, prfDplyOrChg, defaultsFrom, sourceMask, maxSize, maxAge, maxReuse, idleTimeoutOverride, limitType):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (dev_ip, pf_type))
	
    mr = ManagementRoot(str(prfDevIp), 'admin', 'rlatkdcks')
    output = ''

    logging.info("new_ocProfile_build.py Parms DevIP: " + prfDevIp + " Profile name: " + prfName + " Profile Deploy or Change: " + prfDplyOrChg + " Defaults-from: " + defaultsFrom) 

    idx = 1
    if prfDplyOrChg == 'new_profile':    
        strReturn = {str(idx) : 'OneConnect Profile Creation Report'}
        idx += 1
    
        logging.info("Profile Creation process has been initiated. OneConnect Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logging.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logging.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.profile.one_connects.one_connect.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, sourceMask=sourceMask, \
                   maxSize=maxSize, maxAge=maxAge, maxReuse=maxReuse, idleTimeoutOverride=idleTimeoutOverride, limitType=limitType)
        except Exception as e:
            logging.info("Exception during OneConnect Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("OneConnect Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile':
        strReturn = {str(idx) : 'OneConnect Profile Modification Report'}
        idx += 1
    
        logging.info("Profile Modification process has been initiated. OneConnect Profile Name: " + prfName)
        
        # Load OneConnect profile settings of a given OneConnect profile name
        # 'defaultsFrom', 'sourceMask', 'maxSize', 'maxAge', 'maxReuse', 'idleTimeoutOverride', 'limitType'
        try:
            aOCPrf = mr.tm.ltm.profile.one_connects.one_connect.load(name=prfName, partition='Common')
        except Exception as e:
            logging.info("Exception during OneConnect Profile loading")
            strReturn[str(idx)] = "Exception fired during OneConnect Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during OneConnect Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # Save the update OneConnect profile settings
        aOCPrf.defaultsFrom = defaultsFrom
        aOCPrf.sourceMask = sourceMask
        aOCPrf.maxSize = maxSize
        aOCPrf.maxAge = maxAge
        aOCPrf.maxReuse = maxReuse
        aOCPrf.idleTimeoutOverride = idleTimeoutOverride
        aOCPrf.limitType = limitType

                
        strReturn[str(idx)] = "OneConnect Profile settings have been saved!"
        idx += 1
        
        try:
            aOCPrf.update()
        except Exception as e:
            strReturn[str(idx)] = "Exception fired during OneConnect profile loading (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during OneConnect profile loading: " + str(e))
            return json.dumps(strReturn)
    
    if prfDplyOrChg == 'new_profile':
        strReturn[str(idx)] = "OneConnect Profile(" + prfName + ") has been created"
        idx += 1
        logging.info("OneConnect Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "OneConnect Profile Modification(" + prfName + ") has been completd"
        idx += 1
        logging.info("OneConnect Profile Modification has been completed")

    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_ocProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])
