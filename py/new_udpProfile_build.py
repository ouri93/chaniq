from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

def check_profileName_conflict(mr, prfName, prfDftFrom):
    udpPrfNames = mr.tm.ltm.profile.udps.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for udpPrfName in udpPrfNames:
        if udpPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  
#  'defaultsFrom', 'proxyMss', 'idleTimeout', 'ipTosToClient', 'linkQosToClient',
#  'datagramLoadBalancing', 'allowNoPayload', 'ipDfMode', 'ipTtlV4', 'ipTtlV6',
#  'ipDfMode'		
def new_udpProfile_build(active_ltm, prfName, prfDplyOrChg, defaultsFrom, proxyMss, idleTimeout, ipTosToClient, linkQosToClient, datagramLoadBalancing, allowNoPayload, ipTtlMode, ipTtlV4, ipTtlV6, ipDfMode):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    output = ''

    logging.info("new_udpProfile_build.py Parms DevIP: " + active_ltm + " Profile name: " + prfName + " Profile Deploy or Change: " + prfDplyOrChg + " Defaults-from: " + defaultsFrom) 
    idx = 1
    if prfDplyOrChg == 'new_profile':
        strReturn = {str(idx) : 'UDP Profile Creation Report'}
    
        idx += 1
    
        logging.info("Profile Creation process has been initiated. UDP Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logging.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logging.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.profile.udps.udp.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, proxyMss=proxyMss, idleTimeout=idleTimeout, ipTosToClient=ipTosToClient, linkQosToClient=linkQosToClient, datagramLoadBalancing=datagramLoadBalancing, allowNoPayload=allowNoPayload, ipTtlMode=ipTtlMode, ipTtlV4=ipTtlV4, ipTtlV6=ipTtlV6, ipDfMode=ipDfMode)
        except Exception as e:
            logging.info("Exception during UDP Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("UDP Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile': 
        strReturn = {str(idx) : 'UDP Profile Creation Report'}
        idx += 1
    
        logging.info("Profile Modification process has been initiated. UDP Profile Name: " + prfName)
        
        # Load UDP profile settings of a given UDP profile name
        #  'defaultsFrom', 'proxyMss', 'idleTimeout', 'ipTosToClient', 'linkQosToClient',
        #  'datagramLoadBalancing', 'allowNoPayload', 'ipDfMode', 'ipTtlV4', 'ipTtlV6',
        #  'ipDfMode'  
        try:
            aUdpPrf = mr.tm.ltm.profile.udps.udp.load(name=prfName, partition='Common')
        except Exception as e:
            logging.info("Exception during UDP Profile loading")
            strReturn[str(idx)] = "Exception fired during UDP Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during UDP Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # Save the update UDP profile settings
        aUdpPrf.defaultsFrom = defaultsFrom
        aUdpPrf.proxyMss = proxyMss
        aUdpPrf.idleTimeout = idleTimeout
        aUdpPrf.ipTosToClient = ipTosToClient
        aUdpPrf.linkQosToClient = linkQosToClient
        aUdpPrf.datagramLoadBalancing = datagramLoadBalancing
        aUdpPrf.allowNoPayload = allowNoPayload
        aUdpPrf.ipDfMode = ipDfMode
        aUdpPrf.ipTtlV4 = ipTtlV4
        aUdpPrf.ipTtlV6 = ipTtlV6
        aUdpPrf.ipDfMode = ipDfMode
                
        strReturn[str(idx)] = "UDP Profile settings have been saved!"
        idx += 1
        
        try:
            aUdpPrf.update()
        except Exception as e:
            strReturn[str(idx)] = "Exception fired during UDP profile update() (" + prfName + "): " + str(e)
            idx += 1
            logging.info("UDP Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
        
    if prfDplyOrChg == 'new_profile':
        strReturn[str(idx)] = "UDP Profile (" + prfName + ") has been created"
        idx += 1
        logging.info("UDP Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "UDP Profile Modification(" + prfName + ") has been completed"
        idx += 1
        logging.info("UDP Profile Modification has been completed")

    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_udpProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14])
