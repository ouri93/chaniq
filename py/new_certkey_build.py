from f5.bigip import ManagementRoot
import sys
import logging
import json
import build_std_names
import os
import requests
import getpass

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
logging.info("Head of new_certkey_build() called")

def check_keyname_conflict(mr, certkeyImpName):
    keynames = mr.tm.sys.file.ssl_keys.get_collection()
    logging.info("check_keyname_conflict() Key Name: " + certkeyImpName + "\n")
    
    bitout = 0
    
    for akey in keynames:
        if akey.exists(name=certkeyImpName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

# Only support Internal Data Group
def check_certname_conflict(mr, certkeyImpName):
    certnames = mr.tm.sys.file.ssl_certs.get_collection()
    logging.info("check_certname_conflict() Cert Name: " + certkeyImpName + "\n")
    
    bitout = 0
    
    for acert in certnames:
        if acert.exists(name=certkeyImpName):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
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
    
    # Upload Cert/Key file to F5 BIG-IP
    filepath = '/var/www/chaniq/log/tmp/'
    localpath = 'file:/var/config/rest/downloads/'
    filename = ''
    try:
        if certkeyImpType == 'Key':
            filename = certkeyImpName + '.key'
            _upload(str(active_ltm), ('admin', 'H@ll0N3wP@ss'), filepath + filename)
            logging.info("Key file upload completed! - Source File Full path and name: " + filepath + filename)
            '''
            Deprecated method. 
            Use bigip.tm.sys.file.ssl_keys.ssl_key.create(name='name', sourcePath='file:sourcepath')
            Use bigip.tm.sys.file.ssl_certs.ssl_cert.create(name='name', sourcePath='file:sourcepath')
            param_set = {'from-local-file':localpath+filename, 'name':certkeyImpName}
            mr.tm.sys.crypto.keys.exec_cmd('install', **param_set)
            '''
            if certkeySecType == 'password':
                key = mr.tm.sys.file.ssl_keys.ssl_key.create(name=certkeyImpName, partition='Common', sourcePath=localpath+filename, securityType='password', passphrase=certkeySecTypeData)
            elif certkeySecType == 'normal':
                key = mr.tm.sys.file.ssl_keys.ssl_key.create(name=certkeyImpName, partition='Common', sourcePath=localpath+filename)
            logging.info("Key file upload and install completed")
        elif certkeyImpType == 'Certificate':
            filename = certkeyImpName + '.crt'
            _upload(str(active_ltm), ('admin', 'H@ll0N3wP@ss'), filepath + filename)
            logging.info("Cert file upload completed! Source File Full path and name: " + filepath + filename)
            '''
            param_set = {'from-local-file':localpath+filename, 'name':certkeyImpName}
            mr.tm.sys.crypto.certs.exec_cmd('install', **param_set)
            '''
            cert = mr.tm.sys.file.ssl_certs.ssl_cert.create(name=certkeyImpName, partition='Common', sourcePath=localpath+filename)
            logging.info("Cert file upload and install completed")
        elif certkeyImpType == 'PKCS 12 (IIS)':
            filename = certkeyImpName
            _upload(str(active_ltm), ('admin', 'H@ll0N3wP@ss'), filepath + filename + '.p12')
            #_upload(str(active_ltm), ('admin', 'rlatkdcks'), filepath + filename + '.crt')
            logging.info("PKCS Key and Cert file upload completed! - Source File Full path and name: " + filepath + filename)
            '''
            Deprecated method.
            certparam_set = {'from-local-file':localpath+filename+'.p12', 'name':certkeyImpName}
            keyparam_set = {'from-local-file':localpath+filename+'.p12', 'name':certkeyImpName}
            
            #param_set2 = {'from-local-file':localpath+filename+'.p12', 'name':certkeyImpName}
            mr.tm.sys.crypto.keys.exec_cmd('install', **keyparam_set)
            mr.tm.sys.crypto.certs.exec_cmd('install', **certparam_set)
            '''
            '''
            Need to extract key and cert from pkcs12, then import them.
            '''
            if certkeySecType == 'password':
                key = mr.tm.sys.file.ssl_keys.ssl_key.create(name=certkeyImpName, partition='Common', sourcePath=localpath+filename+'.p12', password=certkeyPKCSPw, passphrase=certkeySecTypeData)
            elif certkeySecType == 'normal':
                key = mr.tm.sys.file.ssl_keys.ssl_key.create(name=certkeyImpName, partition='Common', sourcePath=localpath+filename+'.p12', password=certkeyPKCSPw)
                
            cert = mr.tm.sys.file.ssl_certs.ssl_cert.create(name=certkeyImpName, partition='Common', sourcePath=localpath+filename + '.p12')
            
            logging.info("PKCS Cert and Key file upload and install have been completed") 
            
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
