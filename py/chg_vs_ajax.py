from f5.bigip import ManagementRoot
from f5.bigip.contexts import TransactionContextManager
import sys
import logging
import json

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)


# Compare two dictionaries
# Return 'True' if two dictionaries have exactly same keys and values. Otherwise return 'False'
def Dicts_Not_Equal(first,second):
    """ return True if both do not have same length or if any keys and values are not the same """
    if len(first) == len(second): 
        for k in first:
            if first.get(k) != second.get(k,k) or k not in second:
                #print('Key: %s Value1: %s Value2: %s' % (k, first.get(k), second.get(k, k)))
                return (True)
        for k in second:         
            if first.get(k,k) != second.get(k) or k not in first:
                #print('Key: %s Value1: %s Value2: %s' % (k, first.get(k, k), second.get(k)))
                return (True)
        return (False)   
    return (True)

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
def get_vsconfig(mr, vs_name, vs_part, loaded_prf_names):

    logger.info("get_vsconfig Head")
    try:
        loaded_vs = mr.tm.ltm.virtuals.virtual.load(name=vs_name, partition=vs_part, requests_params={'params': 'expandSubcollections=true'} )

        loaded_prf_names['name'] = vs_name
        
        if hasattr(loaded_vs, 'description'):
            loaded_prf_names['description'] = loaded_vs.description
        
        ip_and_port = get_ith_name_from_partname_str(loaded_vs.destination, '/', 2)
        loaded_prf_names['ip'] = get_ith_name_from_partname_str(ip_and_port, ':', 0)
        loaded_prf_names['port'] = get_ith_name_from_partname_str(ip_and_port, ':', 1)

        # Support only Standard Virtual Server
        loaded_prf_names['ipProtocol'] = 'tcp'
        
        #Reference: loaded_prf_names = {'protocolProfileClient':'none', 'httpProfile':'none', 'oneConnectProfile':'none', 'sslProfileClient':'none',
        # 'sslProfileServer':'none', 'rules':'none', 'sourceAddressTranslation':'none', 'persistence':'none',  'policies':'none'}
    
        profs = loaded_vs.__dict__['profilesReference']['items']
        for p in profs:
            if p['nameReference']['link'].find('/profile/http') != -1:
                if p['name'] != '':
                    loaded_prf_names['httpProfile'] = p['name']
            elif p['nameReference']['link'].find('/profile/tcp') != -1 and p['context'] == 'clientside':
                if p['name'] != '':
                    loaded_prf_names['protocolProfileClient'] = p['name']
            elif p['nameReference']['link'].find('/profile/client-ssl') != -1:
                if p['name'] != '':
                    loaded_prf_names['sslProfileClient'] = p['name']
            elif p['nameReference']['link'].find('/profile/server-ssl') != -1:
                if p['name'] != '':
                    loaded_prf_names['sslProfileServer'] = p['name']

        if hasattr(loaded_vs, 'persist'):
            persistNames = loaded_vs.__dict__['persist']
            for p in persistNames:
                if p['name'] != '':
                    loaded_prf_names['persistence'] = p['name']
        
        if hasattr(loaded_vs, 'rules') and len(loaded_vs.rules) > 0:
            loaded_prf_names['rules'] = get_ith_name_from_partname_str(loaded_vs.rules[0], '/', 2)
        
        try:
            if hasattr(loaded_vs, 'sourceAddressTranslation') and loaded_vs.__dict__['sourceAddressTranslation']['type'] != 'none':
                loaded_prf_names['sourceAddressTranslation'] = get_ith_name_from_partname_str(loaded_vs.__dict__['sourceAddressTranslation']['pool'], '/', 2)
        except Exception as e:
            logger.info("Exception on Snatpool. Error: " + str(e))
            
        if hasattr(loaded_vs, 'policiesReference') and len(loaded_vs.policiesReference) > 2:
            polNames = loaded_vs.__dict__['policiesReference']['items']
            for p in polNames:
                if p['name'] != '':
                    loaded_prf_names['policies'] = p['name']

        if hasattr(loaded_vs, 'pool'):
            loaded_prf_names['pool'] = get_ith_name_from_partname_str(loaded_vs.pool, '/', 2)
    except Exception as e:
        logger.info("Exception during retrieving virtual server properties")
        logger.info("Error details: " + str(e))
        loaded_prf_names['vs_name'] = "FAIL Error message: " + str(e)
        return json.dumps(loaded_prf_names)
    
    logger.info('get_vsconfig() - All Virtual Server properties have been collected successfully\n')
    logger.info('Print get_vsconfig() Result before return\n')

    logger.info("====== Printing loaded configuration names ======")
    for k, v in loaded_prf_names.items():
        logger.info('Key: ' + k + ' Value: ' + v)
        
    return loaded_prf_names

