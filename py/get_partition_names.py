from f5.bigip import ManagementRoot
import sys
import logging
import traceback
import getpass

def get_partition_names(active_ltm):
    logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    logging.info('Called get_partition_names() Dev IP: %s' % (active_ltm))
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    output = ''
    
    logging.info('get_names() called')
    '''
    Error with partition_list = mr.tm.auth.partitions.get_collection()
    - With direct Python code, mr.tm.auth.partitions.get_collection() code works well. However in some reason, here it causes below error
    INFO:root:Traceback (most recent call last):
        File "/var/www/chaniq/py/get_partition_names.py", line 15, in get_partition_names
            partition_list = mr.tm.auth.partitions.get_collection()
        File "/usr/local/lib/python2.7/dist-packages/f5/bigip/mixins.py", line 102, in __getattr__
            raise AttributeError(error_message)
    AttributeError: '<class 'f5.bigip.tm.auth.Auth'>' object has no attribute 'partitions'
    '''
    try:
        for folder in mr.tm.sys.folders.get_collection():
            if not folder.name == "/" and not folder.name =="Drafts" and not folder.name == "Common" and not folder.name.endswith(".app"):
                output = output + folder.name + ':'
    except Exception as e:
        logging.info("error during retrieving partition name")
        logging.info("Error details: " + str(e))
        logging.info(traceback.format_exc())
    logging.info('Partition names(): %s' % (output))
    
    return output

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
    #logging.info('main called: param1: ')
    print get_partition_names(sys.argv[1])
