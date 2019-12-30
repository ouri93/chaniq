from f5.bigip import ManagementRoot
import sys
import logging
import json
import build_std_names
import getpass
import loadStdNames

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
logging.info("Head of new_monitor_build() called")

def check_http_mon_conflict(mr, std_monname):
    httpmons = mr.tm.ltm.monitor.https.get_collection()
    logging.info("check_http_mon_conflict() STD Name: " + std_monname + "\n")
    
    bitout = 0
    
    for amon in httpmons:
        if amon.exists(name=std_monname):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False    
    
def check_https_mon_conflict(mr, std_monname):
    httpsmons = mr.tm.ltm.monitor.https_s.get_collection()
    logging.info("check_https_mon_conflict() STD Name: " + std_monname + "\n")
    
    bitout = 0
    
    for amon in httpsmons:
        if amon.exists(name=std_monname):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

def check_tcp_mon_conflict(mr, std_monname):
    tcpmons = mr.tm.ltm.monitor.tcps.get_collection()
    logging.info("check_tcp_mon_conflict() STD Name: " + std_monname + "\n")
    
    bitout = 0
    
    for amon in tcpmons:
        if amon.exists(name=std_monname):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

def check_udp_mon_conflict(mr, std_monname):
    udpmons = mr.tm.ltm.monitor.udps.get_collection()
    logging.info("check_udp_mon_conflict() STD Name: " + std_monname + "\n")
    
    bitout = 0
    
    for amon in udpmons:
        if amon.exists(name=std_monname):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

def check_tcp_halfopen_mon_conflict(mr, std_monname):
    tcphalfmons = mr.tm.ltm.monitor.tcp_half_opens.get_collection()
    logging.info("check_http_mon_conflict() STD Name: " + std_monname + "\n")
    
    bitout = 0
    
    for amon in tcphalfmons:
        if amon.exists(name=std_monname):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

def check_external_mon_conflict(mr, std_monname):
    extmons = mr.tm.ltm.monitor.externals.get_collection()
    logging.info("check_http_mon_conflict() STD Name: " + std_monname + "\n")
    
    bitout = 0
    
    for amon in extmons:
        if amon.exists(name=std_monname):
            bitout = bitout | (1 << 0)
    

    #logging.info("bitout value: " + str(bitout) + "\n")    

    # If Poolname conflicts, return True. Otherwise return False
    if (bitout >> 0) & 1:
        return True
    else:
        return False  

def check_monname_conflict(mr, std_monname, mMonType):
    
    logging.info("new_monitor_build() - check_monname_conflict() Monitor name: " + std_monname + " Monitor Type: " + mMonType)
    
    byMonType = {
        "HTTP": check_http_mon_conflict,
        "HTTPS": check_https_mon_conflict,
        "TCP": check_tcp_mon_conflict,
        "UDP": check_udp_mon_conflict,
        "TCP Half Open": check_tcp_halfopen_mon_conflict,
        "External": check_external_mon_conflict        
    }
    
    return byMonType[mMonType](mr, std_monname)

#def new_monitor_build(active_ltm, vs_dnsname, vs_port, vs_env, vs_poolmon, pLBMethod):
def new_monitor_build(active_ltm, monName, mDesc, mEnv, mMonType, mMonCode, mParMonType, mInterval, mTimeout, mSend, mRecv, mUsername, mPassword, mReverse, mAliasPort, mCipherlist ):
    
    logging.info("new_monitor_build.py parms DevIP: " + active_ltm + " VS Name: " + monName + " Env: " + mEnv + " Mon Code: " + mMonCode + " Interval: " + mInterval + " Send: " + mSend + " Reverse: " + mReverse + " Alias Port: " + mAliasPort + " CipherList: " + mCipherlist) 

    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')

    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logging.info("new_monitor_build()- Use Standard Global naming : " + useGlobalNaming )
        
    idx = 1
    strReturn = {str(idx) : 'Monitor Creation Report'}
    
    idx += 1

    if useGlobalNaming == '1':
        if mMonType == "TCP Half Open":
            std_monname = loadStdNames.get_std_name(active_ltm, 'SHARED', 'MONITOR', 'TCP_HALF_OPEN', monName)
        elif mMonType == 'External':
            std_monname = loadStdNames.get_std_name(active_ltm, 'SHARED', 'MONITOR', 'EXTERNAL', monName)            
        else:
            std_monname = loadStdNames.get_std_name(active_ltm, 'SHARED', 'MONITOR', mMonType, monName)
    else:
        std_monname = monName                     
    #std_monname = build_std_names.build_std_mon_name(str(mEnv), str(monName))
    
    logging.info("Monitor Creation process has been initiated. Pool Name: " + std_monname) 
    
    if check_monname_conflict(mr, std_monname, mMonType):
        strReturn.update({str(idx) : 'Monitor Name conflict'})
        logging.info("Monitor name conflict.")
        idx += 1
        return json.dumps(strReturn)
    logging.info("No Monitor name conflict. Now creating a monitor")
    
    #Create a monitor
    if mMonType == "HTTP":
        mymon = mr.tm.ltm.monitor.https.http.create(name=std_monname, partition='Common', description=mDesc, interval=int(mInterval), timeout=int(mTimeout), reverse=mReverse, send=mSend, recv=mRecv, username=mUsername, password=mPassword, destination="*:"+ mAliasPort)
    elif mMonType == "HTTPS":
        mymon = mr.tm.ltm.monitor.https_s.https.create(name=std_monname, partition='Common', description=mDesc, interval=int(mInterval), timeout=int(mTimeout), reverse=mReverse, send=mSend, recv=mRecv, username=mUsername, password=mPassword, destination="*:"+ mAliasPort, cipherlist=mCipherlist)
    elif mMonType == "TCP":
        mymon = mr.tm.ltm.monitor.tcps.tcp.create(name=std_monname, partition='Common', description=mDesc, interval=int(mInterval), timeout=int(mTimeout), reverse=mReverse, send=mSend, recv=mRecv, destination="*:"+ mAliasPort)
    elif mMonType == "UDP":
        mymon = mr.tm.ltm.monitor.udps.udp.create(name=std_monname, partition='Common', description=mDesc, interval=int(mInterval), timeout=int(mTimeout), reverse=mReverse, send=mSend, recv=mRecv, destination="*:"+ mAliasPort)
    elif mMonType == "TCP Half Open":
        mymon = mr.tm.ltm.monitor.tcp_half_opens.tcp_half_open.create(name=std_monname, partition='Common', description=mDesc, interval=int(mInterval), timeout=int(mTimeout),destination="*:"+ mAliasPort)
    elif mMonType == "External":    
        pass

    strReturn[str(idx)] = mMonType + " Monitor (" + std_monname + ") has been created"
    idx += 1
    logging.info("Monitor created")
                    
    
    for keys, values in strReturn.items():
        logging.info("Key: " + keys + " Value: " + values)

    return json.dumps(strReturn)

if __name__ == "__main__":
    print new_monitor_build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14], sys.argv[15], sys.argv[16])
