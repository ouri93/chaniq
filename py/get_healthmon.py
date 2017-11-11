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
    
def get_httpmonitors(mr):
    httpmons = mr.tm.ltm.monitor.https.get_collection()
    output = ''
    for amon in httpmons:
        if output != '':
            output = output + ':'
        output = output + amon.name
    #logging.info('output in get_httpprofile: %s' % output)
    return output
    
def get_httpsmonitors(mr):
    httpsmons = mr.tm.ltm.monitor.https_s.get_collection()
    output = ''
    for amon in httpsmons:
        if output != '':
            output = output + ':'
        output = output + amon.name
    #logging.info('output in get_httpprofile: %s' % output)
    return output
    
def get_udpmonitors(mr):
    udpmons = mr.tm.ltm.monitor.udps.get_collection()
    output = ''
    for amon in udpmons:
        if output != '':
            output = output + ':'
        output = output + amon.name
    #logging.info('output in get_httpprofile: %s' % output)
    return output
    
def get_tcphalfmonitors(mr):
    tcphalfmons = mr.tm.ltm.monitor.tcp_half_opens.get_collection()
    output = ''
    for amon in tcphalfmons:
        if output != '':
            output = output + ':'
        output = output + amon.name
    #logging.info('output in get_httpprofile: %s' % output)
    return output
    
def get_gwicmpmonitors(mr):
    gwicmpmons = mr.tm.ltm.monitor.gateway_icmps.get_collection()
    output = ''
    for amon in gwicmpmons:
        if output != '':
            output = output + ':'
        output = output + amon.name
    #logging.info('output in get_httpprofile: %s' % output)
    return output
    
def get_eavmonitors(mr):
    evamons = mr.tm.ltm.monitor.externals.get_collection()
    output = ''
    for amon in evamons:
        if output != '':
            output = output + ':'
        output = output + amon.name
    #logging.info('output in get_httpprofile: %s' % output)
    return output

def get_allmonitors(mr):
    output = ''
    output = output + get_tcpmonitors(mr) + ':' + get_httpmonitors(mr) + ':' + get_httpsmonitors(mr) + ':' + get_udpmonitors(mr) + ':' + \
    get_tcphalfmonitors(mr) + ':' + get_gwicmpmonitors(mr) + ':' + get_eavmonitors(mr)
    
    #print "all monitors: " + output
    return output
   

def get_healthmonitors(dev_ip, mon_type):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    logging.info('Called get_healthmonitors(): %s %s' % (dev_ip, mon_type))
    
    mr = ManagementRoot('192.168.80.150', 'admin', 'rlatkdcks')
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
        output = get_allmonitors(mr)
    elif mon_type == "TCP":
        output = get_tcpmonitors(mr)
    elif mon_type == "HTTP":
        output = get_httpmonitors(mr)
    elif mon_type == "HTTPS":
        output = get_httpsmonitors(mr)
    elif mon_type == "UDP":
        output = get_udpmonitors(mr)
    elif mon_type == "TCP_HALF":
        output = get_tcphalfmonitors(mr)
    elif mon_type == "GW_ICMP":
        output = get_gwicmpmonitors(mr)
    elif mon_type == "EAV":
        output = get_eavmonitors(mr)
        
    #logging.info('output in get_active_profiles: %s' % output)
    return output

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print get_healthmonitors(sys.argv[1], sys.argv[2])
