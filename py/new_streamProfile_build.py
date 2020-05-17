from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass
import loadStdNames
import chaniq_util

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
    
def isNeedUpdate(loadedPrf, modContent, defaultsFrom, source, tmTarget):
    cnt = 0    

    if chaniq_util.isStrPropModified(loadedPrf, 'defaultsFrom', defaultsFrom):
        modContent['defaultsFrom'] = defaultsFrom
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'source', source):
        modContent['source'] = source
        cnt = cnt + 1 
    if chaniq_util.isStrPropModified(loadedPrf, 'tmTarget', tmTarget):
        modContent['tmTarget'] = tmTarget
        cnt = cnt + 1 

    if cnt > 0: return True
    else: return False 
    
#  'defaultsFrom', 'source', 'tmTarget'		
def new_streamProfile_build(active_ltm, prfName, prfDplyOrChg, defaultsFrom, source, tmTarget):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    output = ''

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logging.info("new_streamProfile_build()- Use Standard Global naming : " + useGlobalNaming )
    
    logging.info("new_streamProfile_build.py Parms DevIP: " + active_ltm + " Profile name: " + prfName + " Profile Deploy or Change: " + prfDplyOrChg + " Defaults-from: " + defaultsFrom) 
    idx = 1
    
    if prfDplyOrChg == 'new_profile':
        strReturn = {str(idx) : 'Stream Profile Creation Report'}
        idx += 1

        if useGlobalNaming == '1':
            prfName = loadStdNames.get_std_name(active_ltm, 'SHARED', 'PROFILE', 'STREAM', prfName)
                
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
        
        modContent = {}
        
        strReturn = {str(idx) : 'Stream Profile Modification Report'}
        idx += 1
    
        logging.info("Profile Modification process has been initiated. Stream Profile Name: " + prfName)
        
        # Load Stream profile settings of a given Stream profile name
        # 'defaultsFrom', 'source', 'tmTarget'
        try:
            loadedPrf = mr.tm.ltm.profile.streams.stream.load(name=prfName, partition='Common')
        except Exception as e:
            logging.info("Exception during Stream Profile loading")
            strReturn[str(idx)] = "Exception fired during Stream Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during Stream Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        
        # Save the update Stream profile settings
        '''
        loadedPrf.defaultsFrom = defaultsFrom
        loadedPrf.source = source
        loadedPrf.tmTarget = tmTarget
        '''
        
        if isNeedUpdate(loadedPrf, modContent, defaultsFrom, source, tmTarget):        
            strReturn[str(idx)] = "Stream Profile settings have been saved!"
            idx += 1
            
            try:
                #loadedPrf.update()
                loadedPrf.modify (**modContent)
            except Exception as e:
                strReturn[str(idx)] = "Exception fired during Stream profile modification (" + prfName + "): " + str(e)
                idx += 1
                logging.info("Stream Profile modification exception fired: " + str(e))
                return json.dumps(strReturn)
        else:
            logging.info("No Stream Profile modification is needed")
            strReturn[str(idx)] = "No Stream Profile modification is needed (" + prfName + "): "
            idx += 1                
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
