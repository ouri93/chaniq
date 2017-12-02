from f5.bigip import ManagementRoot
import sys
import logging


def get_tcpmonitors(mr):
    tcpmons = mr.tm.ltm.monitor.tcps.get_collection()
    output = ''
    for amon in tcpmons:
        if output != '':
            output = output + ':'
        output = output + amon.name
    #logging.info('output in get_httpprofile: %s' % output)
    return output

def get_tcpmon_setting(mr, parent_mon):
    pass

def get_httpmon_setting(mr, parent_mon):
    pass

def get_httpsmon_setting(mr, parent_mon):
    pass

def get_udpmon_setting(mr, parent_mon):
    pass

def get_tcphalfmon_setting(mr, parent_mon):
    pass

def get_gwicmpmon_setting(mr, parent_mon):
    pass

def get_eavmon_setting(mr, parent_mon):
    pass   

def get_healthmon_setting(dev_ip, mon_type, parent_mon):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    logging.info('Called get_healthmonitors(): %s %s' % (dev_ip, mon_type))
    
    mr = ManagementRoot(dev_ip, 'admin', 'rlatkdcks')
    output = ''
    '''
    Suppported Health Monitor types
    1. TCP
    2. HTTP and HTTPS
    3. UDP
    4. TCP Half_open
    5. Gateway ICMP
    6. External
    '''
    if mon_type == "TCP":
        output = get_tcpmon_setting(mr, parent_mon)
    elif mon_type == "HTTP":
        output = get_httpmon_setting(mr, parent_mon)
    elif mon_type == "HTTPS":
        output = get_httpsmon_setting(mr, parent_mon)
    elif mon_type == "UDP":
        output = get_udpmon_setting(mr, parent_mon)
    elif mon_type == "TCP_HALF":
        output = get_tcphalfmon_setting(mr, parent_mon)
    elif mon_type == "GW_ICMP":
        output = get_gwicmpmon_setting(mr, parent_mon)
    elif mon_type == "EAV":
        output = get_eavmon_setting(mr, parent_mon)
        
    #logging.info('output in get_active_profiles: %s' % output)
    return output

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    # argv[1] - Device IP, argv[2] - Monitor Type, argv[3] - Parent Monitor Name
    print get_healthmon_setting(sys.argv[1], sys.argv[2], sys.argv[3])
