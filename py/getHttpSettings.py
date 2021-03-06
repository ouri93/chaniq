from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def get_setting_val(aPrf, attName):
    try:
        accessVal = 'aPrf' + '.' + attName
        logger.info('get_setting_val(): ' + accessVal)
        return eval(accessVal)
    except AttributeError:
        return ""

def get_setting_list_val(aPrf, attName):
    try:
        accessVal = 'aPrf' + '.' + attName
        listVals = eval(accessVal)
        logger.info('get_setting_list_val(): ' + accessVal)
        return ' '.join(listVals)
    except AttributeError:
        return ""
def get_setting_dict_val(aPrf, fstAttName, sndAttName):
    try:
      accessVal = 'aPrf' + '.' + fstAttName
      prfDict = eval(accessVal)
      logger.info("explictProxy Values: " + (prfDict.get(sndAttName)).split('/')[2])
      logger.info('get_setting_dict_val(): ' + accessVal)
      return (prfDict.get(sndAttName)).split('/')[2]
    except AttributeError:
        return ""
    
def getHttpRevSettings(mr, prfName):
    httpPrfs = mr.tm.ltm.profile.https.get_collection()
    output = ''
    #outputDict = {'proxyType':'reverse', 'defaultsFrom':'/Common/http', 'basicAuthRealm':'', 'fallbackHost':'', 'fallbackStatusCodes':'', 'headerErase':'', 'headerInsert':'', 'insertXforwardedFor':'', 'serverAgentName':''}
    try:
        for aprf in httpPrfs:
            if(aprf.name == prfName):
                output += 'reverse|'
                output += '/Common/http|'
                output += get_setting_val(aprf, 'basicAuthRealm') + "|"
                output += get_setting_val(aprf, 'fallbackHost') + "|"
                output += get_setting_list_val(aprf, 'fallbackStatusCodes') + "|"
                output += get_setting_val(aprf, 'headerErase') + "|"
                output += get_setting_val(aprf, 'headerInsert') + "|"
                output += get_setting_val(aprf, 'requestChunking') + "|"
                output += get_setting_val(aprf, 'responseChunking') + "|"
                output += get_setting_val(aprf, 'insertXforwardedFor') + "|"
                output += get_setting_val(aprf, 'serverAgentName')
    except Exception as e:
        logger.info("Exception during retrieving profile setting: " + str(e))
    logger.info('getHttpRevSettings(): ' + output)
    return output

def getHttpExpSettings(mr, prfName):
    httpPrfs = mr.tm.ltm.profile.https.get_collection()
    output = ''
    #outputDict = {'proxyType':'explicit', 'defaultsFrom':'/Common/http', 'basicAuthRealm':'', 'fallbackHost':'', 'fallbackStatusCodes':'', 'headerErase':'', 'headerInsert':'', 'insertXforwardedFor':'', 'serverAgentName':''}

    try:
        for aprf in httpPrfs:
            if(aprf.name == prfName):
                output += 'explicit|'
                output += '/Common/http-explicit|'
                output += get_setting_val(aprf, 'basicAuthRealm') + "|"
                output += get_setting_val(aprf, 'fallbackHost') + "|"
                output += get_setting_list_val(aprf, 'fallbackStatusCodes') + "|"
                output += get_setting_val(aprf, 'headerErase') + "|"
                output += get_setting_val(aprf, 'headerInsert') + "|"
                output += get_setting_val(aprf, 'requestChunking') + "|"
                output += get_setting_val(aprf, 'responseChunking') + "|"
                output += get_setting_val(aprf, 'insertXforwardedFor') + "|"
                output += get_setting_val(aprf, 'serverAgentName') + "|"
                output += get_setting_dict_val(aprf, 'explicitProxy', 'dnsResolver')
    except Exception as e:
        logger.info("Exception during retrieving profile setting: " + str(e))
    logger.info('getHttpExpSettings(): ' + output)
    return output

