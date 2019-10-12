from f5.bigip import ManagementRoot
import sys
import logging

def get_poolnames(mr):
    output = ''
    poolnames = mr.tm.ltm.pools.get_collection()
    
    for apool in poolnames:
        if output != '':
            output = output + ':'
        output = output + apool.name
    logging.info('get_poolnames(): %s' % output)
    return output           

def get_pool_names(dev_ip):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    logging.info('Called get_pool_names(): %s' % (dev_ip))
    
    mr = ManagementRoot(dev_ip, 'admin', 'rlatkdcks')
    output = ''
    
    output = get_poolnames(mr)
    #logging.info('output in get_active_profiles: %s' % output)
    return output

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print get_pool_names(sys.argv[1])