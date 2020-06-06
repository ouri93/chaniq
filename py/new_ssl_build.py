from f5.bigip import ManagementRoot
from f5.bigip.contexts import TransactionContextManager
import sys
import logging
import json
import build_std_names
import os
import requests
import getpass
import loadStdNames
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


# 'sslDevIP':'', 'issuerType':'', 'sslName':'', 'sslCN':'', 'sslSelfLifetime':'', 'sslCAChallengePW':'', 'sslDvz':'', 
# 'sslOG':'', 'sslLoc':'', 'sslState':'', 'sslCountry':'', 'sslEmail':'', 'sslSAN':'', 'sslKeyType':'', 'sslKeySize':''
def new_ssl_build(active_ltm, issuerType, sslName, sslCN, sslSelfLifetime, sslCAChallengePW, sslDvz, sslOG, sslLoc, sslState, sslCountry, sslEmail, sslSAN, sslKeyType, sslKeySize):
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)

    idx = 1
    strReturn = {str(idx) : 'SSL Cert/Key/CSR Creation Report'}
    idx += 1

    if check_certkeyname_conflict(mr, 'Key', sslName):
        strReturn.update({str(idx) : 'Cert/Key Name conflict'})
        logging.info("Cert/Key Name conflict.")
        idx += 1
        return json.dumps(strReturn)
    logging.info("No Cert/Key name conflict. Now creating a Cert/Key")

    pySdkVer = str(chaniq_util.loadIniConfigVal('PYTHON_SDK_INFO', 'SDK_VER'))
    logging.info("Loaded Python SDK Version: " + pySdkVer)
    f5LocalPath = 'file:/var/config/rest/downloads/'
    if pySdkVer == '2.3.3':
        f5LocalPath = '/var/config/rest/downloads/'

    if pySdkVer == '2.3.3':
        keyParam_set = {'from-local-file': f5LocalPath+sslName+'.key', 'name':sslName}
        certParam_set = {'from-local-file': f5LocalPath+sslName+'.crt', 'name':sslName}
                
    # Upload Cert/Key file to F5 BIG-IP
    chanIQFilePath = '/var/www/chaniq/log/tmp/'
            
    # Self - Lifetime (Default: 365)
    # Certificate Authority - Challenge Password
    # Common: Name, CN, C, O, OU, L, ST, Email address, Key Type (RSA), Key Size
    # Common but need special care: SAN - Config file or config thru. CLI should be provided.
    # f5LocalPath variable is used to specify F5 side cert/key download folder. 
    # If Python SDK version is 2.3.3, we use exec_cmd command to install cert or key. Otherwise, create() method is used.
    
    # Create a private key
    strKeyCmd = ""
    if issuerType == 'Certificate Authority' and sslCAChallengePW != '':
        strKeyCmd =  "-c '" + 'openssl genrsa -out "/var/config/rest/downloads/' + sslName + '.key" -passout pass:' + sslCAChallengePW + " " + str(sslKeySize) +  "'"
    else:
        strKeyCmd = "-c '" + 'openssl genrsa -out "/var/config/rest/downloads/' + sslName + '.key" ' + str(sslKeySize) + "'"
    logging.info("Key Generation String: " + strKeyCmd)
    mr.tm.util.bash.exec_cmd('run', utilCmdArgs = strKeyCmd)
    # Install the generate private key on F5
    if pySdkVer == '2.3.3':
        mr.tm.sys.crypto.keys.exec_cmd('install', **keyParam_set)
    else:
        if sslCAChallengePW != '':
            mr.tm.sys.file.ssl_keys.ssl_key.create(name=sslName, partition='Common', sourcePath=f5LocalPath+sslName+'.key', securityType='password', passphrase=certkeySecTypeData)
        else:
            mr.tm.sys.file.ssl_keys.ssl_key.create(name=sslName, partition='Common', sourcePath=f5LocalPath+sslName+'.key')
    logging.info("Key has been generated successfully")    
    strReturn.update({str(idx) : 'Key has been generated and installed successfully'})
    idx += 1

    subj = ""
    # Build a subj string
    dicCertProp = {'emailAddress':sslEmail, 'CN':sslCN, 'OU':sslDvz, 'O':sslOG, 'L':sslLoc, 'ST':sslState, 'C':sslCountry.split(":")[1] }

    for k,v in dicCertProp.iteritems():
        if v != "":
            subj = subj + "/" + k + "=" + v

    # Create a cert using the existing key (Only for Self Signed cert)
    if issuerType == "Self":
        strCrtCmd = "-c '" + 'openssl req -key "/var/config/rest/downloads/' + sslName + '.key" -new -x509 -days ' + str(sslSelfLifetime) + ' -out "/var/config/rest/downloads/' + sslName + '.crt" -subj "' + subj + '"' + "'"
        logging.info("Crt Generation String: " + strCrtCmd)
        mr.tm.util.bash.exec_cmd('run', utilCmdArgs = strCrtCmd)
        logging.info("Cert has been generated")
        
        # Install the generated Cert on F5
        if pySdkVer == '2.3.3':
            mr.tm.sys.crypto.certs.exec_cmd('install', **certParam_set)
        else:
            mr.tm.sys.file.ssl_certs.ssl_cert.create(name=sslName, partition='Common', sourcePath=f5LocalPath+sslName+'.crt')
        
        strReturn.update({str(idx) : 'Cert has been generated and installed successfully'})
        idx += 1

    # Create a CSR using the existing private key
    strCsrCmd = ""
    if issuerType == "Certificate Authority":
        if sslCAChallengePW != '':
            strCsrCmd = "-c '" + 'openssl req -out "/var/config/rest/downloads/' + sslName + '.csr"  -new -key "/var/config/rest/downloads/' + sslName + '.key" -passin pass: '+ sslCAChallengePW + '-subj "' + subj + '"' + "'" 
        else:
            strCsrCmd = "-c '" + 'openssl req -out "/var/config/rest/downloads/' + sslName + '.csr"  -new -key "/var/config/rest/downloads/' + sslName + '.key" -subj "' + subj + '"' + "'"                
    
        logging.info("CSR Generation String: " + strCsrCmd)
        mr.tm.util.bash.exec_cmd('run', utilCmdArgs = strCsrCmd)
        logging.info("CSR has been generated")
    
        # Install the generated CSR on F5 - CSR is created through openssl command but installing the csr on F5 keeps failing.
        mr.tm.sys.file.ssl_csrs.ssl_csr.create(name=sslName, sourcePath='file:/var/config/rest/downloads/' + sslName + '.csr', subject='CN=www.home.local,L=Lenexa,ST=KS,C=US,emailAddress=admin@home.local')
        #mr.tm.sys.config.exec_cmd('save')
        
        strReturn.update({str(idx) : 'CSR has been generated and installed successfully'})
        idx += 1
        
    return json.dumps(strReturn)


if __name__ == "__main__":
    print new_ssl_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14], sys.argv[15])
