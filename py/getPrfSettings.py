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
      return (prfDict.get(sndAttName)).split('/')[2]
    except AttributeError:
        return ""
    
def getDnsPrfSettings(mr, parPrfName):
    dnsPrfs = mr.tm.ltm.profile.dns_s.get_collection()
    output = ''
    
    #outputDict = {'defaultsFrom', 'enableHardwareQueryValidation', 'enableHardwareResponseCache', 'enableDnsExpress', 'enableGtm', 'unhandledQueryAction', 'useLocalBind', 'processXfr','enableDnsFirewall', 'processRd']
    try:
        for aprf in dnsPrfs:
            if(aprf.name == parPrfName):
                output += '/Common/'+ parPrfName + '|'
                output += get_setting_val(aprf, 'enableHardwareQueryValidation') + '|'
                output += get_setting_val(aprf, 'enableHardwareResponseCache') + '|'
                output += get_setting_val(aprf, 'enableDnsExpress') + '|'
                output += get_setting_val(aprf, 'enableGtm') + '|'
                output += get_setting_val(aprf, 'unhandledQueryAction') + '|'
                output += get_setting_val(aprf, 'useLocalBind') + '|'                
                output += get_setting_val(aprf, 'processXfr') + '|'
                output += get_setting_val(aprf, 'enableDnsFirewall') + '|'
                output += get_setting_val(aprf, 'processRd')
    except Exception as e:
        logging.info("Exception during retrieving DNS profile setting: " + str(e))
    logging.info('getDnsPrfSettings(): ' + output)
    return output

def getCookiePrfSettings(mr, parPrfName):
    cookiePrfs = mr.tm.ltm.persistence.cookies.get_collection()
    output = ''
    
    #outputDict = {'defaultsFrom', 'method'- Cookie method(hash, insert, passive, rewrite), 'cookieName', 'httponly', 'secure', 'alwaysSend', 'expiration', 'overrideConnectionLimit']
    try:
        for aprf in cookiePrfs:
            if(aprf.name == parPrfName):
                output += '/Common/'+ parPrfName + '|'
                output += get_setting_val(aprf, 'method') + '|'
                output += get_setting_val(aprf, 'cookieName') + '|'
                output += get_setting_val(aprf, 'httponly') + '|'
                output += get_setting_val(aprf, 'secure') + '|'
                output += get_setting_val(aprf, 'alwaysSend') + '|'
                output += get_setting_val(aprf, 'expiration') + '|'                
                output += get_setting_val(aprf, 'overrideConnectionLimit')
    except Exception as e:
        logging.info("Exception during retrieving Cookie Persistence profile setting: " + str(e))
    logging.info('getCookiePrfSettings(): ' + output)
    return output

def getDstAffSettings(mr, parPrfName):
    dstAffPrfs = mr.tm.ltm.persistence.dest_addrs.get_collection()
    output = ''
    
    #outputDict = {'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'timeout', 'mask', 'overrideConnectionLimit']
    try:
        for aprf in dstAffPrfs:
            if(aprf.name == parPrfName):
                output += '/Common/'+ parPrfName + '|'
                output += get_setting_val(aprf, 'matchAcrossServices') + '|'
                output += get_setting_val(aprf, 'matchAcrossVirtuals') + '|'
                output += get_setting_val(aprf, 'matchAcrossPools') + '|'
                output += get_setting_val(aprf, 'hashAlgorithm') + '|'
                output += get_setting_val(aprf, 'timeout') + '|'
                output += get_setting_val(aprf, 'mask') + '|'                
                output += get_setting_val(aprf, 'overrideConnectionLimit')
    except Exception as e:
        logging.info("Exception during retrieving Destination Address Persistence profile setting: " + str(e))
    logging.info('getDstAffSettings(): ' + output)
    return output

