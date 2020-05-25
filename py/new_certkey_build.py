from f5.bigip import ManagementRoot
import sys
import logging
import json
import build_std_names
import os
import requests
import getpass
import chaniq_util

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
logging.info("Head of new_certkey_build() called")

def check_keyname_conflict(mr, certkeyImpName):
    keynames = mr.tm.sys.file.ssl_keys.get_collection()
    logging.info("check_keyname_conflict() Key Name: " + certkeyImpName + ".key\n")
    
    bitout = 0
    
    for akey in keynames:
        if akey.exists(name=certkeyImpName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Key name conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

# Only support Internal Data Group
def check_certname_conflict(mr, certkeyImpName):
    certnames = mr.tm.sys.file.ssl_certs.get_collection()
    logging.info("check_certname_conflict() Cert Name: " + certkeyImpName + ".crt\n")
    
    bitout = 0
    
    for acert in certnames:
        if acert.exists(name=certkeyImpName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Cert name conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

def check_pkcsname_conflict(mr, certkeyImpName):

    if check_certname_conflict(mr, certkeyImpName) or check_keyname_conflict(mr, certkeyImpName):
        return True
    else:
        return False

def check_certkeyname_conflict(mr, certkeyImpType, certkeyImpName):
    
    logging.info("new_certkey_build() - check_certkeyname_conflict() Import Type: " + certkeyImpType + " Cert/Key Name: " + certkeyImpName)
    
    byImpKeyType = {
        "Key": check_keyname_conflict,
        "Certificate": check_certname_conflict,
        "PKCS 12 (IIS)": check_pkcsname_conflict
    }
    
    return byImpKeyType[certkeyImpType](mr, certkeyImpName)

def _upload(host, creds, fp):
 
    logging.info("_upload called!")
    logging.info("Host: " + str(host) + " Filename: " + fp + "\n")
    chunk_size = 512 * 1024
    headers = {
        'Content-Type': 'application/octet-stream'
    }
    fileobj = open(fp, 'rb')
    filename = os.path.basename(fp)
    if os.path.splitext(filename)[-1] == '.iso':
        uri = 'https://%s/mgmt/cm/autodeploy/software-image-uploads/%s' % (host, filename)
    else:
        uri = 'https://%s/mgmt/shared/file-transfer/uploads/%s' % (host, filename)
 
    logging.info("_upload URI: " + uri)
    requests.packages.urllib3.disable_warnings()
    size = os.path.getsize(fp)
 
    start = 0
 
    while True:
        file_slice = fileobj.read(chunk_size)
        if not file_slice:
            break
 
        current_bytes = len(file_slice)
        if current_bytes < chunk_size:
            end = size
        else:
            end = start + current_bytes
 
        content_range = "%s-%s/%s" % (start, end - 1, size)
        headers['Content-Range'] = content_range
        try:
            requests.post(uri,
                          auth=creds,
                          data=file_slice,
                          headers=headers,
                          verify=False)
        except Exception as e:
            logging.info("Exception while requests.post processing - Error: " + str(e)) 
        start += current_bytes
    logging.info("_upload() is completed")

def new_certkey_build(active_ltm, certkeyImpType, certkeyImpName, certkeyKeySource, certkeyKeySourceData, certkeySecType, certkeySecTypeData, certkeyPKCSPw):
    
    logging.info("new_certkey_build.py parms DevIP: " + active_ltm + " Import Type: " + certkeyImpType + "Import name: " + certkeyImpName + " Key Source: " + certkeyKeySource + " Security Type: " + certkeySecType + " Security Data: " + certkeySecTypeData + " PKCS PW: " + certkeyPKCSPw) 

    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    
    idx = 1
    strReturn = {str(idx) : 'SSL Cert/Key Creation Report'}
    
    idx += 1
 
    '''
    If the key source type is "PASTE", save Key or Certficate content into a file under /var/config/rest/downloads/ location
    This will make all Key and Certificate source type as a file.
    Note. 'from-editor' is not the command where it takes the key or cert content directly. For this reason, I convert key/cert content into a file 
    '''
    if certkeyKeySource == 'PASTE':
        try:
            if certkeyImpType == 'Key':
                keyfilename = '/var/www/chaniq/log/tmp/' + certkeyImpName + '.key'
                f= open(keyfilename, "w+")
                f.write(certkeyKeySourceData)
                f.close()
            elif certkeyImpType == 'Certificate':
                certfilename = '/var/www/chaniq/log/tmp/' + certkeyImpName + '.crt'
                f= open(certfilename, "w+")
                f.write(certkeyKeySourceData)
                f.close()
            else:
                logging.info("Unsupported Cert/Key Source Type: " + certkeyImpType)
                strReturn[str(idx)] = "Unsupported Cert/Key Source Type: " + certkeyImpType
                idx += 1
                return json.dumps(strReturn)
        except Exception as e:
            logging.info("File Creation Exception fired: " + str(e))
            strReturn[str(idx)] = "Exception fired during cert/key file creation!: " + str(e)
            idx += 1
            return json.dumps(strReturn)
    
    if check_certkeyname_conflict(mr, certkeyImpType, certkeyImpName):
        strReturn.update({str(idx) : 'Cert/Key Name conflict'})
        logging.info("Cert/Key Name conflict.")
        idx += 1
        return json.dumps(strReturn)
    logging.info("No Cert/Key name conflict. Now creating a Cert/Key")
    
    # f5LocalPath variable is used to specify F5 side cert/key download folder. 
    # If Python SDK version is 2.3.2, we use exec_cmd command to install cert or key. Otherwise, create() method is used.
    pySdkVer = str(chaniq_util.loadIniConfigVal('PYTHON_SDK_INFO', 'SDK_VER'))
    logging.info("Loaded Python SDK Version: " + pySdkVer)
    f5LocalPath = 'file:/var/config/rest/downloads/'
    if pySdkVer == '2.3.2':
        f5LocalPath = '/var/config/rest/downloads/'
    
    # Upload Cert/Key file to F5 BIG-IP
    chanIQFilePath = '/var/www/chaniq/log/tmp/'

    try:
        # Known issue with Password encrypted private Key - https://support.f5.com/csp/article/K46145454
        # Solution: Upgrade to BIG-IP 13.1.0 or later
        
        if pySdkVer == '2.3.2':
            keyParam_set = {'from-local-file': f5LocalPath+certkeyImpName+'.key', 'name':certkeyImpName}
            certParam_set = {'from-local-file': f5LocalPath+certkeyImpName+'.crt', 'name':certkeyImpName}
        
        if certkeyImpType == 'Key':
            _upload(str(active_ltm), ('admin', admpass), chanIQFilePath + certkeyImpName + '.key')

            logging.info("Key file upload completed! - Source File Full path: " + chanIQFilePath +  " name: " + certkeyImpName + '.key')
            '''
            Ref1: https://devcentral.f5.com/s/feed/0D51T00006j1piKSAQ
            Ref2: https://programtalk.com/python-examples-amp/f5.bigip.contexts.TransactionContextManager/
            
            If Python SDK version is 2.3.2, use exec_cmd(), use create() to install cert and key
            param_set = {'from-local-file': '/var/config/rest/downloads/keyfile.key', 'name':Your_key_name}
            Using bigi.tm.sys.crypto.keys.exec_cmd('install', **param_set) is a deprecated method.
            
            If Python SDK version is newer than 2.3.2, use create() to install cert and key
            Use sys.file.ssl_keys.ssl_key and sys.file.ssl_certs.ssl_cert instead. 
            Use bigip.tm.sys.file.ssl_keys.ssl_key.create(name='name', sourcePath='file:sourcepath')
            Use bigip.tm.sys.file.ssl_certs.ssl_cert.create(name='name', sourcePath='file:sourcepath')
            '''
            # To install cert and key, a key must be imported first
            # If you try to import a key where a cert having the same name exists but same name key doesn't exist, return with error message
            if check_certname_conflict(mr, certkeyImpName):
                logging.info("To install the both of cert and key, a key must be imported first")
                strReturn[str(idx)] = "To install the both of cert and key, a key must be imported first"
                idx += 1
                return json.dumps(strReturn)
            # Create a new key
            if certkeySecType == 'Password':
                if pySdkVer == '2.3.2':
                    keyParam_set['securityType'] = 'password'
                    keyParam_set['passphrase'] = certkeySecTypeData
                    key = mr.tm.sys.crypto.keys.exec_cmd('install', **keyParam_set)
                else:
                    logging.info("I am here with password")
                    key = mr.tm.sys.file.ssl_keys.ssl_key.create(name=certkeyImpName, partition='Common', sourcePath=f5LocalPath+certkeyImpName+'.key', securityType='password', passphrase=certkeySecTypeData)
            elif certkeySecType == 'Normal':
                if pySdkVer == '2.3.2':
                    logging.info("I am here with normal")
                    key = mr.tm.sys.crypto.keys.exec_cmd('install', **keyParam_set)
                else:
                    key = mr.tm.sys.file.ssl_keys.ssl_key.create(name=certkeyImpName, partition='Common', sourcePath=f5LocalPath+certkeyImpName+'key')
            else:
                logging.info("Unsupported Key Security Type - Provided Security Type: " + certkeySecType)
                strReturn[str(idx)] = "Unsupported Key Security Type - Provided Security Type: " + certkeySecType 
                idx += 1 

            logging.info("Key file upload and install completed")
        elif certkeyImpType == 'Certificate':
            _upload(str(active_ltm), ('admin', admpass), chanIQFilePath + certkeyImpName + '.crt')
            logging.info("Cert file upload completed! Source File Full path and name: " + chanIQFilePath +  " name: " + certkeyImpName + '.crt')
            
            if pySdkVer == '2.3.2':
                cert = mr.tm.sys.crypto.certs.exec_cmd('install', **certParam_set)
            else:
                cert = mr.tm.sys.file.ssl_certs.ssl_cert.create(name=certkeyImpName, partition='Common', sourcePath=f5LocalPath+certkeyImpName + '.crt')
            
            logging.info("Cert file upload and install completed")
        elif certkeyImpType == 'PKCS 12 (IIS)':
            logging.info("Uploading and installing PKCS 12 Cert and Key")
            _upload(str(active_ltm), ('admin', admpass), chanIQFilePath + certkeyImpName + '.pfx')
            #_upload(str(active_ltm), ('admin', 'rlatkdcks'), chanIQFilePath + certkeyImpName + '.crt')
            logging.info("PKCS Key and Cert file upload completed! - Source File Full path and name: " + chanIQFilePath +  " name: " + certkeyImpName + '.pfx')
            '''
            Deprecated method.
            certparam_set = {'from-local-file':f5LocalPath+certkeyImpName + '.pfx', 'name':certkeyImpName}
            keyparam_set = {'from-local-file':f5LocalPath+certkeyImpName + '.pfx', 'name':certkeyImpName}
            
            #param_set2 = {'from-local-file':f5LocalPath+certkeyImpName + '.pfx', 'name':certkeyImpName}
            mr.tm.sys.crypto.keys.exec_cmd('install', **keyparam_set)
            mr.tm.sys.crypto.certs.exec_cmd('install', **certparam_set)
            '''
            '''
            Need to extract key and cert from pkcs12, then import them.
            '''
            # Create a new key
            if certkeySecType == 'Password':
                if pySdkVer == '2.3.2':
                    keyParam_set['securityType'] = 'password'
                    keyParam_set['passphrase'] = certkeySecTypeData
                    key = mr.tm.sys.crypto.keys.exec_cmd('install', **keyParam_set)
                else:
                    key = mr.tm.sys.file.ssl_keys.ssl_key.create(name=certkeyImpName, partition='Common', sourcePath=f5LocalPath+certkeyImpName+'.pfx', securityType='password', passphrase=certkeySecTypeData)
            elif certkeySecType == 'Normal':
                if pySdkVer == '2.3.2':
                    key = mr.tm.sys.crypto.keys.exec_cmd('install', **keyParam_set)
                else:
                    key = mr.tm.sys.file.ssl_keys.ssl_key.create(name=certkeyImpName, partition='Common', sourcePath=f5LocalPath+certkeyImpName+'pfx')
            else:
                logging.info("Unsupported Key Security Type - Provided Security Type: " + certkeySecType)
                strReturn[str(idx)] = "Unsupported Key Security Type - Provided Security Type: " + certkeySecType 
                idx += 1 
            logging.info("PKCS12 Key file upload and installation has been completed")
            
            # Create a new cert            
            if pySdkVer == '2.3.2':
                cert = mr.tm.sys.crypto.certs.exec_cmd('install', **certParam_set)
            else:
                cert = mr.tm.sys.file.ssl_certs.ssl_cert.create(name=certkeyImpName, partition='Common', sourcePath=f5LocalPath+certkeyImpName + '.pfx')
            
            logging.info("PKCS12 Cert file upload and installation has been completed")
            logging.info("PKCS Cert and Key file upload and installation have been completed") 
            
    except Exception as e:
        logging.info("File Upload Exception fired: " + str(e))
        strReturn[str(idx)] = "Exception fired during cert/key upload or install! (" + certkeyImpName + "): " + str(e)
        idx += 1
        logging.info("Cert/Key upload or install exception: " + str(e))
        return json.dumps(strReturn)
    
    strReturn[str(idx)] = certkeyImpType + " (" + certkeyImpName + ") has been successfully created"
    idx += 1
    logging.info("Cert/Key has been created")
                    
    
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)

    return json.dumps(strReturn)

if __name__ == "__main__":
    print new_certkey_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
