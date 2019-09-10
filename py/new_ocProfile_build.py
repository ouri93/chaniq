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
		
def new_ocProfile_build(prfDevIp, prfName, prfDplyOrChg, prfPara1, prfPara2, prfPara3, prfPara4, prfPara5, prfPara6, prfPara7):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (dev_ip, pf_type))
	
    mr = ManagementRoot(prfDevIp, 'admin', 'rlatkdcks')
    output = ''

    logging.info("new_ocProfile_build.py Parms DevIP: " + prfDevIp + " Profile name: " + prfName + " Profile Deploy or Change: " + prfDplyOrChg + " Defaults-from: " + prfPara1) 

    mr = ManagementRoot(str(prfDevIp), 'admin', 'rlatkdcks')
	
    idx = 1
    strReturn = {str(idx) : 'OneConnect Persistence Profile Creation Report'}

    idx += 1

    logging.info("Profile Creation process has been initiated. OneConnect Persistence Profile Name: " + prfName)

    if check_profileName_conflict(mr, prfName, prfPara1):
        strReturn.update({str(idx) : 'Profile Name conflict'})
        logging.info("Profile name conflict.")
        idx += 1
        return json.dumps(strReturn)
    logging.info("No profile name conflict. Now creating the requested profile")
		
    try:
        mydg = mr.tm.ltm.profile.one_connects.one_connect.create(name=prfName, partition='Common', defaultsFrom=prfPara1, sourceMask=prfPara2, maxSize=prfPara3, maxAge=prfPara4, maxReuse=prfPara5, idleTimeoutOverride=prfPara6, limitType=prfPara7)
    except Exception as e:
        logging.info("Exception during OneConnect Persistence Profile creation")
        strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
        idx += 1
        logging.info("OneConnect Persistence Profile creation exception fired: " + str(e))
        return json.dumps(strReturn)

    strReturn[str(idx)] = "OneConnect Persistence Profile (" + prfName + ") has been created"
    idx += 1
    logging.info("OneConnect Persistence Profile has been created")

    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_ocProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])
