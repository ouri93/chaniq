from f5.bigip import ManagementRoot
import sys
import logging
import json
import traceback
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

logger.info("Head of chg_monitor_config() called")

#def chg_monitor_config(active_ltm, vs_dnsname, vs_port, vs_env, vs_poolmon, pLBMethod):
def chg_monitor_config(active_ltm, monName, mDesc, mMonType, mMonCode, mParMonType, mInterval, mTimeout, mSend, mRecv, mUsername, mPassword, mReverse, mAliasPort, mCipherlist ):
    
    logger.info("chg_monitor_config.py parms DevIP: " + active_ltm + " VS Name: " + monName + " Mon Code: " + mMonCode + " Interval: " + mInterval + " Send: " + mSend + " Reverse: " + mReverse + " Alias Port: " + mAliasPort + " CipherList: " + mCipherlist) 

    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
        
    idx = 1
    strReturn = {str(idx) : 'Monitor Modification Report'}
    
    idx += 1
 
    logger.info("Monitor Config Modification process has been initiated.") 
    # Load corresponding Monitor type - 
    try:
        if mMonType == "HTTP":
            loadedMon = mr.tm.ltm.monitor.https.http.load(name=monName, partition='Common')
            loadedMon.update(name=monName, partition='Common', description=mDesc, \
                             interval=int(mInterval), \
                             timeout=int(mTimeout), \
                             reverse=mReverse, \
                             send=mSend, \
                             recv=mRecv, \
                             username=mUsername, \
                             password=mPassword)
        elif mMonType == "HTTPS":
            loadedMon = mr.tm.ltm.monitor.https_s.https.load(name=monName, partition='Common')
            loadedMon.update(name=monName, partition='Common', description=mDesc, interval=int(mInterval), timeout=int(mTimeout), reverse=mReverse, send=mSend, recv=mRecv, username=mUsername, password=mPassword, cipherlist=mCipherlist)
        elif mMonType == "TCP":
            loadedMon = mr.tm.ltm.monitor.tcps.tcp.load(name=monName, partition='Common')
            loadedMon.update(name=monName, partition='Common', description=mDesc, interval=int(mInterval), timeout=int(mTimeout), reverse=mReverse, send=mSend, recv=mRecv)
        elif mMonType == "UDP":
            loadedMon = mr.tm.ltm.monitor.udps.udp.load(name=monName, partition='Common')
            loadedMon.update(name=monName, partition='Common', description=mDesc, interval=int(mInterval), timeout=int(mTimeout), reverse=mReverse, send=mSend, recv=mRecv)
        elif mMonType == "TCP Half Open":
            loadedMon = mr.tm.ltm.monitor.tcp_half_opens.tcp_half_open.load(name=monName, partition='Common')
            loadedMon.update(name=monName, partition='Common', description=mDesc, interval=int(mInterval), timeout=int(mTimeout))
        elif mMonType == "External":    
            pass
    except Exception as e:
        logger.info("Exception during Monitor Loading or configuration modification process")
        strReturn[str(idx)] = "Exception error: " + str(e)
        idx += 1
        logger.info("Health Monitor configuration Loading or Modification exception: " + str(e))
        logger.info("Error Details: " + str(e))
        logger.info(traceback.format_exc())
        return json.dumps(strReturn)

    strReturn[str(idx)] = mMonType + " Monitor configuration(" + monName + ") has been modified successfully."
    idx += 1
    logger.info("Monitor Configuration has been modified successfully")
                    
    
    for keys, values in strReturn.items():
        logger.info("Key: " + keys + " Value: " + values)

    return json.dumps(strReturn)

if __name__ == "__main__":
    print chg_monitor_config(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14], sys.argv[15])
