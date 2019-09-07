from f5.bigip import ManagementRoot
import sys
import logging
import json

def get_setting_val(aPrf, attName):
    try:
        accessVal = 'aPrf' + '.' + attName
        return eval(accessVal)
    except AttributeError:
        return ""

def get_setting_list_val(aPrf, attName):
    try:
        accessVal = 'aPrf' + '.' + attName
        listVals = eval(accessVal)
        return ' '.join(listVals)
    except AttributeError:
        return ""
def get_setting_dict_val(aPrf, fstAttName, sndAttName):
    try:
      accessVal = 'aPrf' + '.' + fstAttName
      prfDict = eval(accessVal)
      logging.info("explictProxy Values: " + (prfDict.get(sndAttName)).split('/')[2])
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
        logging.info("Exception during retrieving profile setting: " + str(e))
    logging.info('getHttpRevSettings(): ' + output)
    return output

def getHttpExpSettings(mr, prfName):
    httpPrfs = mr.tm.ltm.profile.https.get_collection()
    output = ''
    #outputDict = {'proxyType':'explicit', 'defaultsFrom':'/Common/http', 'basicAuthRealm':'', 'fallbackHost':'', 'fallbackStatusCodes':'', 'headerErase':'', 'headerInsert':'', 'insertXforwardedFor':'', 'serverAgentName':''}

    try:
        for aprf in httpPrfs:
            if(aprf.name == prfName):
                output += 'explicit|'
                output += '/Common/http|'
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
        logging.info("Exception during retrieving profile setting: " + str(e))
    logging.info('getHttpExpSettings(): ' + output)
    return output

def getHttpTransSettings(mr, prfName):
    httpPrfs = mr.tm.ltm.profile.https.get_collection()
    output = ''
    #outputDict = {'proxyType':'explicit', 'defaultsFrom':'/Common/http', 'basicAuthRealm':'', 'fallbackHost':'', 'fallbackStatusCodes':'', 'headerErase':'', 'headerInsert':'', 'insertXforwardedFor':'', 'serverAgentName':''}
    try:
        for aprf in httpPrfs:
            if(aprf.name == prfName):
                output += 'transparent|'
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
        logging.info("Exception during retrieving profile setting: " + str(e))
    logging.info('getHttpTransSettings(): ' + output)
    return output

def loadHttpSettings(mr, prfName):
    http_prfs = mr.tm.ltm.profile.https.get_collection()
    output = ''

    # Print HTTP Profile settings for a gvien http profile name
    #outputDict = {'proxyType':'explicit', 'defaultsFrom':'/Common/http', 'basicAuthRealm':'', 
    #              'fallbackHost':'', 'fallbackStatusCodes':'', 'headerErase':'', 'headerInsert':'', 
    #              'insertXforwardedFor':'', 'serverAgentName':''}
    try:
        for aHttpPrf in http_prfs:
            if aHttpPrf.fullPath == '/Common/' + prfName:
                output += get_setting_val(aHttpPrf,'proxyType|') + "|"
                output += get_setting_val(aHttpPrf,'fullPath|') + "|"
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
        logging.info("loadHttpSettings() - Exception during loading HTTP profile setting: " + str(e))
        
    return output
    
def getHttpSettings(dev_ip, proxyType, prfType, prfName, prfMode):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    logging.info('Called getHttpSettings(): %s %s %s %s %s' % (dev_ip, proxyType, prfType, prfName, prfMode))
    
    mr = ManagementRoot(dev_ip, 'admin', 'rlatkdcks')

    output = {}
    
    if prfMode == 'new_profile':
        '''
        Suppported Proxy Mode
        1. Reverse
        2. Explicit
        3. Transparent
        '''
        if proxyType == "reverse" :
            logging.info('getHttpSettings() reverse Proxy mode')
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
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    # argv[1] - Device IP, argv[2] - Monitor Type, argv[3] - Parent Monitor Name
    print getHttpSettings(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
