from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def get_setting_val(aMon, attName):
    try:
        accessVal = 'aMon' + '.' + attName
        return eval(accessVal)
    except AttributeError:
        return ""

def get_tcpmon_setting(mr, parent_mon):
    tcpmons = mr.tm.ltm.monitor.tcps.get_collection()
    outputDict = {'interval':'', 'timeout':'', 'send':'', 'recv':'', 'reverse':'', 'aliasPort':'', 'description':'', 'defaultsFrom':''}
    for amon in tcpmons:
        if(amon.name == parent_mon):
            outputDict['interval'] = get_setting_val(amon, "interval")
            outputDict['timeout'] = get_setting_val(amon, "timeout")
            outputDict['send'] = get_setting_val(amon, "send")
            outputDict['recv'] = get_setting_val(amon, "recv")
            outputDict['reverse'] = get_setting_val(amon, "reverse")
            destIP, aliasPort = amon.destination.split(":")
            outputDict['aliasPort'] = aliasPort
            outputDict['description'] = get_setting_val(amon, "description")
            outputDict['defaultsFrom'] = get_setting_val(amon, "defaultsFrom")
    return outputDict

def get_httpmon_setting(mr, parent_mon):
    httpmons = mr.tm.ltm.monitor.https.get_collection()
    #outputDict = {'interval':'', 'timeout':'', 'send':'', 'recv':'', 'username':'', 'password': '', 'reverse':'', 'aliasPort':''}
    outputDict = {'interval':'', 'timeout':'', 'send':'', 'recv':'', 'username':'', 'password': '', 'reverse':'', 'aliasPort':'', 'description':'', 'defaultsFrom':''}
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
            outputDict['description'] = get_setting_val(amon, "description")
            outputDict['defaultsFrom'] = get_setting_val(amon, "defaultsFrom")
    return outputDict

def get_httpsmon_setting(mr, parent_mon):
    httpsmons = mr.tm.ltm.monitor.https_s.get_collection()
    outputDict = {'interval':'', 'timeout':'', 'send':'', 'recv':'', 'username':'', 'password': '', 'cipherlist':'', 'reverse':'', 'aliasPort':'', 'description':'', 'defaultsFrom':''}
    for amon in httpsmons:
        if(amon.name == parent_mon):
            outputDict['interval'] = get_setting_val(amon, "interval")
            outputDict['timeout'] = get_setting_val(amon, "timeout")
            outputDict['send'] = get_setting_val(amon, "send")
            outputDict['recv'] = get_setting_val(amon, "recv")
            outputDict['username'] = get_setting_val(amon, "username")
            outputDict['password'] = get_setting_val(amon, "password")
            outputDict['cipherlist'] = get_setting_val(amon, "cipherlist")
            outputDict['reverse'] = get_setting_val(amon, "reverse")
            destIP, aliasPort = amon.destination.split(":")
            outputDict['aliasPort'] = aliasPort
            outputDict['description'] = get_setting_val(amon, "description")
            outputDict['defaultsFrom'] = get_setting_val(amon, "defaultsFrom")            
    return outputDict

def get_udpmon_setting(mr, parent_mon):
    udpmons = mr.tm.ltm.monitor.udps.get_collection()
    outputDict = {'interval':'', 'timeout':'', 'send':'', 'recv':'', 'reverse':'', 'aliasPort':'', 'description':'', 'defaultsFrom':''}
    for amon in udpmons:
        if(amon.name == parent_mon):
            outputDict['interval'] = get_setting_val(amon, "interval")
            outputDict['timeout'] = get_setting_val(amon, "timeout")
            outputDict['send'] = get_setting_val(amon, "send")
            outputDict['recv'] = get_setting_val(amon, "recv")
            outputDict['reverse'] = get_setting_val(amon, "reverse")
            destIP, aliasPort = amon.destination.split(":")
            outputDict['aliasPort'] = aliasPort
            outputDict['description'] = get_setting_val(amon, "description")
            outputDict['defaultsFrom'] = get_setting_val(amon, "defaultsFrom")            
    return outputDict

def get_tcphalfmon_setting(mr, parent_mon):
    tcphalfmons = mr.tm.ltm.monitor.tcp_half_opens.get_collection()
    outputDict = {'interval':'', 'timeout':'', 'aliasPort':'', 'description':'', 'defaultsFrom':''}
    for amon in tcphalfmons:
        if(amon.name == parent_mon):
            outputDict['interval'] = get_setting_val(amon, "interval")
            outputDict['timeout'] = get_setting_val(amon, "timeout")
            destIP, aliasPort = amon.destination.split(":")
            outputDict['aliasPort'] = aliasPort
            outputDict['description'] = get_setting_val(amon, "description")
            outputDict['defaultsFrom'] = get_setting_val(amon, "defaultsFrom")            
    return outputDict

def get_gwicmpmon_setting(mr, parent_mon):
    pass

def get_eavmon_setting(mr, parent_mon):
    evamons = mr.tm.ltm.monitor.externals.get_collection()
    outputDict = {'interval':'', 'timeout':'', 'args':'', 'run':'', 'aliasPort':'', 'description':'', 'defaultsFrom':''}
    for amon in evamons:
        if(amon.name == parent_mon):
            outputDict['interval'] = get_setting_val(amon, "interval")
            outputDict['timeout'] = get_setting_val(amon, "timeout")
            outputDict['args'] = get_setting_val(amon, "args")
            outputDict['run'] = get_setting_val(amon, "run")
            destIP, aliasPort = amon.destination.split(":")
            outputDict['aliasPort'] = aliasPort
            outputDict['description'] = get_setting_val(amon, "description")
            outputDict['defaultsFrom'] = get_setting_val(amon, "defaultsFrom")            
    return outputDict
   

def get_healthmon_setting(active_ltm, mon_type, parent_mon):
    logger.info('Called get_healthmonitors(): %s %s %s' % (active_ltm, mon_type, parent_mon))
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)

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
    if mon_type == "TCP" :
        output = get_tcpmon_setting(mr, parent_mon)
    elif mon_type == "UDP" :
        output = get_udpmon_setting(mr, parent_mon)
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
        
    logger.info('Chosen Monitor Type: %s Return: %s' % (mon_type, output))
    print json.dumps(output)

if __name__ == "__main__":
    #logger.info('main called: param1: ')
    # argv[1] - Device IP, argv[2] - Monitor Type, argv[3] - Parent Monitor Name
    get_healthmon_setting(sys.argv[1], sys.argv[2], sys.argv[3])
