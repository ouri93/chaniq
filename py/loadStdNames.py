import sys
import logging
import ConfigParser
import traceback
import chaniq_util

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

# Read ini Config option of USE_STD_NAME value under USE_STD_NAMING section from config/chaniq.ini
# Return: String '0'(default) for no Standard Naming and '1' to use Standard naming
def useStdNaming():
    
    config = ConfigParser.ConfigParser()
    try:
        config.read('/var/www/chaniq/config/chaniq.ini')
    except Exception as e:
        logging.info("File Read error: " + str(e))
    
    return config.get('USE_STD_NAMING', 'USE_STD_NAME')

# dev_ip: BIG-IP IP address
# obj_type: LOCAL - Device specific objects, SHARED - Shared objects
# obj_id: Key part of BIGIP_LOCAL_OBJ_ID section such as VIRTUAL_SERVER, POOL, SNAT_POOL, ...
#     [BIGIP_LOCAL_OBJ_ID]
#     VIRTUAL_SERVER = VS
#     POOL = P
#     SNAT_POOL = SNATP
#     SNAT_LIST = SNATL
#     NODE = N
#     ROUTE_DOMAIN = RD
#     
#     [BIGIP_SHRD_OBJ_ID]
#     PROFILES = PR
#     IRULE = IR
#     MONITOR = MON
#     TRAFFIC_POLICY = TPOL
#     CERTIFICATE = CERT
# obj_subtype: If obj_id is PR or MON, there are subtypes. Otherwise obj_subtype is empty string ("")
# desc: User defined description

def get_std_name(dev_ip, obj_type, obj_id, obj_subtype, desc):
    
    stdNameIniFile = chaniq_util.loadIniConfigVal('CONFIG_PATH_INFO','STD_NAME_INI_PATH') + 'StandardNaming.ini'
    logging.info('INI full path returned: ' + stdNameIniFile)
    # Read DB name, DB Admin name and Password
    config = ConfigParser.ConfigParser()
    
    try:
        config.read(stdNameIniFile)
        logging.info('Sections in INI Config read: ' + str(config.sections()))
    except Exception as e:
        logging.info("File Read error: " + str(e))
    logging.info('INI file has been read. Object Type: ' + obj_type)
    
    try:
        if obj_type == 'LOCAL':
            dev_prefix = config.get('PREFIX_PER_DEVICE', dev_ip)
            local_part_name = config.get('BIGIP_LOCAL_OBJ_ID', obj_id)
            local_part_name = dev_prefix + '_' + local_part_name
        elif obj_type == 'SHARED':
            logging.info('SHARED Object Type Name buidling process starts')
            local_part_name = config.get('BIGIP_SHRD_OBJ_ID', obj_id)
            logging.info('SHARED Object Type Name buidling process local_part_name from INI: ' + local_part_name)
            subtype_name = ''
            if obj_id == 'PROFILE':
                subtype_name = config.get('SUBTYPE_PROFILE', obj_subtype)
            elif obj_id == 'MONITOR':
                subtype_name = config.get('SUBTYPE_MONITOR', obj_subtype)
            if subtype_name != '':
                local_part_name = local_part_name + '_' + subtype_name
            logging.info('SHARED Object Type Name buidling process final local_part_name: ' + local_part_name)
    except Exception as e:
        logging.info("Config Read through config.get() failed: " + str(e))
        
    logging.info('Standard Name crated: ' + local_part_name + '_' + desc) 
    
    return local_part_name + '_' + desc