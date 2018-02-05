from f5.bigip import ManagementRoot
import sys
import logging
import json

def check_profileName_conflict(mr, prfName, prfDftFrom):
    dnsPrfNames = mr.tm.ltm.profile.dns_s.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for httpPrfName in dnsPrfNames:
        if httpPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  
		
def new_DnsProfile_build(prfDevIp, prfName, prfDftFrom, prfHwValid, prfHwRespCache, prfDnsExp, prfGtm, prfUnhandledAct, prfUseBind, prfZoneXfr, prfDnsSecurity, prfRecursion):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (dev_ip, pf_type))
	
    mr = ManagementRoot('192.168.80.150', 'admin', 'rlatkdcks')
    output = ''

    logging.info("new_DnsProfile_build.py Parms DevIP: " + prfDevIp + " Profile name: " + prfName + " Defaults-from: " + prfDftFrom) 

    mr = ManagementRoot(str(prfDevIp), 'admin', 'rlatkdcks')
	
    idx = 1
    strReturn = {str(idx) : 'DNS Profile Creation Report'}

    idx += 1
    #logging.info("ProxyType before change: " + prfPxyType)

    logging.info("Profile Creation process has been initiated. Profile Name: " + prfName)

    if check_profileName_conflict(mr, prfName, prfDftFrom):
        strReturn.update({str(idx) : 'Profile Name conflict'})
        logging.info("Profile name conflict.")
        idx += 1
        return json.dumps(strReturn)
    logging.info("No profile name conflict. Now creating the requested profile")
		
    try:
        mydg = mr.tm.ltm.profile.dns_s.dns.create(name=prfName, partition='Common', defaultsFrom=prfDftFrom, enableHardwareQueryValidation=prfHwValid, enableHardwareResponseCache=prfHwRespCache, enableDnsExpress=prfDnsExp, enableGtm=prfGtm, unhandledQueryAction=prfUnhandledAct , useLocalBind=prfUseBind, processXfr=prfZoneXfr, enableDnsFirewall=prfDnsSecurity, processRd=prfRecursion)
    except Exception as e:
        logging.info("Exception during DNS Profile creation")
        strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
        idx += 1
        logging.info("DNS Profile creation exception fired: " + str(e))
        return json.dumps(strReturn)

    strReturn[str(idx)] = "DNS Profile (" + prfName + ") has been created"
    idx += 1
    logging.info("DNS Profile has been created")

    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_DnsProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12])
