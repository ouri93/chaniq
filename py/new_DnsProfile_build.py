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
		
def new_DnsProfile_build(prfDevIp, prfName, prfDplyOrChg, prfDftFrom, prfHwValid, prfHwRespCache, prfDnsExp, prfGtm, prfUnhandledAct, prfUseBind, prfZoneXfr, prfDnsSecurity, prfRecursion):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (dev_ip, pf_type))
	
    mr = ManagementRoot(str(prfDevIp), 'admin', 'rlatkdcks')
    output = ''


    logging.info("new_DnsProfile_build.py Parms \nDevIP: " + prfDevIp + "\nProfile name: " + prfName + "\nProfile Deploy or Change: " + prfDplyOrChg + "\nDefaults-from: " + prfDftFrom) 

    idx = 1
    
    #logging.info("ProxyType before change: " + prfPxyType)
    if prfDplyOrChg == 'new_profile':    
        strReturn = {str(idx) : 'DNS Profile Creation Report'}

        idx += 1

        logging.info("Profile Creation process has been initiated. Profile Name: " + prfName + "\n")
    
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
    elif prfDplyOrChg == 'chg_profile':
        strReturn = {str(idx) : 'DNS Profile Modification Report'}

        idx += 1
        
        logging.info("Profile Modification process has been initiated. Profile Name: " + prfName + "\n")
        
        # Load DNS profile settings of a given DNS profile name
        try:
            aDnsPrf = mr.tm.ltm.profile.dns_s.dns.load(name=prfName, partition='Common')
        except Exception as e:
            logging.info("Exception during DNS Profile loading")
            strReturn[str(idx)] = "Exception fired during DNS Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during DNS Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # Save the update DNS profile settings
        logging.info("I am top")
        aDnsPrf.defaultsFrom = prfDftFrom
        aDnsPrf.enableHardwareQueryValidation = prfHwValid
        aDnsPrf.enableHardwareResponseCache = prfHwRespCache
        aDnsPrf.enableDnsExpress = prfDnsExp
        aDnsPrf.enableGtm = prfGtm
        aDnsPrf.unhandledQueryAction = prfUnhandledAct
        aDnsPrf.useLocalBind = prfUseBind
        aDnsPrf.processXfr = prfZoneXfr
        aDnsPrf.enableDnsFirewall = prfDnsSecurity
        aDnsPrf.processRd = prfRecursion
        
        strReturn[str(idx)] = "DNS Profile settings have been saved!"
        idx += 1
        
        try:
            aDnsPrf.update()
        except Exception as e:
            strReturn[str(idx)] = "Exception fired during DNS profile update() (" + prfName + "): " + str(e)
            idx += 1
            logging.info("DNS Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
  
    if prfDplyOrChg == 'new_profile': 
        strReturn[str(idx)] = "DNS Profile (" + prfName + ") has been created"
        idx += 1
        logging.info("DNS Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "DNS Profile modification has been completed"
        idx += 1
        logging.info("DNS Profile modification has been completed")
        
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
        
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_DnsProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13])