def getHttpTransSettings(mr, prfName):
    httpPrfs = mr.tm.ltm.profile.https.get_collection()
    output = ''
    #outputDict = {'proxyType':'explicit', 'defaultsFrom':'/Common/http', 'basicAuthRealm':'', 'fallbackHost':'', 'fallbackStatusCodes':'', 'headerErase':'', 'headerInsert':'', 'insertXforwardedFor':'', 'serverAgentName':''}
    try:
        for aprf in httpPrfs:
            if(aprf.name == prfName):
                output += 'transparent|'
                output += '/Common/http-transparent|'
                output += get_setting_val(aprf, 'basicAuthRealm') + "|"
                output += get_setting_val(aprf, 'fallbackHost') + "|"
                output += get_setting_list_val(aprf, 'fallbackStatusCodes') + "|"
                output += get_setting_val(aprf, 'headerErase') + "|"
                output += get_setting_val(aprf, 'headerInsert') + "|"
                output += get_setting_val(aprf, 'requestChunking') + "|"
                output += get_setting_val(aprf, 'responseChunking') + "|"                
                output += get_setting_val(aprf, 'insertXforwardedFor') + "|"
                output += get_setting_val(aprf, 'serverAgentName')
    except Exception as e:
        logger.info("Exception during retrieving profile setting: " + str(e))
    logger.info('getHttpTransSettings(): ' + output)
    return output

# A HTTP profile name is given, load the corresponding HTTP profile configuration
def loadHttpSettings(mr, prfName):
    http_prfs = mr.tm.ltm.profile.https.get_collection()
    output = ''

    # Print HTTP Profile settings for a gvien http profile name
    #outputDict = {'proxyType':'explicit', 'defaultsFrom':'/Common/http', 'basicAuthRealm':'', 
    #              'fallbackHost':'', 'fallbackStatusCodes':'', 'headerErase':'', 'headerInsert':'', 
    #              'insertXforwardedFor':'', 'serverAgentName':''}
    # Note: In Profile change mode, teh second return value is the name of parent profile
    try:
        for aHttpPrf in http_prfs:
            if aHttpPrf.fullPath == '/Common/' + prfName:
                output += get_setting_val(aHttpPrf,'proxyType') + "|"
                output += get_setting_val(aHttpPrf,'defaultsFrom') + "|"
                output += get_setting_val(aHttpPrf, 'basicAuthRealm') + "|"
                output += get_setting_val(aHttpPrf, 'fallbackHost') + "|"
                output += get_setting_list_val(aHttpPrf, 'fallbackStatusCodes') + "|"
                output += get_setting_val(aHttpPrf, 'headerErase') + "|"
                output += get_setting_val(aHttpPrf, 'headerInsert') + "|"
                output += get_setting_val(aHttpPrf, 'requestChunking') + "|"
                output += get_setting_val(aHttpPrf, 'responseChunking') + "|"                
                output += get_setting_val(aHttpPrf, 'insertXforwardedFor') + "|"
                output += get_setting_val(aHttpPrf, 'serverAgentName')
                if aHttpPrf.proxyType == 'explicit':
                    output += "|" + get_setting_dict_val(aHttpPrf, 'explicitProxy', 'dnsResolver')
    except Exception as e:
        logger.info("loadHttpSettings() - Exception during loading HTTP profile setting: " + str(e))
        
    return output
    
def getHttpSettings(active_ltm, proxyType, prfType, prfName, prfMode):
    logger.info('Called getHttpSettings(): %s %s %s %s %s' % (active_ltm, proxyType, prfType, prfName, prfMode))
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)

    output = {}
    
    if prfMode == 'new_profile':
        '''
        Suppported Proxy Mode
        1. Reverse
        2. Explicit
        3. Transparent
        '''
        if proxyType == "reverse" :
            logger.info('getHttpSettings() reverse Proxy mode')
            output = getHttpRevSettings(mr, prfName)
        elif proxyType == "explicit" :
            output = getHttpExpSettings(mr, prfName)
        elif proxyType == "transparent":
            output = getHttpTransSettings(mr, prfName)
    if prfMode == 'chg_profile':
        output = loadHttpSettings(mr, prfName)

    return output
    #print json.dumps(output)

if __name__ == "__main__":
    #logger.info('main called: param1: ')
    # argv[1] - Device IP, argv[2] - Monitor Type, argv[3] - Parent Monitor Name
    print getHttpSettings(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
