from f5.bigip import ManagementRoot
import sys
import logging


def get_tcpmonitors(mr, mon_part):
    tcpmons = mr.tm.ltm.monitor.tcps.get_collection()
    output = ''
    for amon in tcpmons:
        if output != '':
            output = output + ':'
        output = output + amon.name
    #logging.info('output in get_httpprofile: %s' % output)
    return output
    
def get_httpmonitors(mr, mon_part):
    httpmons = mr.tm.ltm.monitor.https.get_collection()
    output = ''
    for amon in httpmons:
        if output != '':
            output = output + ':'
        output = output + amon.name
    #logging.info('output in get_httpprofile: %s' % output)
    return output
    
def get_httpsmonitors(mr, mon_part):
    httpsmons = mr.tm.ltm.monitor.https_s.get_collection()
    output = ''
    for amon in httpsmons:
        if output != '':
            output = output + ':'
        output = output + amon.name
    #logging.info('output in get_httpprofile: %s' % output)
    return output
    
def get_udpmonitors(mr, mon_part):
    udpmons = mr.tm.ltm.monitor.udps.get_collection()
    output = ''
    for amon in udpmons:
        if output != '':
            output = output + ':'
        output = output + amon.name
    #logging.info('output in get_httpprofile: %s' % output)
    return output
    
def get_tcphalfmonitors(mr, mon_part):
    tcphalfmons = mr.tm.ltm.monitor.tcp_half_opens.get_collection()
    output = ''
    for amon in tcphalfmons:
        if output != '':
            output = output + ':'
        output = output + amon.name
    #logging.info('output in get_httpprofile: %s' % output)
    return output
    
def get_gwicmpmonitors(mr, mon_part):
    gwicmpmons = mr.tm.ltm.monitor.gateway_icmps.get_collection()
    output = ''
    for amon in gwicmpmons:
        if output != '':
            output = output + ':'
        output = output + amon.name
    #logging.info('output in get_httpprofile: %s' % output)
    return output
    
def get_eavmonitors(mr, mon_part):
    evamons = mr.tm.ltm.monitor.externals.get_collection()
    output = ''
    for amon in evamons:
        if output != '':
            output = output + ':'
        output = output + amon.name
    #logging.info('output in get_httpprofile: %s' % output)
    return output

def get_allmonitors(mr, mon_part):
    output = ''
    output = output + get_tcpmonitors(mr) + ':' + get_httpmonitors(mr) + ':' + get_httpsmonitors(mr) + ':' + get_udpmonitors(mr) + ':' + \
    get_tcphalfmonitors(mr) + ':' + get_gwicmpmonitors(mr) + ':' + get_eavmonitors(mr)
    
    #print "all monitors: " + output
    return output
   

def get_healthmonitor_names(dev_ip, mon_type, mon_part):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    logging.info('Called get_healthmonitor_names(): %s %s' % (dev_ip, mon_type))
    
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
    if mon_type == "ALL":
        output = get_allmonitors(mr, mon_part)
    elif mon_type == "TCP":
        output = get_tcpmonitors(mr, mon_part)
    elif mon_type == "HTTP":
        output = get_httpmonitors(mr, mon_part)
    elif mon_type == "HTTPS":
        output = get_httpsmonitors(mr, mon_part)
    elif mon_type == "UDP":
        output = get_udpmonitors(mr, mon_part)
    elif mon_type == "TCP Half Open":
        output = get_tcphalfmonitors(mr, mon_part)
    elif mon_type == "GW_ICMP":
        output = get_gwicmpmonitors(mr, mon_part)
    elif mon_type == "External":
        output = get_eavmonitors(mr, mon_part)
        
    logging.info('output in get_active_profiles: %s' % output)
    return output
    

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print get_healthmonitor_names(sys.argv[1], sys.argv[2], sys.argv[3])