def chg_vs_ajax(dev_ip, vs_name, vs_dest, vs_port, vs_desc, vs_tcpprofile, vs_persistence, vs_type, vs_httpprofile, vs_sslclient, vs_sslserver, vs_irule, vs_snatpool, vs_policy, vs_poolname):
    
    logger.info("chg_vs_ajax Head")
    mr = ManagementRoot(str(dev_ip), 'admin', 'rlatkdcks')

    idx = 1
    strReturn = {str(idx) : 'VS Modification Report'}
    idx += 1
    
    logger.info("Logger - Before VS Modification" + str(dev_ip) + " VS DNS:" + str(vs_name) + " VS DEST:" + str(vs_dest) + " VS PORT:" + str(vs_port) + " VS DESC:" + str(vs_desc) + " VS TCP Prf:" + str(vs_tcpprofile) + " VS Persist:" + str(vs_persistence) + " VS Type:" + str(vs_type) + " VS HTTP Prf:" + str(vs_httpprofile) + " VS Clientssl:" + str(vs_sslclient) + " VS Serverssl:" + str(vs_sslserver) + " VS iRule: " + str(vs_irule) + " VS SNATPOOL: " + str(vs_snatpool) + " VS Policy: " + str(vs_policy) + " VS Pool Name: " + str(vs_poolname))
    logger.info("VS Modification process has been initiated.")
     
    try:
        # fieldNames = VS properties collected from BIG-IP    
        fieldNames = {"name":vs_name, "description":vs_desc, "ip":vs_dest, "port":vs_port, "ipProtocol":"tcp", "pool":vs_poolname, \
        "protocolProfileClient":vs_tcpprofile, "httpProfile":vs_httpprofile, "oneConnectProfile":"none", "sslProfileClient":vs_sslclient, \
        "sslProfileServer":vs_sslserver, "rules":vs_irule, "sourceAddressTranslation":vs_snatpool, "persistence":vs_persistence,  "policies":vs_policy}
        
        logger.info("Protocol Profile: " + fieldNames["protocolProfileClient"] + " HTTP Profie: " + fieldNames["httpProfile"] + \
                     " SSL Client Profile: " + fieldNames["sslProfileClient"] + " SSL Server Profile: " + fieldNames["sslProfileServer"] +   \
                     " iRule: " + fieldNames["rules"] +   " Persistence: " + fieldNames["persistence"] +   " Policy: " + fieldNames["policies"])  

        loaded_vs = mr.tm.ltm.virtuals.virtual.load(name=fieldNames["name"], partition="Common")
        
                # Get profile names from loaded virtual server
        loaded_prf_names = {'name':'','description':'', 'ip':'', 'port':'', 'ipProtocol':'tcp','pool':'none', 'protocolProfileClient':'tcp', 'httpProfile':'none', \
                            'oneConnectProfile':'none', 'sslProfileClient':'none', 'sslProfileServer':'none', 'rules':'none', 'sourceAddressTranslation':'none', \
                            'persistence':'none',  'policies':'none'}

        get_vsconfig (mr, fieldNames['name'], 'Common', loaded_prf_names)

        if not Dicts_Not_Equal(loaded_prf_names, fieldNames):
            logger.info("Two dictionaries are SAME - No change is needed")
            strReturn = {str(idx) : 'No change is needed'}
            idx += 1
            return json.dumps(strReturn)
        
        # Print loaded vs config
        logger.info("====== Printing BIG-IP loaded configuration names after return ======")
        for k, v in loaded_prf_names.items():
            logger.info('Key: ' + k + ' Value: ' + v)
        logger.info("====== Printing GUI configuration names after return ======")
        for k, v in fieldNames.items():
            logger.info('Key: ' + k + ' Value: ' + v)

        # Create the profiles. When a virtual server is created which has a TCP 
        # base protocol then it is automatically assigned the base 'tcp' profile.
        # This profile cannot be removed without assigning some other TCP profile.
        # To do this you have to wrap the deletion of the 'tcp' profile and the
        # creation of the of the other TCP profile in a transaction.
        tx = mr.tm.transactions.transaction

        # Note - DO NOT PROCESS FURTHER IF THERE IS NOTHING TO COMMIT. Otherwise TransationContextManager will fire an error like below:
        # 404 Unexpected Error: Not Found for uri: https://192.168.144.11:443/mgmt/tm/transaction/1574570920607126/
        # Text: u'{"code":404,"message":"there is no command to commit in the transaction.","errorStack":[],"apiError":1}'

        # TransactionContextManager validate_only option - Default: False. If true, just validate(test) the changes in the context
        # TransactionContextManager(tx, validate_only=True)
        with TransactionContextManager(tx) as api:
            logger.info('#####################################')
            # Update Basic VS properties
            if loaded_prf_names['description'] != fieldNames['description']:
                logger.info("Description has been updated. Current: " + loaded_prf_names['description'] + " New: " + fieldNames['description'] )
                loaded_vs.description = fieldNames['description']
                loaded_vs.update()
            
            loaded_vs.source = '0.0.0.0/0'
            #loaded_vs.destination = '%s:%s' % (fieldNames['ip'], fieldNames['port'])
            if loaded_prf_names['ip'] != fieldNames['ip'] or loaded_prf_names['port'] != fieldNames['port']:
                loaded_vs.destination = '/Common/%s:%s' % (fieldNames['ip'], fieldNames['port'])
                logger.info("IP or Port has been updated. Current IP: " + loaded_prf_names['ip'] + " New IP: " + fieldNames['ip'] + " Current Port: " + loaded_prf_names['port'] + " New Port: " + fieldNames['port'] )
                loaded_vs.update()

            if loaded_prf_names['pool'] != fieldNames['pool']:
                loaded_vs.pool = '/Common/%s' % fieldNames['pool']
                logger.info("Pool has been updated. Current: " + loaded_prf_names['pool'] + " New: " + fieldNames['pool'])
                loaded_vs.update()
            
            # Update http profile
            if loaded_prf_names['httpProfile'] !=  fieldNames['httpProfile']:
                # Update VS profile - Delete and then add
                loaded_httpprf = loaded_vs.profiles_s.profiles.load(partition='Common', name=loaded_prf_names['httpProfile'])
                loaded_httpprf.delete()
                loaded_vs.profiles_s.profiles.create(name=fieldNames['httpProfile'], partition='Common')
                loaded_vs.update()
                #update_httpprf = { 'name':fieldNames['httpProfile']}
                logger.info("HTTP Profile has been updated. Current: " + loaded_prf_names['httpProfile'] + " New: " + fieldNames['httpProfile'] )
                #pprint.pprint(loaded_httpprf.raw)
            #else:
                #print("HTTP Profile is NOT updated.  Current: %s New: %s" % (loaded_prf_names['httpProfile'],fieldNames['httpProfile'] ))
            
            # Update tcp client profile
            if loaded_prf_names['protocolProfileClient'] !=  fieldNames['protocolProfileClient']:
                # Update TCP profile - Delete and then add
                #loaded_tcpprf = loaded_vs.profiles_s.profiles.load(partition='Common', name=loaded_prf_names['protocolProfileClient'], context='clientside')
                loaded_tcpprf = loaded_vs.profiles_s.profiles.load(partition='Common', name=loaded_prf_names['protocolProfileClient'])
                loaded_tcpprf.delete()
                loaded_vs.profiles_s.profiles.create(name=fieldNames['protocolProfileClient'], partition='Common', context='clientside')
                loaded_vs.update()
                logger.info("TCP Profile has been updated. Current: " + loaded_prf_names['protocolProfileClient'] + " New: " + fieldNames['protocolProfileClient'])
                #pprint.pprint(loaded_tcpprf.raw)
            #else:
                #print("TCP Profile is NOT updated.  Current: %s New: %s" % (loaded_prf_names['protocolProfileClient'],fieldNames['protocolProfileClient'] ))

            # Update ssl client profile
            if loaded_prf_names['sslProfileClient'] !=  fieldNames['sslProfileClient']:
                # Update Client SSL profile - Delete and then add
                #loaded_sslcliprf = loaded_vs.profiles_s.profiles.load(partition='Common', name=loaded_prf_names['sslProfileClient'], context='clientside')
                loaded_sslcliprf = loaded_vs.profiles_s.profiles.load(partition='Common', name=loaded_prf_names['sslProfileClient'])
                loaded_sslcliprf.delete()
                loaded_vs.profiles_s.profiles.create(name=fieldNames['sslProfileClient'], partition='Common', context='clientside')
                loaded_vs.update()
                logger.info("SSL Client Profile has been updated. Current: " + loaded_prf_names['sslProfileClient'] + " New: " + fieldNames['sslProfileClient'] )
                #pprint.pprint(loaded_sslcliprf.raw)
            #else:
                #print("SSL Client Profile is NOT updated.  Current: %s New: %s" % (loaded_prf_names['sslProfileClient'],fieldNames['sslProfileClient'] ))

            # Update ssl server profile
            if loaded_prf_names['sslProfileServer'] !=  fieldNames['sslProfileServer']:
                # Update Server SSL profile - Delete and then add
                #loaded_sslsrvprf = loaded_vs.profiles_s.profiles.load(partition='Common', name=loaded_prf_names['sslProfileServer'], context='serverside')
                loaded_sslsrvprf = loaded_vs.profiles_s.profiles.load(partition='Common', name=loaded_prf_names['sslProfileServer'])
                loaded_sslsrvprf.delete()
                loaded_vs.profiles_s.profiles.create(name=fieldNames['sslProfileServer'], partition='Common', context='serverside')
                loaded_vs.update()
                logger.info("SSL Server Profile has been updated. Current: " + loaded_prf_names['sslProfileServer'] + " New: " + fieldNames['sslProfileServer'] )
                #pprint.pprint(loaded_sslsrvprf.raw)
            #else:
                #print("SSL Server Profile is NOT updated.  Current: %s New: %s" % (loaded_prf_names['sslProfileServer'],fieldNames['sslProfileServer'] ))

            # Update Persistence profile
            if loaded_prf_names['persistence'] !=  fieldNames['persistence']:
                # Update Persistence profile - Prep persistence setting and then update
                logger.info("Persistence has been updated. Current: " + loaded_prf_names['persistence'] + " New: " + fieldNames['persistence'] )
                loaded_vs.persist = [{'name':fieldNames['persistence'], 'partition':'Common'}]
                loaded_vs.update()
                
            # Update iRule
            if loaded_prf_names['rules'] !=  fieldNames['rules']:
                # Update Persistence profile - Prep persistence setting and then update
                logger.info("iRule has been updated. Current: " + loaded_prf_names['rules'] + " New: " + fieldNames['rules'] )
                rule_name = '/Common/%s' % fieldNames['rules']
                loaded_vs.rules = [rule_name]
                loaded_vs.update()
                
            # Update Policy profile            
            if loaded_prf_names['policies'] !=  fieldNames['policies']:
                # Update Policy profile - Delete and then add
                logger.info("Policy has been updated. Current: " + loaded_prf_names['policies'] + " New: " + fieldNames['policies'] )
                loaded_pol = loaded_vs.policies_s.policies.load(partition='Common', name=loaded_prf_names['policies'])
                loaded_pol.delete()
                loaded_vs.policies_s.policies.create(name=fieldNames['policies'], partition='Common')
                loaded_vs.update()

            # Update SNAT Pool            
            if loaded_prf_names['sourceAddressTranslation'] !=  fieldNames['sourceAddressTranslation']:
                # Update SNAT Pool
                logger.info("SNAT Pool has been updated. Current: " + loaded_prf_names['sourceAddressTranslation'] + " New: " + fieldNames['sourceAddressTranslation'] )
                snatpool_name = '/Common/%s' % fieldNames['sourceAddressTranslation']
                loaded_vs.sourceAddressTranslation = {'pool':snatpool_name, 'type':'snat'}
                loaded_vs.update()                
                
    except Exception as e:
        logger.info("Error during updating virtual server properties")
        logger.info("Error Details: " + str(e))
        strReturn = {str(idx) : 'Error during updating virtual server properties Error Detail: ' + str(e) }
        idx += 1
        return json.dumps(strReturn)
    
    logger.info("Virtual Server has been updated successfully")    
    strReturn = {str(idx) : 'Virtual Server has been updated successfully' }
    idx += 1

    return json.dumps(strReturn)


if __name__ == "__main__":
    logger.info("chg_vs_ajax.py logging has been started")
    print chg_vs_ajax(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14], sys.argv[15])
