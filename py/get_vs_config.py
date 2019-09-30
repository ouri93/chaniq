from f5.bigip import ManagementRoot
import sys
import logging

def get_vsconfig(mr, vs_name):
    output = ''
    poolnames = mr.tm.ltm.pools.get_collection()
    
    for apool in poolnames:
        if output != '':
            output = output + ':'
        output = output + apool.name
    logging.info('get_vsconfig(): %s' % output)
    return output           

def get_vs_config(dev_ip, vs_name):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    logging.info('Called get_vs_config(): %s %s' % (dev_ip, vs_name))
    
    mr = ManagementRoot(dev_ip, 'admin', 'rlatkdcks')
    output = ''
    
    # Rest URL: https://192.168.144.11/mgmt/tm/ltm/virtual/STANDALONE_VS_www8.home.local_443
    fieldNames = {"name":'std_vsname'}
                  
    output = get_vsconfig(mr, vs_name)
    #logging.info('output in get_active_profiles: %s' % output)
    return output

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print get_vs_config(sys.argv[1], sys.argv[2])
