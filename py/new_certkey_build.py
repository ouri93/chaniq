from f5.bigip import ManagementRoot
import sys
import logging
import json
import build_std_names

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
logging.info("Head of new_certkey_build() called")

def check_keyname_conflict(mr, certkeyImpName):
    keynames = mr.tm.sys.files.ssl_keys.get_collection()
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
    certnames = mr.tm.sys.files.ssl_certs.get_collection()
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
    
    logging.info("new_certkey_build() - check_certkeyname_conflict() iRule/Data Group name: " + std_certkeyname + " Monitor Type: " + certkeyKeySourceData + " DG Type: " + certkeySecTypeData)
    
    byImpKeyType = {
        "Key": check_keyname_conflict,
        "Certificate": check_certname_conflict,
        "PKCS 12 (IIS)": check_pkcsname_conflict
    }
    
    return byImpKeyType[certkeyImpType](mr, certkeyImpName)

def _upload(host, creds, fp):
 
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
        requests.post(uri,
                      auth=creds,
                      data=file_slice,
                      headers=headers,
                      verify=False)
 
        start += current_bytes

def new_certkey_build(certkeyDevIp, certkeyImpType, certkeyImpName, certkeyKeySource, certkeyKeySourceData, certkeySecType, certkeySecTypeData, certkeyPKCSPw):
    
    logging.info("new_certkey_build.py parms DevIP: " + certkeyDevIp + " Import Type: " + certkeyImpType + "Import name: " + certkeyImpName + " Key Source: " + certkeyKeySource + " Security Type: " + certkeySecType + " Security Data: " + certkeySecTypeData + " PKCS PW: " + certkeyPKCSPw) 

    mr = ManagementRoot(str(certkeyDevIp), 'admin', 'rlatkdcks')
    
    idx = 1
    strReturn = {str(idx) : 'SSL Cert/Key Creation Report'}
    
    idx += 1
 
    if check_certkeyname_conflict(mr, certkeyImpType, certkeyImpName):
        strReturn.update({str(idx) : 'Cert/Key Name conflict'})
        logging.info("Cert/Key Name conflict.")
        idx += 1
        return json.dumps(strReturn)
    logging.info("No Cert/Key name conflict. Now creating a Cert/Key")
    
    #Create a iRule/Data Group
    try:
        if certkeyKeySourceData == "iRule":
            mycertkey = mr.tm.ltm.rules.rule.create(name=std_certkeyname, partition='Common', apiAnonymous=certkeySecType)
        elif certkeyKeySourceData == "Data Group":
            new_records = []
            arrRecords = certkeyPKCSPw.split(',');
            for arrRecord in arrRecords:
                aRecord = arrRecord.split(':')
                logging.info("name: " + aRecord[0] + " Value: " + aRecord[1])
                nr = [{'name':str(aRecord[0]), 'data':str(aRecord[1])}]
                new_records.extend(nr)
            if certkeySecTypeData == "Address":
                mydg = mr.tm.ltm.data_group.internals.internal.create(name=std_certkeyname, partition='Common', type='ip', records=new_records)
            elif certkeySecTypeData == "String":
                mydg = mr.tm.ltm.data_group.internals.internal.create(name=std_certkeyname, partition='Common', type='string', records=new_records)
            elif certkeySecTypeData == "Integer":
                mydg = mr.tm.ltm.data_group.internals.internal.create(name=std_certkeyname, partition='Common', type='integer', records=new_records)
    except Exception as e:
        logging.info("iRule/Data Group Exception printing")
        strReturn[str(idx)] = "Exception fcertkeyed! (" + std_certkeyname + "): " + str(e)
        idx += 1
        logging.info("iRule/Data Group creation exception fcertkeyed: " + str(e))
        return json.dumps(strReturn)
    
    strReturn[str(idx)] = certkeyKeySourceData + " iRule/Data Group (" + std_certkeyname + ") has been created"
    idx += 1
    logging.info("iRule/Data Group has been created")
                    
    
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)

    return json.dumps(strReturn)

if __name__ == "__main__":
    print new_certkey_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
