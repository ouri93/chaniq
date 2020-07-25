from f5.bigip import ManagementRoot
import sys
import logging
import json
import traceback
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

logger.info("Head of del_monitor_ajax() called")

#def del_monitor_ajax(active_ltm, vs_dnsname, vs_port, vs_env, vs_poolmon, pLBMethod):
def del_monitor_ajax(active_ltm, monName, mDesc, mMonType, mParMonType):
    
    logger.info("del_monitor_ajax.py parms DevIP: " + active_ltm + " VS Name: " + monName + "\n") 
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    
    idx = 1
    strReturn = {str(idx) : 'Monitor Deletion Report'}
    
    idx += 1
 
    logger.info("Monitor Deletion process has been initiated.") 
    # Load corresponding Monitor type - 
    try:
        if mMonType == "HTTP":
            loadedMon = mr.tm.ltm.monitor.https.http.load(name=monName, partition='Common')
        elif mMonType == "HTTPS":
            loadedMon = mr.tm.ltm.monitor.https_s.https.load(name=monName, partition='Common')
        elif mMonType == "TCP":
            loadedMon = mr.tm.ltm.monitor.tcps.tcp.load(name=monName, partition='Common')
        elif mMonType == "UDP":
            loadedMon = mr.tm.ltm.monitor.udps.udp.load(name=monName, partition='Common')
        elif mMonType == "TCP Half Open":
            loadedMon = mr.tm.ltm.monitor.tcp_half_opens.tcp_half_open.load(name=monName, partition='Common')
        elif mMonType == "External":    
            pass
        loadedMon.delete()
    except Exception as e:
        logger.info("Exception during Monitor Loading or Deletion process")
        strReturn[str(idx)] = "Exception error: " + str(e)
        idx += 1
        logger.info("Health Monitor Loading or Deletion exception: " + str(e))
        logger.info("Error Details: " + str(e))
        logger.info(traceback.format_exc())
        return json.dumps(strReturn)

    strReturn[str(idx)] = mMonType + " Monitor Deletion(" + monName + ") has been completed successfully."
    idx += 1
    logger.info("Monitor Deletion has been completd successfully")
                    
    
    for keys, values in strReturn.items():
        logger.info("Key: " + keys + " Value: " + values)

    return json.dumps(strReturn)

if __name__ == "__main__":
    print del_monitor_ajax(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
