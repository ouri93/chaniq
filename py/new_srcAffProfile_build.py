from f5.bigip import ManagementRoot
import sys
import logging
import json

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
		
def new_srcAffProfile_build(prfDevIp, prfName, prfPara1, prfPara2, prfPara3, prfPara4, prfPara5, prfPara6, prfPara7, prfPara8, prfPara9):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (dev_ip, pf_type))
	
    mr = ManagementRoot('192.168.80.150', 'admin', 'rlatkdcks')
    output = ''

    logging.info("new_srcAffProfile_build.py Parms DevIP: " + prfDevIp + " Profile name: " + prfName + " Defaults-from: " + prfPara1) 

    mr = ManagementRoot(str(prfDevIp), 'admin', 'rlatkdcks')
	
    idx = 1
    strReturn = {str(idx) : 'Source Address Persistence Profile Creation Report'}

    idx += 1

    logging.info("Profile Creation process has been initiated. Source Address Persistence Profile Name: " + prfName)

    if check_profileName_conflict(mr, prfName, prfPara1):
        strReturn.update({str(idx) : 'Profile Name conflict'})
        logging.info("Profile name conflict.")
        idx += 1
        return json.dumps(strReturn)
    logging.info("No profile name conflict. Now creating the requested profile")
		
    try:
        mydg = mr.tm.ltm.persistence.source_addrs.source_addr.create(name=prfName, partition='Common', defaultsFrom=prfPara1, matchAcrossServices=prfPara2, matchAcrossVirtuals=prfPara3, matchAcrossPools=prfPara4, hashAlgorithm=prfPara5, timeout=prfPara6, mask=prfPara7, mapProxies=prfPara8, overrideConnectionLimit=prfPara9)
    except Exception as e:
        logging.info("Exception during Source Address Persistence Profile creation")
        strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
        idx += 1
        logging.info("Source Address Persistence Profile creation exception fired: " + str(e))
        return json.dumps(strReturn)

    strReturn[str(idx)] = "Source Address Persistence Profile (" + prfName + ") has been created"
    idx += 1
    logging.info("Source Address Persistence Profile has been created")

    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_srcAffProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11])