def getSrcAffSettings(mr, parPrfName):
    srcAffPrfs = mr.tm.ltm.persistence.source_addrs.get_collection()
    output = ''
    
    #outputDict = {'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'timeout', 'mask', 'mapProxies', 'overrideConnectionLimit']
    try:
        for aprf in srcAffPrfs:
            if(aprf.name == parPrfName):
                output += '/Common/'+ parPrfName + '|'
                output += get_setting_val(aprf, 'matchAcrossServices') + '|'
                output += get_setting_val(aprf, 'matchAcrossVirtuals') + '|'
                output += get_setting_val(aprf, 'matchAcrossPools') + '|'
                output += get_setting_val(aprf, 'hashAlgorithm') + '|'
                output += get_setting_val(aprf, 'timeout') + '|'
                output += get_setting_val(aprf, 'mask') + '|'
                output += get_setting_val(aprf, 'mapProxies') + '|'
                output += get_setting_val(aprf, 'overrideConnectionLimit')
    except Exception as e:
        logging.info("Exception during retrieving Source Address Persistence profile setting: " + str(e))
    logging.info('getSrcAffSettings(): ' + output)
    return output

def getHashSettings(mr, parPrfName):
    hashPrfs = mr.tm.ltm.persistence.hashs.get_collection()
    output = ''
    
    #outputDict = {defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, hashOffset, hashLength, hashStartPattern, hashEndPattern, hashBufferLimit, timeout, rule, overrideConnectionLimit]
    try:
        for aprf in hashPrfs:
            if(aprf.name == parPrfName):
                output += '/Common/'+ parPrfName + '|'
                output += get_setting_val(aprf, 'matchAcrossServices') + '|'
                output += get_setting_val(aprf, 'matchAcrossVirtuals') + '|'
                output += get_setting_val(aprf, 'matchAcrossPools') + '|'
                output += get_setting_val(aprf, 'hashAlgorithm') + '|'
                output += str(get_setting_val(aprf, 'hashOffset')) + '|'
                output += str(get_setting_val(aprf, 'hashLength')) + '|'
                output += get_setting_val(aprf, 'hashStartPattern') + '|'
                output += get_setting_val(aprf, 'hashEndPattern') + '|'
                output += str(get_setting_val(aprf, 'hashBufferLimit')) + '|'
                output += get_setting_val(aprf, 'timeout') + '|'
                output += get_setting_val(aprf, 'rule') + '|'
                output += get_setting_val(aprf, 'overrideConnectionLimit')
    except Exception as e:
        logging.info("Exception during retrieving Hash Persistence profile setting: " + str(e))
    logging.info('getHashSettings(): ' + output)
    return output

def getSSLSettings(mr, parPrfName):
    sslPrfs = mr.tm.ltm.persistence.ssls.get_collection()
    output = ''
    
    #outputDict = {defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, timeout, overrideConnectionLimit]
    try:
        for aprf in sslPrfs:
            if(aprf.name == parPrfName):
                output += '/Common/'+ parPrfName + '|'
                output += get_setting_val(aprf, 'matchAcrossServices') + '|'
                output += get_setting_val(aprf, 'matchAcrossVirtuals') + '|'
                output += get_setting_val(aprf, 'matchAcrossPools') + '|'
                output += get_setting_val(aprf, 'timeout') + '|'
                output += get_setting_val(aprf, 'overrideConnectionLimit')
    except Exception as e:
        logging.info("Exception during retrieving SSL Persistence profile setting: " + str(e))
    logging.info('getSSLSettings(): ' + output)
    return output

