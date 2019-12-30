from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass
import loadStdNames

def check_profileName_conflict(mr, prfName, prfDftFrom):
    tcpPrfNames = mr.tm.ltm.profile.tcps.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for tcpPrfName in tcpPrfNames:
        if tcpPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

        #  'defaultsFrom', 'resetOnTimeout', 'proxyBufferHigh', 'proxyBufferLow',
        #  'receiveWindowSize', 'sendBufferSize', 'ackOnPush', 'nagle', 'initCwnd',
        #  'slowStart', 'selectiveAcks' 		
def new_tcpProfile_build(active_ltm, prfName, prfDplyOrChg, defaultsFrom, resetOnTimeout, proxyBufferHigh, proxyBufferLow, receiveWindowSize, sendBufferSize, ackOnPush, nagle, initCwnd, slowStart, selectiveAcks):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    output = ''

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logging.info("new_tcpProfile_build()- Use Standard Global naming : " + useGlobalNaming )
    
    logging.info("new_tcpProfile_build.py Parms DevIP: " + active_ltm + " Profile name: " + prfName + " Profile Deploy or Change: " + prfDplyOrChg + " Defaults-from: " + defaultsFrom) 
    idx = 1

    if prfDplyOrChg == 'new_profile': 
        strReturn = {str(idx) : 'TCP Profile Creation Report'}
        idx += 1

        if useGlobalNaming == '1':
            prfName = loadStdNames.get_std_name(active_ltm, 'SHARED', 'PROFILE', 'TCP_PROTOCOL', prfName)
                
        logging.info("Profile Creation process has been initiated. TCP Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logging.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logging.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.profile.tcps.tcp.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, resetOnTimeout=resetOnTimeout,\
                 proxyBufferHigh=proxyBufferHigh, proxyBufferLow=proxyBufferLow, receiveWindowSize=receiveWindowSize, sendBufferSize=sendBufferSize,\
                 ackOnPush=ackOnPush, nagle=nagle, initCwnd=initCwnd, slowStart=slowStart, selectiveAcks=selectiveAcks)
        except Exception as e:
            logging.info("Exception during TCP  Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("TCP Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile':
        strReturn = {str(idx) : 'TCP Profile Modification Report'}
        idx += 1
    
        logging.info("Profile Modification process has been initiated. TCP Profile Name: " + prfName)
        
        # Load TCP profile settings of a given TCP profile name
        #  'defaultsFrom', 'resetOnTimeout', 'proxyBufferHigh', 'proxyBufferLow',
        #  'receiveWindowSize', 'sendBufferSize', 'ackOnPush', 'nagle', 'initCwnd',
        #  'slowStart', 'selectiveAcks'   
        try:
            aTcpPrf = mr.tm.ltm.profile.tcps.tcp.load(name=prfName, partition='Common')
        except Exception as e:
            logging.info("Exception during TCP Profile loading")
            strReturn[str(idx)] = "Exception fired during TCP Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during TCP Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # Save the update TCP profile settings
        aTcpPrf.defaultsFrom = defaultsFrom
        aTcpPrf.resetOnTimeout = resetOnTimeout
        aTcpPrf.proxyBufferHigh = proxyBufferHigh
        aTcpPrf.proxyBufferLow = proxyBufferLow
        aTcpPrf.receiveWindowSize = receiveWindowSize
        aTcpPrf.sendBufferSize = sendBufferSize
        aTcpPrf.ackOnPush = ackOnPush
        aTcpPrf.nagle = nagle
        aTcpPrf.initCwnd = initCwnd
        aTcpPrf.slowStart = slowStart
                
        strReturn[str(idx)] = "TCP Profile settings have been saved!"
        idx += 1
        
        try:
            aTcpPrf.update()
        except Exception as e:
            strReturn[str(idx)] = "Exception fired during TCP profile update() (" + prfName + "): " + str(e)
            idx += 1
            logging.info("TCP Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    
    if prfDplyOrChg == 'new_profile':
        strReturn[str(idx)] = "TCP Profile (" + prfName + ") has been created"
        idx += 1
        logging.info("TCP Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "TCP Profile Modification(" + prfName + ") has been completed"
        idx += 1
        logging.info("TCP Profile modification has been completed")
    
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_tcpProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14])
