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
    

def getPrfSettings(dev_ip, prfType, parPrfName):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    logging.info('Called getPrfSettings(): %s %s %s' % (dev_ip, prfType, parPrfName))
    
    mr = ManagementRoot(dev_ip, 'admin', 'rlatkdcks')

    output = {}

    if prfType == "DNS" :
        logging.info('getPrfSettings() DNS')
        output = getDnsPrfSettings(mr, parPrfName)
    elif prfType == "Cookie":
        output = getHttpExpSettings(mr, parPrfName)            
    elif prfType == "DestAddrAffinity":
        output = getHttpExpSettings(mr, parPrfName)
    elif prfType == "SrcAddrAffinity":
        output = getHttpExpSettings(mr, parPrfName)
    elif prfType == "Hash":
        output = getHttpExpSettings(mr, parPrfName)
    elif prfType == "SSL":
        output = getHttpExpSettings(mr, parPrfName)
    elif prfType == "Universal":
        output = getHttpExpSettings(mr, parPrfName)
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
        output = getHttpExpSettings(mr, parPrfName)
    elif prfType == "Stream":
        output = getHttpExpSettings(mr, parPrfName)

    return output
    #print json.dumps(output)

if __name__ == "__main__":
    # argv[1] - Device IP, argv[2] - Profile Type, argv[3] - Parent Profile Name
    print getPrfSettings(sys.argv[1], sys.argv[2], sys.argv[3])
