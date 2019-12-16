from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

def check_profileName_conflict(mr, prfName, prfDftFrom):
    f4PrfNames = mr.tm.ltm.profile.fastl4s.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for f4PrfName in f4PrfNames:
        if f4PrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  


# 'defaultsFrom', 'resetOnTimeout', 'reassembleFragments', 'idleTimeout',
# 'tcpHandshakeTimeout', 'tcpTimestampMode', 'tcpWscaleMode', 'looseInitialization',
# 'looseClose', 'tcpCloseTimeout', 'keepAliveInterval'		
def new_f4Profile_build(active_ltm, prfName, prfDplyOrChg, defaultsFrom, resetOnTimeout, reassembleFragments, idleTimeout, tcpHandshakeTimeout, tcpTimestampMode, tcpWscaleMode, looseInitialization, looseClose, tcpCloseTimeout, keepAliveInterval):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    output = ''

    logging.info("new_f4Profile_build.py Parms DevIP: " + active_ltm + " Profile name: " + prfName + " Profile Deploy or Change: " + prfDplyOrChg + " Defaults-from: " + defaultsFrom) 
	
    idx = 1
    if prfDplyOrChg == 'new_profile':  
        strReturn = {str(idx) : 'FastL4  Profile Creation Report'}
    
        idx += 1
    
        logging.info("Profile Creation process has been initiated. FastL4  Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logging.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logging.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.profile.fastl4s.fastl4.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, resetOnTimeout=resetOnTimeout,\
                     reassembleFragments=reassembleFragments, idleTimeout=idleTimeout, tcpHandshakeTimeout=tcpHandshakeTimeout, \
                     tcpTimestampMode=tcpTimestampMode, tcpWscaleMode=tcpWscaleMode, looseInitialization=looseInitialization, looseClose=looseClose, \
                     tcpCloseTimeout=tcpCloseTimeout, keepAliveInterval=keepAliveInterval)
        except Exception as e:
            logging.info("Exception during FastL4  Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("FastL4  Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile':
        strReturn = {str(idx) : 'FastL4  Profile Modification Report'}
        idx += 1
    
        logging.info("Profile Modification process has been initiated. FastL4 Profile Name: " + prfName)
        
        # Load FastL4 profile settings of a given FastL4 profile name
        # 'defaultsFrom', 'resetOnTimeout', 'reassembleFragments', 'idleTimeout',
        # 'tcpHandshakeTimeout', 'tcpTimestampMode', 'tcpWscaleMode', 'looseInitialization',
        # 'looseClose', 'tcpCloseTimeout', 'keepAliveInterval'    
        try:
            aFl4Prf = mr.tm.ltm.profile.fastl4s.fastl4.load(name=prfName, partition='Common')
        except Exception as e:
            logging.info("Exception during FastL4 Profile loading")
            strReturn[str(idx)] = "Exception fired during FastL4 Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during FastL4 Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # Save the update FastL4 profile settings
        aFl4Prf.defaultsFrom = defaultsFrom
        aFl4Prf.resetOnTimeout = resetOnTimeout
        aFl4Prf.reassembleFragments = reassembleFragments
        aFl4Prf.idleTimeout = idleTimeout
        aFl4Prf.tcpHandshakeTimeout = tcpHandshakeTimeout
        aFl4Prf.tcpTimestampMode = tcpTimestampMode
        aFl4Prf.tcpWscaleMode = tcpWscaleMode
        aFl4Prf.looseInitialization = looseInitialization
        aFl4Prf.looseClose = looseClose
        aFl4Prf.tcpCloseTimeout = tcpCloseTimeout
        aFl4Prf.keepAliveInterval = keepAliveInterval
                
        strReturn[str(idx)] = "FastL4 Profile settings have been saved!"
        idx += 1
        
        try:
            aFl4Prf.update()
        except Exception as e:
            strReturn[str(idx)] = "Exception fired during FastL4 profile update() (" + prfName + "): " + str(e)
            idx += 1
            logging.info("FastL4 Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    
    if prfDplyOrChg == 'new_profile':
        strReturn[str(idx)] = "FastL4 Profile(" + prfName + ") has been created"
        idx += 1
        logging.info("FastL4  Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "FastL4 Profile Modification(" + prfName + ") has been completed"
        idx += 1
        logging.info("FastL4  Profile Modification has been completed")
        
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_f4Profile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14])
