from f5.bigip import ManagementRoot
from f5.bigip.contexts import TransactionContextManager
import sys
import logging
import json
import getpass
import traceback
from _ast import Or

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
                    logging.info("Loaded http prf name: " + p['name'])
            elif p['nameReference']['link'].find('/profile/tcp') != -1 and (p['context'] == 'clientside' or p['context'] == 'all') :
                logger.info("Loading TCP Profile(p['name']: " + p['name'])
                if p['name'] != '':
                    loaded_prf_names['protocolProfileClient'] = p['name']
                    logging.info("Loaded tcp prf name: " + p['name'])
            elif p['nameReference']['link'].find('/profile/client-ssl') != -1 and p['context'] == 'clientside' :
                if p['name'] != '':
                    loaded_prf_names['sslProfileClient'] = p['name']
                    logging.info("Loaded client ssl prf name: " + p['name'])
            elif p['nameReference']['link'].find('/profile/server-ssl') != -1 and p['context'] == 'serverside' :
                if p['name'] != '':
                    loaded_prf_names['sslProfileServer'] = p['name']
                    logging.info("Loaded server ssl prf name: " + p['name'])

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

def chg_vs_ajax(active_ltm, vs_name, vs_dest, vs_port, vs_desc, vs_tcpprofile, vs_persistence, vs_type, vs_httpprofile, vs_sslclient, vs_sslserver, vs_irule, vs_snatpool, vs_policy, vs_poolname):
    
    logger.info("chg_vs_ajax Head")
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')

    idx = 1
    strReturn = {str(idx) : 'VS Modification Report'}
    idx += 1
    
    logger.info("Logger - Before VS Modification" + str(active_ltm) + " VS DNS:" + str(vs_name) + " VS DEST:" + str(vs_dest) + " VS PORT:" + str(vs_port) + " VS DESC:" + str(vs_desc) + " VS TCP Prf:" + str(vs_tcpprofile) + " VS Persist:" + str(vs_persistence) + " VS Type:" + str(vs_type) + " VS HTTP Prf:" + str(vs_httpprofile) + " VS Clientssl:" + str(vs_sslclient) + " VS Serverssl:" + str(vs_sslserver) + " VS iRule: " + str(vs_irule) + " VS SNATPOOL: " + str(vs_snatpool) + " VS Policy: " + str(vs_policy) + " VS Pool Name: " + str(vs_poolname))
    logger.info("VS Modification process has been initiated.")
     
    try:
        # fieldNames = VS properties collected from CHAN-IQ GUI    
        fieldNames = {"name":vs_name, "description":vs_desc, "ip":vs_dest, "port":vs_port, "ipProtocol":"tcp", "pool":vs_poolname, \
        "protocolProfileClient":vs_tcpprofile, "httpProfile":vs_httpprofile, "oneConnectProfile":"none", "sslProfileClient":vs_sslclient, \
        "sslProfileServer":vs_sslserver, "rules":vs_irule, "sourceAddressTranslation":vs_snatpool, "persistence":vs_persistence,  "policies":vs_policy}
        
        logger.info("Protocol Profile: " + fieldNames["protocolProfileClient"] + " HTTP Profie: " + fieldNames["httpProfile"] + \
                     " SSL Client Profile: " + fieldNames["sslProfileClient"] + " SSL Server Profile: " + fieldNames["sslProfileServer"] +   \
                     " iRule: " + fieldNames["rules"] +   " Persistence: " + fieldNames["persistence"] +   " Policy: " + fieldNames["policies"])  

        loaded_vs = mr.tm.ltm.virtuals.virtual.load(name=fieldNames["name"], partition="Common")
        
        # Get profile names from the loaded virtual server of a target BIG-IP device
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
        
        # Note(01132020) - Virtual Server properties modification
        # For Virtual Server property modification, you MUST use modify(**patch), which calls "patch" and modify the one exactly you want to change.
        # DO NOT USE update(). It would casue an error like " The source (::) and destination (4.5.6.7) addresses for virtual server 
        # (/Common/STDALONE-HOME_VS_vs_01132020) must be be the same type (IPv4 or IPv6)."
        
        # modContent: Include modified properties of a Virtual Server
        modContent= {}
        
        # isPrfModified: Flag to use if any of Profiles has been modified. If so, all profiles must be modified simultaneous even there is no change.
        isPrfModified = 0
        with TransactionContextManager(tx) as api:
            logger.info('#####################################')
            # Update Basic VS properties
            if loaded_prf_names['description'] != fieldNames['description']:
                logger.info("Description has been updated. Current: " + loaded_prf_names['description'] + " New: " + fieldNames['description'] )
                loaded_vs.description = fieldNames['description']
                #loaded_vs.update()
                modContent = {'description':fieldNames['description']}
                #loaded_vs.modify(**modContent)
            
            loaded_vs.source = '0.0.0.0/0'
            #loaded_vs.destination = '%s:%s' % (fieldNames['ip'], fieldNames['port'])
            if loaded_prf_names['ip'] != fieldNames['ip'] or loaded_prf_names['port'] != fieldNames['port']:
                loaded_vs.destination = '%s:%s' % (fieldNames['ip'], fieldNames['port'])
                logger.info("IP or Port has been updated. Current IP: " + loaded_prf_names['ip'] + " New IP: " + fieldNames['ip'] + " Current Port: " + loaded_prf_names['port'] + " New Port: " + fieldNames['port'] )
                modContent['destination'] = '/Common/%s:%s' % (fieldNames['ip'], fieldNames['port'])

            if loaded_prf_names['pool'] != fieldNames['pool']:
                if fieldNames['pool'] == 'none':
                    loaded_vs.pool = fieldNames['pool']
                else:
                    loaded_vs.pool = '/Common/%s' % fieldNames['pool']
                #mod3Content = { 'pool':'/Common/%s' % fieldNames['pool'] }
                modContent['pool'] = '/Common/%s' % fieldNames['pool']
                logger.info("Pool has been updated. Current: " + loaded_prf_names['pool'] + " New: " + fieldNames['pool'])

            #prfRefItems: List variable contains all of Profiles Items such as tcp, http, ssl client, ssl server profiles
            prfRefItems = []
            # ALL profiles under 'profilesReference' should be updated at the same time. So if there is at least 1 profile modified, all profiles must
            # be modified at the same time
            if (loaded_prf_names['httpProfile'] !=  fieldNames['httpProfile'] or
                loaded_prf_names['protocolProfileClient'] !=  fieldNames['protocolProfileClient'] or
                loaded_prf_names['sslProfileClient'] !=  fieldNames['sslProfileClient'] or
                loaded_prf_names['sslProfileServer'] !=  fieldNames['sslProfileServer'] or 
                loaded_prf_names['rules'] !=  fieldNames['rules'] or 
                loaded_prf_names['policies'] !=  fieldNames['policies']) :
                isPrfModified = 1
            # Update http profile
            if loaded_prf_names['httpProfile'] !=  fieldNames['httpProfile'] or isPrfModified == 1:
                # Update VS profile - Delete and then add
                if loaded_prf_names['httpProfile'] != 'none' and fieldNames['httpProfile'] == 'none':
                    loaded_httpprf = loaded_vs.profiles_s.profiles.load(partition='Common', name=loaded_prf_names['httpProfile'])
                    loaded_httpprf.delete()
                else:
                    # Newly assigned HTTP profile is not none. Use modify() to simply update HTTP profile
                    #profilesRef = { 'items':[{'name':fieldNames['httpProfile'], 'context':'all'}] }
                    prfRefItems.append({'name':fieldNames['httpProfile'], 'context':'all'})

                logger.info("HTTP Profile has been updated. Current: " + loaded_prf_names['httpProfile'] + " New: " + fieldNames['httpProfile'] )

            # Update tcp client profile - At this point, tcp server profiel update is not provided.
            if loaded_prf_names['protocolProfileClient'] !=  fieldNames['protocolProfileClient'] or isPrfModified == 1:
                # Update TCP profile - Delete and then add
                logger.info("Loaded TCP Prf name: " + loaded_prf_names['protocolProfileClient'] + " Your choice: " + fieldNames['protocolProfileClient']) 
                loaded_tcpprf = loaded_vs.profiles_s.profiles.load(partition='Common', name=loaded_prf_names['protocolProfileClient'])
                loaded_tcpprf.delete()
                
                prfRefItems.append({'name':fieldNames['protocolProfileClient'], 'context':'all'})
                
                logger.info("TCP Profile has been updated. Current: " + loaded_prf_names['protocolProfileClient'] + " New: " + fieldNames['protocolProfileClient'])

            # Update ssl client profile
            if loaded_prf_names['sslProfileClient'] !=  fieldNames['sslProfileClient'] or isPrfModified == 1:
                logger.info("Loaded clientssl Prf name: " + loaded_prf_names['sslProfileClient'] + " Your choice: " + fieldNames['sslProfileClient'])
                # Update Client SSL profile - Delete and then add
                if loaded_prf_names['sslProfileClient'] != 'none' and fieldNames['sslProfileClient'] == 'none':
                    loaded_sslcliprf = loaded_vs.profiles_s.profiles.load(partition='Common', name=loaded_prf_names['sslProfileClient'])
                    loaded_sslcliprf.delete()
                else:
                    # Newly assigned HTTP profile is not none. Use modify() to simply update HTTP profile
                    #profilesRef3 = { 'items':[{'name':fieldNames['sslProfileClient'], 'context':'clientside'}] }
                    #params3 = {'profilesReference':profilesRef3}
                    #loaded_vs.modify(**params3)
                    prfRefItems.append({'name':fieldNames['sslProfileClient'], 'context':'clientside'})                    

                logger.info("SSL Client Profile has been updated. Current: " + loaded_prf_names['sslProfileClient'] + " New: " + fieldNames['sslProfileClient'] )

            # Update ssl server profile
            if loaded_prf_names['sslProfileServer'] !=  fieldNames['sslProfileServer'] or isPrfModified == 1:
                logger.info("Loaded serverssl Prf name: " + loaded_prf_names['sslProfileServer'] + " Your choice: " + fieldNames['sslProfileServer'])
                # Update Server SSL profile - Delete and then add
                if loaded_prf_names['sslProfileServer'] != 'none' and fieldNames['sslProfileServer'] == 'none':
                    loaded_sslsrvprf = loaded_vs.profiles_s.profiles.load(partition='Common', name=loaded_prf_names['sslProfileServer'])
                    loaded_sslsrvprf.delete()
                else:
                    # Newly assigned HTTP profile is not none. Use modify() to simply update HTTP profile
                    #profilesRef4 = { 'items':[{'name':fieldNames['sslProfileServer'], 'context':'serverside'}] }
                    #params4 = {'profilesReference':profilesRef4}
                    #loaded_vs.modify(**params4)
                    prfRefItems.append({'name':fieldNames['sslProfileServer'], 'context':'serverside'})                          
                    
                logger.info("SSL Server Profile has been updated. Current: " + loaded_prf_names['sslProfileServer'] + " New: " + fieldNames['sslProfileServer'] )

            # Update Persistence profile
            psstItems = []
            if loaded_prf_names['persistence'] !=  fieldNames['persistence']:
                # Update Persistence profile - Prep persistence setting and then update
                if loaded_prf_names['persistence'] != 'none' and fieldNames['persistence'] == 'none':
                    psstItems = []
                elif loaded_prf_names['persistence'] == 'none' and fieldNames['persistence'] != 'none':
                    psstItems.append({'name':fieldNames['persistence'], 'partition':'Common'})
                else:
                    psstItems.append({'name':fieldNames['persistence'], 'partition':'Common'})
                    
                modContent['persist'] = psstItems
                
                logger.info("Persistence has been updated. Current: " + loaded_prf_names['persistence'] + " New: " + fieldNames['persistence'] )
              
            # Update iRule
            # Ref with a value: u'rules': [u'/Common/REDIRECT']
            # Ref without a value: 'rules': []
            iRuleItmes = []
            if loaded_prf_names['rules'] !=  fieldNames['rules'] or isPrfModified == 1:
                # Update Persistence profile - Prep persistence setting and then update
                if loaded_prf_names['rules'] != 'none' and fieldNames['rules'] == 'none':
                    iRuleItmes = []
                #elif loaded_prf_names['rules'] == 'none' and fieldNames['rules'] == 'none':
                elif loaded_prf_names['rules'] == fieldNames['rules']:
                    iRuleItems = []
                elif loaded_prf_names['rules'] == 'none' and fieldNames['rules'] != 'none':
                    iRuleItmes.append('/Common/%s' % fieldNames['rules'])
                else:
                    iRuleItmes.append('/Common/%s' % fieldNames['rules'])
                    
                modContent['rules'] = iRuleItmes
                
                logger.info("iRule has been updated. Current: " + loaded_prf_names['rules'] + " New: " + fieldNames['rules'] )
            
            # Update Policy profile      
            polRefItems = []
            if loaded_prf_names['policies'] !=  fieldNames['policies'] or isPrfModified == 1:
                if loaded_prf_names['policies'] != 'none' and fieldNames['policies'] == 'none':
                    polRefItems = []
                elif loaded_prf_names['policies'] == fieldNames['policies']:
                    polRefItems = []
                elif loaded_prf_names['policies'] == 'none' and fieldNames['policies'] != 'none':
                    polRefItems.append({'name':fieldNames['policies'], 'partition':'Common'})                  
                else:
                    # Newly assigned HTTP profile is not none. Use modify() to simply update HTTP profile
                    #profilesRef = { 'items':[{'name':fieldNames['httpProfile'], 'context':'all'}] }
                    polRefItems.append({'name':fieldNames['policies'], 'partition':'Common'})
                logger.info("Policy has been updated. Current: " + loaded_prf_names['policies'] + " New: " + fieldNames['policies'] )

            # Update SNAT Pool
            # Ref with no value: u'sourceAddressTranslation': {u'type': u'none'}
            # Ref with value:sourceAddressTranslation': {u'pool': u'/Common/snap_p_1.2.3.5', 
            #                u'poolReference': {u'link': u'https://localhost/mgmt/tm/ltm/snatpool/~Common~snap_p_1.2.3.5?ver=12.1.2'},
            #                u'type': u'snat'}
            snatItems = {}
            if loaded_prf_names['sourceAddressTranslation'] !=  fieldNames['sourceAddressTranslation'] or isPrfModified == 1:
                # Update SNAT Pool
                if loaded_prf_names['sourceAddressTranslation'] != 'none' and fieldNames['sourceAddressTranslation'] == 'none':
                    snatItems = {}
                elif loaded_prf_names['sourceAddressTranslation'] == fieldNames['sourceAddressTranslation']:
                    snatItems = {}
                elif loaded_prf_names['sourceAddressTranslation'] == 'none' and fieldNames['sourceAddressTranslation'] != 'none':
                    snatItems = {'pool':'/Common/%s' % fieldNames['sourceAddressTranslation'], 'type':'snat'}
                else:
                    snatItems = {'pool':'/Common/%s' % fieldNames['sourceAddressTranslation'], 'type':'snat'}
                    
                logger.info("SNAT Pool has been updated. Current: " + loaded_prf_names['sourceAddressTranslation'] + " New: " + fieldNames['sourceAddressTranslation'] )
            modContent['sourceAddressTranslation'] = snatItems
            
            prfRef = {}
            polRef = {}
            prfRef['items'] = prfRefItems
            polRef['items'] = polRefItems
            modContent['profilesReference'] = prfRef
            modContent['policiesReference'] = polRef
            loaded_vs.modify(**modContent)                
   
    except Exception as e:
        logger.info("Error during updating virtual server properties")
        logger.info("Error Details: " + str(e))
        logging.info(traceback.format_exc())
        strReturn = {str(idx) : 'Error during updating virtual server properties Error Detail: ' + str(e) }
        idx += 1
        return json.dumps(strReturn)
    
    mr.tm.sys.config.exec_cmd('save')
    logger.info("Virtual Server has been updated successfully")    
    strReturn = {str(idx) : 'Virtual Server has been updated successfully' }
    idx += 1

    return json.dumps(strReturn)


if __name__ == "__main__":
    logger.info("chg_vs_ajax.py logging has been started")
    print chg_vs_ajax(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14], sys.argv[15])
