from f5.bigip import ManagementRoot
import sys
import logging
import json

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)

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
    logging.info("Here -1")
    output = {'vs_name':'', 'vs_desc':'', 'vs_dest':'', 'vs_port':'', 'vs_type':'', 'vs_tcpprofile':'none', 'vs_persist':'none', 'vs_irule':'none',\
               'vs_snatpool':'none', 'vs_policy':'none', 'vs_httpprf':'none', 'vs_clisslprf':'none', 'vs_srvsslprf':'none', 'vs_poolname':'none'}
    
    logging.info("Here0")
    output['vs_name'] = vs_name
    try:
        logging.info("Here1")
        loaded_vs = mr.tm.ltm.virtuals.virtual.load(name=vs_name, partition=vs_part, requests_params={'params': 'expandSubcollections=true'} )
        logging.info("Here2")
        if hasattr(loaded_vs, 'description'):
            output['vs_desc'] = loaded_vs.description
        
        logging.info("Here3")
        ip_and_port = get_ith_name_from_partname_str(loaded_vs.destination, '/', 2)
        output['vs_dest'] = get_ith_name_from_partname_str(ip_and_port, ':', 0)
        output['vs_port'] = get_ith_name_from_partname_str(ip_and_port, ':', 1)
        # Support only Standard Virtual Server
        output['vs_type'] = 'Standard'
        logging.info("Here4")
        profs = loaded_vs.__dict__['profilesReference']['items']
        logging.info("Here5")
        for p in profs:
            if p['nameReference']['link'].find('/profile/http') != -1:
                if p['name'] != '':
                    output['vs_httpprf'] = p['name']
            elif p['nameReference']['link'].find('/profile/tcp') != -1 and p['context'] == 'clientside':
                if p['name'] != '':
                    output['vs_tcpprofile'] = p['name']
            elif p['nameReference']['link'].find('/profile/client-ssl') != -1:
                if p['name'] != '':
                    output['vs_clisslprf'] = p['name']
            elif p['nameReference']['link'].find('/profile/server-ssl') != -1:
                if p['name'] != '':
                    output['vs_srvsslprf'] = p['name']
        logging.info("Here6 - Looping for each profile")
        if hasattr(loaded_vs, 'persist'):
            persistNames = loaded_vs.__dict__['persist']
            logging.info("Here7")
            for p in persistNames:
                if p['name'] != '':
                    output['vs_persist'] = p['name']
        
        if hasattr(loaded_vs, 'rules') and len(loaded_vs.rules) > 0:
            output['vs_irule'] = get_ith_name_from_partname_str(loaded_vs.rules[0], '/', 2)
        logging.info("Here9")
        
        try:
            if hasattr(loaded_vs, 'sourceAddressTranslation') and loaded_vs.__dict__['sourceAddressTranslation']['type'] != 'none':
                output['vs_snatpool'] = get_ith_name_from_partname_str(loaded_vs.__dict__['sourceAddressTranslation']['pool'], '/', 2)
        except Exception as e:
            logging.info("Exception on Snatpool. Error: " + str(e))
            
        logging.info("Here10")
        if hasattr(loaded_vs, 'policiesReference') and len(loaded_vs.policiesReference) > 2:
            polNames = loaded_vs.__dict__['policiesReference']['items']
            for p in polNames:
                if p['name'] != '':
                    output['vs_policy'] = p['name']

        logging.info("Here11")
        if hasattr(loaded_vs, 'pool'):
            output['vs_poolname'] = get_ith_name_from_partname_str(loaded_vs.pool, '/', 2)
    except Exception as e:
        logging.info("Exception during retrieving virtual server properties")
        logging.info("Error details: " + str(e))
        output['vs_name'] = "FAIL Error message: " + str(e)
        return json.dumps(output)
    
    logging.info('get_vsconfig() - All Virtual Server properties have been collected successfully\n')
    logging.info('Print get_vsconfig() Result before return\n')
    for k, v in output.items():
        logging.info( k + ":" + v)
    return output           

def get_vs_config(dev_ip, vs_name, vs_part):
    # ID list: vs_desc, vs_dest, vs_port, vs_type, vs_tcpprofile, vs_persist, vs_irule, vs_snatpool, 
    # vs_policy, vs_httpprf, vs_clisslprf, vs_srvsslprf, chg_vs_pool_chosen
    logging.info('Called get_vs_config(): IP: ' + dev_ip + ' VS name: ' + vs_name + ' VS Partition: ' + vs_part)
    
    try:
        mr = ManagementRoot(dev_ip, 'admin', 'rlatkdcks')
    except Exception as e:
        logging.info("Exception fired during loading mgmt root")
        logging.info("Error Details: " + str(e))
                  
    output = get_vsconfig(mr, vs_name, vs_part)
    #logging.info('output in get_active_profiles: %s' % output)
    return json.dumps(output)

if __name__ == "__main__":
    logging.info('main called: param1: ')
    print get_vs_config(sys.argv[1], sys.argv[2], sys.argv[3])
