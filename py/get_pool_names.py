from f5.bigip import ManagementRoot
import sys
import logging
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def get_poolnames(mr, part_name):
    output = ''
    poolnames = mr.tm.ltm.pools.get_collection()
    
    for apool in poolnames:
        if output != '':
            output = output + ':'
        if apool.partition == part_name:
            output = output + apool.name
    logger.info('get_poolnames(): %s' % output)
    return output           

def get_pool_names(active_ltm, part_name):
    logger.info('Called get_pool_names(): %s' % active_ltm)
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    output = ''
    
    output = get_poolnames(mr, part_name)
    #logger.info('output in get_active_profiles: %s' % output)
    return output

if __name__ == "__main__":
    #logger.info('main called: param1: ')
    print get_pool_names(sys.argv[1], sys.argv[2])
