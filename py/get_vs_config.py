from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

# mixedStr format - "/Common/name_of_object"
# ith: Array index of returning object
# get_ith_name_from_partname_str ("/Common/name_of_object", "/", 2) will return name_of_object
def get_ith_name_from_partname_str (mixedStr, sepStr, ith):
    rtnVal =mixedStr.split(sepStr)[ith] 
    if  rtnVal != '':
        return rtnVal
    else:
        return 'none'

'''
Ref: https://devcentral.f5.com/s/question/0D51T00006i7jCs/trying-to-find-virtual-server-type-through-python-sdk
To see all properties of a virtual server, use 'requests_params={'params': 'expandSubcollections=true'}' so that you can
see all subcollections and their properties
'''
def get_vsconfig(mr, vs_name, vs_part):
    output = {'vs_name':'', 'vs_desc':'', 'vs_dest':'', 'vs_port':'', 'vs_type':'', 'vs_tcpprofile':'none', 'vs_persist':'none', 'vs_irule':'none',\
               'vs_snatpool':'none', 'vs_policy':'none', 'vs_httpprf':'none', 'vs_clisslprf':'none', 'vs_srvsslprf':'none', 'vs_poolname':'none'}

    output['vs_name'] = vs_name
    try:
        loaded_vs = mr.tm.ltm.virtuals.virtual.load(name=vs_name, partition=vs_part, requests_params={'params': 'expandSubcollections=true'} )
        if hasattr(loaded_vs, 'description'):
            output['vs_desc'] = loaded_vs.description
        
        ip_and_port = get_ith_name_from_partname_str(loaded_vs.destination, '/', 2)
        output['vs_dest'] = get_ith_name_from_partname_str(ip_and_port, ':', 0)
        output['vs_port'] = get_ith_name_from_partname_str(ip_and_port, ':', 1)
        # Support only Standard Virtual Server
        output['vs_type'] = 'Standard'
        profs = loaded_vs.__dict__['profilesReference']['items']
        for p in profs:
            if p['nameReference']['link'].find('/profile/http') != -1:
                if p['name'] != '':
                    output['vs_httpprf'] = p['name']
                    logger.info("Loaded http prf name: " + p['name'])
            elif p['nameReference']['link'].find('/profile/tcp') != -1 and (p['context'] == 'clientside' or p['context'] == 'all'):
                if p['name'] != '':
                    output['vs_tcpprofile'] = p['name']
                    logger.info("Loaded TCP prf name: " + p['name'])
            elif p['nameReference']['link'].find('/profile/client-ssl') != -1 and p['context'] == 'clientside' :
                if p['name'] != '':
                    output['vs_clisslprf'] = p['name']
                    logger.info("Loaded client ssl prf name: " + p['name'])
            elif p['nameReference']['link'].find('/profile/server-ssl') != -1 and p['context'] == 'serverside' :
                if p['name'] != '':
                    output['vs_srvsslprf'] = p['name']
                    logger.info("Loaded server ssl prf name: " + p['name'])

        if hasattr(loaded_vs, 'persist'):
            persistNames = loaded_vs.__dict__['persist']
            for p in persistNames:
                if p['name'] != '':
                    output['vs_persist'] = p['name']
        
        if hasattr(loaded_vs, 'rules') and len(loaded_vs.rules) > 0:
            output['vs_irule'] = get_ith_name_from_partname_str(loaded_vs.rules[0], '/', 2)
        
        try:
            if hasattr(loaded_vs, 'sourceAddressTranslation') and loaded_vs.__dict__['sourceAddressTranslation']['type'] != 'none':
                output['vs_snatpool'] = get_ith_name_from_partname_str(loaded_vs.__dict__['sourceAddressTranslation']['pool'], '/', 2)
        except Exception as e:
            logger.info("Exception on Snatpool. Error: " + str(e))
            
        if hasattr(loaded_vs, 'policiesReference') and len(loaded_vs.policiesReference) > 2:
            polNames = loaded_vs.__dict__['policiesReference']['items']
            for p in polNames:
                if p['name'] != '':
                    output['vs_policy'] = p['name']

        if hasattr(loaded_vs, 'pool'):
            output['vs_poolname'] = get_ith_name_from_partname_str(loaded_vs.pool, '/', 2)
    except Exception as e:
        logger.info("Exception during retrieving virtual server properties")
        logger.info("Error details: " + str(e))
        output['vs_name'] = "FAIL Error message: " + str(e)
        return json.dumps(output)
    
    logger.info('get_vsconfig() - All Virtual Server properties have been collected successfully\n')
    logger.info('Print get_vsconfig() Result before return\n')
    for k, v in output.items():
        logger.info( k + ":" + v)
    return output           

def get_vs_config(active_ltm, vs_name, vs_part):
    # ID list: vs_desc, vs_dest, vs_port, vs_type, vs_tcpprofile, vs_persist, vs_irule, vs_snatpool, 
    # vs_policy, vs_httpprf, vs_clisslprf, vs_srvsslprf, chg_vs_pool_chosen
    logger.info('Called get_vs_config(): IP: ' + active_ltm + ' VS name: ' + vs_name + ' VS Partition: ' + vs_part)
    
    try:
        admpass = getpass.getpass('LTM', 'admin')
        mr = ManagementRoot(str(active_ltm), 'admin', admpass)
        #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    except Exception as e:
        logger.info("Exception fired during loading mgmt root")
        logger.info("Error Details: " + str(e))
                  
    output = get_vsconfig(mr, vs_name, vs_part)
    #logger.info('output in get_active_profiles: %s' % output)
    return json.dumps(output)

if __name__ == "__main__":
    logger.info('main called: param1: ')
    print get_vs_config(sys.argv[1], sys.argv[2], sys.argv[3])
