from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

def check_profileName_conflict(mr, prfName, prfDftFrom):
    cookiePrfNames = mr.tm.ltm.persistence.cookies.get_collection()
    logging.info("check_profileName_conflict() STD Name: " + prfName + "\n")
    
    bitout = 0
    
    for cookiePrfName in cookiePrfNames:
        if cookiePrfName.exists(name=prfName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  
		
#{'defaultsFrom', 'method'- Cookie method(hash, insert, passive, rewrite), 'cookieName', 'httponly', 'secure', 'alwaysSend', 'expiration', 'overrideConnectionLimit']        
def new_cookieProfile_build(active_ltm, prfName, prfDplyOrChg, defaultsFrom, method, cookieName, httponly, secure, alwaysSend, expiration, overrideConnectionLimit):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('Called get_profiles(): %s %s' % (dev_ip, pf_type))
	
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    output = ''

    logging.info("new_cookieProfile_build.py Parms DevIP: " + active_ltm + " Profile name: " + prfName + " Profile Deploy or Change: " + prfDplyOrChg + " Defaults-from: " + defaultsFrom) 

    idx = 1
    if prfDplyOrChg == 'new_profile':  
        strReturn = {str(idx) : 'Cookie Persistence Profile Creation Report'}
    
        idx += 1
        #logging.info("ProxyType before change: " + prfPxyType)
    
        logging.info("Profile Creation process has been initiated. Cookie Persistence Profile Name: " + prfName)
    
        if check_profileName_conflict(mr, prfName, defaultsFrom):
            strReturn.update({str(idx) : 'Profile Name conflict'})
            logging.info("Profile name conflict.")
            idx += 1
            return json.dumps(strReturn)
        logging.info("No profile name conflict. Now creating the requested profile")
    		
        try:
            mydg = mr.tm.ltm.persistence.cookies.cookie.create(name=prfName, partition='Common', defaultsFrom=defaultsFrom, method=method, cookieName=cookieName, httponly=httponly, secure=secure, alwaysSend=alwaysSend, expiration=expiration, overrideConnectionLimit=overrideConnectionLimit)
        except Exception as e:
            logging.info("Exception during Cookie Persistence Profile creation")
            strReturn[str(idx)] = "Exception fired! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Cookie Persistence Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
    elif prfDplyOrChg == 'chg_profile':
        strReturn = {str(idx) : 'Cookie Persistence Profile Modification Report'}
    
        idx += 1
        #logging.info("ProxyType before change: " + prfPxyType)
    
        logging.info("Profile Modification process has been initiated. Cookie Persistence Profile Name: " + prfName)
        
        # Load Cookie profile settings of a given Cookie profile name
        try:
            aCookiePrf = mr.tm.ltm.persistence.cookies.cookie.load(name=prfName, partition='Common')
        except Exception as e:
            logging.info("Exception during Cookie Persistence Profile loading")
            strReturn[str(idx)] = "Exception fired during Cookie Profile setting loading! (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Exception fired during Cookie Persistence Profile setting loading! ( " + str(e) + ")")
            return json.dumps(strReturn)
        # Save the update Cookie Persistence profile settings
        aCookiePrf.defaultsFrom = defaultsFrom
        aCookiePrf.method = method
        aCookiePrf.cookieName = cookieName
        aCookiePrf.httponly = httponly
        aCookiePrf.secure = secure
        aCookiePrf.alwaysSend = alwaysSend
        aCookiePrf.expiration = expiration
        aCookiePrf.overrideConnectionLimit = overrideConnectionLimit
        
        strReturn[str(idx)] = "Cookie Profile settings have been saved!"
        idx += 1
        
        try:
            aCookiePrf.update()
        except Exception as e:
            strReturn[str(idx)] = "Exception fired during Cookie profile update() (" + prfName + "): " + str(e)
            idx += 1
            logging.info("Cookie Profile creation exception fired: " + str(e))
            return json.dumps(strReturn)
            
    if prfDplyOrChg == 'new_profile':     
        strReturn[str(idx)] = "Cookie Persistence Profile (" + prfName + ") has been created"
        idx += 1
        logging.info("Cookie Persistence Profile has been created")
    elif prfDplyOrChg == 'chg_profile':
        strReturn[str(idx)] = "Cookie Persistence Profile modification(" + prfName + ") has been completed"
        idx += 1
        logging.info("Cookie Persistence Profile modification has been completed")
                 
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)
    
    return json.dumps(strReturn)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print new_cookieProfile_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11])
