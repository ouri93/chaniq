from f5.bigip import ManagementRoot
import sys
import logging
import json

def check_profileName_conflict(mr, prfName, prfDftFrom):
    strmPrfNames = mr.tm.ltm.profile.streams.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for strmPrfName in strmPrfNames:
        if strmPrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  
#  'defaultsFrom', 'source', 'tmTarget'		
def new_streamProfile_build(prfDevIp, prfName, prfDplyOrChg, defaultsFrom, source, tmTarget):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (dev_ip, pf_type))
	
    mr = ManagementRoot(str(prfDevIp), 'admin', 'rlatkdcks')
    output = ''

    logging.info("new_streamProfile_build.py Parms DevIP: " + prfDevIp + " Profile name: " + prfName + " Profile Deploy or Change: " + prfDplyOrChg + " Defaults-from: " + defaultsFrom) 
    idx = 1
    
    if prfDplyOrChg == 'new_profile':
        strReturn = {str(idx) : 'Stream Profile Creation Report'}
        idx += 1
    
        logging.info("Profile Creation process has been initiated. Stream Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logging.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logging.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.profile.streams.stream.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, source=source, tmTarget=tmTarget)
        except Exception as e:
            logging.info("Exception during Stream Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Stream Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile':
        strReturn = {str(idx) : 'Stream Profile Modification Report'}
        idx += 1
    
        logging.info("Profile Modification process has been initiated. Stream Profile Name: " + prfName)
        
        # Load Stream profile settings of a given Stream profile name
        # 'defaultsFrom', 'source', 'tmTarget'
        try:
            aStrmPrf = mr.tm.ltm.profile.streams.stream.load(name=prfName, partition='Common')
        except Exception as e:
            logging.info("Exception during Stream Profile loading")
            strReturn[str(idx)] = "Exception fired during Stream Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during Stream Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # Save the update Stream profile settings
        aStrmPrf.defaultsFrom = defaultsFrom
        aStrmPrf.source = source
        aStrmPrf.tmTarget = tmTarget
                
        strReturn[str(idx)] = "Stream Profile settings have been saved!"
        idx += 1
        
        try:
            aStrmPrf.update()
        except Exception as e:
            strReturn[str(idx)] = "Exception fired during Stream profile modification (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Stream Profile modification exception fired: " + str(e))
            return json.dumps(strReturn)
    if prfDplyOrChg == 'new_profile':
        strReturn[str(idx)] = "Stream Profile (" + prfName + ") has been created"
        idx += 1
        logging.info("Stream Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "Stream Profile Modification(" + prfName + ") has been completed"
        idx += 1
        logging.info("Stream Profile modification has been completed")

    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_streamProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
