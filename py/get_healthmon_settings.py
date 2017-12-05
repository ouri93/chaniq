from f5.bigip import ManagementRoot
import sys
import logging
import json

def get_setting_val(aMon, attName):
    try:
        accessVal = 'aMon' + '.' + attName
        return eval(accessVal)
    except AttributeError:
        return ""

def get_tcpmon_setting(mr, parent_mon):
    tcpmons = mr.tm.ltm.monitor.tcps.get_collection()
    outputDict = {'interval':'', 'timeout':'', 'send':'', 'recv':'', 'reverse':'', 'aliasPort':''}
    for amon in tcpmons:
        if(amon.name == parent_mon):
            outputDict['interval'] = get_setting_val(amon, "interval")
            outputDict['timeout'] = get_setting_val(amon, "timeout")
            outputDict['send'] = get_setting_val(amon, "send")
            outputDict['recv'] = get_setting_val(amon, "recv")
            outputDict['reverse'] = get_setting_val(amon, "reverse")
            destIP, aliasPort = amon.destination.split(":")
            outputDict['aliasPort'] = aliasPort
    return outputDict

def get_httpmon_setting(mr, parent_mon):
    httpmons = mr.tm.ltm.monitor.https.get_collection()
    outputDict = {'interval':'', 'timeout':'', 'send':'', 'recv':'', 'username':'', 'password': '', 'reverse':'', 'aliasPort':''}
    for amon in httpmons:
        if(amon.name == parent_mon):
            outputDict['interval'] = get_setting_val(amon, "interval")
            outputDict['timeout'] = get_setting_val(amon, "timeout")
            outputDict['send'] = get_setting_val(amon, "send")
            outputDict['recv'] = get_setting_val(amon, "recv")
            outputDict['username'] = get_setting_val(amon, "username")
            outputDict['password'] = get_setting_val(amon, "password")
            outputDict['reverse'] = get_setting_val(amon, "reverse")
            destIP, aliasPort = amon.destination.split(":")
            outputDict['aliasPort'] = aliasPort
    return outputDict

def get_httpsmon_setting(mr, parent_mon):
    httpsmons = mr.tm.ltm.monitor.https_s.get_collection()
    outputDict = {'interval':'', 'timeout':'', 'send':'', 'recv':'', 'username':'', 'password': '', 'cipherlist':'', 'reverse':'', 'aliasPort':''}
    for amon in httpsmons:
        if(amon.name == parent_mon):
            outputDict['interval'] = get_setting_val(amon, "interval")
            outputDict['timeout'] = get_setting_val(amon, "timeout")
            outputDict['send'] = get_setting_val(amon, "send")
            outputDict['recv'] = get_setting_val(amon, "recv")
            outputDict['username'] = get_setting_val(amon, "username")
            outputDict['password'] = get_setting_val(amon, "cipherlist")
            outputDict['cipherlist'] = get_setting_val(amon, "password")
            outputDict['reverse'] = get_setting_val(amon, "reverse")
            destIP, aliasPort = amon.destination.split(":")
            outputDict['aliasPort'] = aliasPort
    return outputDict

def get_udpmon_setting(mr, parent_mon):
    pass

def get_tcphalfmon_setting(mr, parent_mon):
    tcphalfmons = mr.tm.ltm.monitor.tcp_half_opens.get_collection()
    outputDict = {'interval':'', 'timeout':'', 'aliasPort':''}
    for amon in tcphalfmons:
        if(amon.name == parent_mon):
            outputDict['interval'] = get_setting_val(amon, "interval")
            outputDict['timeout'] = get_setting_val(amon, "timeout")
            destIP, aliasPort = amon.destination.split(":")
            outputDict['aliasPort'] = aliasPort
    return outputDict

def get_gwicmpmon_setting(mr, parent_mon):
    pass

def get_eavmon_setting(mr, parent_mon):
    evamons = mr.tm.ltm.monitor.externals.get_collection()
    outputDict = {'interval':'', 'timeout':'', 'args':'', 'run':'', 'aliasPort':''}
    for amon in evamons:
        if(amon.name == parent_mon):
            outputDict['interval'] = get_setting_val(amon, "interval")
            outputDict['timeout'] = get_setting_val(amon, "timeout")
            outputDict['args'] = get_setting_val(amon, "args")
            outputDict['run'] = get_setting_val(amon, "run")
            destIP, aliasPort = amon.destination.split(":")
            outputDict['aliasPort'] = aliasPort
    return outputDict
   

def get_healthmon_setting(dev_ip, mon_type, parent_mon):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    logging.info('Called get_healthmonitors(): %s %s %s' % (dev_ip, mon_type, parent_mon))
    
    mr = ManagementRoot(dev_ip, 'admin', 'rlatkdcks')

    output = {}
    '''
    Suppported Health Monitor types
    1. TCP
    2. HTTP and HTTPS
    3. UDP
    4. TCP Half Open
    5. Gateway ICMP
    6. External
    '''
    if mon_type == "TCP" or mon_type == "UDP" :
        output = get_tcpmon_setting(mr, parent_mon)
    elif mon_type == "HTTP":
        output = get_httpmon_setting(mr, parent_mon)
    elif mon_type == "HTTPS":
        output = get_httpsmon_setting(mr, parent_mon)
    elif mon_type == "TCP Half Open":
        output = get_tcphalfmon_setting(mr, parent_mon)
    elif mon_type == "GW_ICMP":
        output = get_gwicmpmon_setting(mr, parent_mon)
    elif mon_type == "External":
        output = get_eavmon_setting(mr, parent_mon)
        
    logging.info('Chosen Monitor Type: %s Return: %s' % (mon_type, output))
    print json.dumps(output)

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    # argv[1] - Device IP, argv[2] - Monitor Type, argv[3] - Parent Monitor Name
    get_healthmon_setting(sys.argv[1], sys.argv[2], sys.argv[3])