def getUniSettings(mr, parPrfName):
    uniPrfs = mr.tm.ltm.persistence.universals.get_collection()
    output = ''
    
    #outputDict = {defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, timeout, rule, overrideConnectionLimit]
    try:
        for aprf in uniPrfs:
            if(aprf.name == parPrfName):
                output += '/Common/'+ parPrfName + '|'
                output += get_setting_val(aprf, 'matchAcrossServices') + '|'
                output += get_setting_val(aprf, 'matchAcrossVirtuals') + '|'
                output += get_setting_val(aprf, 'matchAcrossPools') + '|'
                output += get_setting_val(aprf, 'timeout') + '|'
                output += get_setting_val(aprf, 'rule') + '|'
                output += get_setting_val(aprf, 'overrideConnectionLimit')
    except Exception as e:
        logging.info("Exception during retrieving Universal Persistence profile setting: " + str(e))
    logging.info('getUniSettings(): ' + output)
    return output

def getOCSettings(mr, parPrfName):
    ocPrfs = mr.tm.ltm.profile.one_connects.get_collection()
    output = ''
    
    try:
        for aprf in ocPrfs:
            if(aprf.name == parPrfName):
                output += '/Common/'+ parPrfName + '|'
                output += get_setting_val(aprf, 'sourceMask') + '|'
                output += str(get_setting_val(aprf, 'maxSize')) + '|'
                output += str(get_setting_val(aprf, 'maxAge')) + '|'
                output += str(get_setting_val(aprf, 'maxReuse')) + '|'
                output += get_setting_val(aprf, 'idleTimeoutOverride') + '|'
                output += get_setting_val(aprf, 'limitType')
    except Exception as e:
        logging.info("Exception during retrieving OneConnect Persistence profile setting: " + str(e))
    logging.info('getOCSettings(): ' + output)
    return output


def getStreamSettings(mr, parPrfName):
    strmPrfs = mr.tm.ltm.profile.streams.get_collection()
    output = ''
    
    try:
        for aprf in strmPrfs:
            if(aprf.name == parPrfName):
                output += '/Common/'+ parPrfName + '|'
                output += get_setting_val(aprf, 'source') + '|'
                output += get_setting_val(aprf, 'tmTarget')
    except Exception as e:
        logging.info("Exception during retrieving Stream Persistence profile setting: " + str(e))
    logging.info('getStreamSettings(): ' + output)
    return output

def getPrfSettings(dev_ip, prfType, parPrfName):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    logging.info('Called getPrfSettings(): %s %s %s' % (dev_ip, prfType, parPrfName))
    
    mr = ManagementRoot(dev_ip, 'admin', 'rlatkdcks')

    output = {}

    if prfType == "DNS" :
        logging.info('getPrfSettings() DNS')
        output = getDnsPrfSettings(mr, parPrfName)
    elif prfType == "Cookie":
        output = getCookiePrfSettings(mr, parPrfName)            
    elif prfType == "DestAddrAffinity":
        output = getDstAffSettings(mr, parPrfName)
    elif prfType == "SrcAddrAffinity":
        output = getSrcAffSettings(mr, parPrfName)
    elif prfType == "Hash":
        output = getHashSettings(mr, parPrfName)
    elif prfType == "SSL":
        output = getSSLSettings(mr, parPrfName)
    elif prfType == "Universal":
        output = getUniSettings(mr, parPrfName)
    elif prfType == "FastL4":
        output = getHttpExpSettings(mr, parPrfName)
    elif prfType == "TCP":
        output = getHttpExpSettings(mr, parPrfName)
    elif prfType == "UDP":
        output = getHttpExpSettings(mr, parPrfName)
    elif prfType == "CLIENTSSL":
        output = getHttpExpSettings(mr, parPrfName)
    elif prfType == "SERVERSSL":
        output = getHttpExpSettings(mr, parPrfName)
    elif prfType == "OneConnect":
        output = getOCSettings(mr, parPrfName)
    elif prfType == "Stream":
        output = getStreamSettings(mr, parPrfName)

    return output
    #print json.dumps(output)

if __name__ == "__main__":
    # argv[1] - Device IP, argv[2] - Profile Type, argv[3] - Parent Profile Name
    print getPrfSettings(sys.argv[1], sys.argv[2], sys.argv[3])
