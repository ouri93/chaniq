from f5.bigip import ManagementRoot
import sys
import logging
import json

def check_profileName_conflict(mr, prfName, prfDftFrom):
    hashPrfNames = mr.tm.ltm.persistence.hashs.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for hashPrfName in hashPrfNames:
        if hashPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  
		
def new_hashProfile_build(prfDevIp, prfName, prfDplyOrChg, prfPara1, prfPara2, prfPara3, prfPara4, prfPara5, prfPara6, prfPara7, prfPara8, prfPara9, prfPara10, prfPara11, prfPara12, prfPara13):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (dev_ip, pf_type))
	
    mr = ManagementRoot(prfDevIp, 'admin', 'rlatkdcks')
    output = ''

    logging.info("new_hashProfile_build.py Parms DevIP: " + prfDevIp + " Profile name: " + prfName + " Profile Deploy or Change: " + prfDplyOrChg + " Defaults-from: " + prfPara1) 

    mr = ManagementRoot(str(prfDevIp), 'admin', 'rlatkdcks')
	
    idx = 1
    strReturn = {str(idx) : 'Hash Persistence Profile Creation Report'}

    idx += 1

    logging.info("Profile Creation process has been initiated. Hash Persistence Profile Name: " + prfName)

    if check_profileName_conflict(mr, prfName, prfPara1):
        strReturn.update({str(idx) : 'Profile Name conflict'})
        logging.info("Profile name conflict.")
        idx += 1
        return json.dumps(strReturn)
    logging.info("No profile name conflict. Now creating the requested profile")
		
    try:
        mydg = mr.tm.ltm.persistence.hashs.hash.create(name=prfName, partition='Common', defaultsFrom=prfPara1, matchAcrossServices=prfPara2, matchAcrossVirtuals=prfPara3, matchAcrossPools=prfPara4, hashAlgorithm=prfPara5, hashOffset=prfPara6, hashLength=prfPara7, hashStartPattern=prfPara8, hashEndPattern=prfPara9, hashBufferLimit=prfPara10, timeout=prfPara11, rule=prfPara12, overrideConnectionLimit=prfPara13)
    except Exception as e:
        logging.info("Exception during Hash Persistence Profile creation")
        strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
        idx += 1
        logging.info("Hash Persistence Profile creation exception fired: " + str(e))
        return json.dumps(strReturn)

    strReturn[str(idx)] = "Hash Persistence Profile (" + prfName + ") has been created"
    idx += 1
    logging.info("Hash Persistence Profile has been created")

    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_hashProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14], sys.argv[15], sys.argv[16])
