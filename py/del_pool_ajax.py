from f5.bigip import ManagementRoot
import logging
import sys
import json
import getpass

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)

# 'PhpFileName':'', 'DevIP':'', 'P_name':'', 'P_part':'' 
def del_pool_ajax(active_ltm, p_name, p_part):
    
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    
    idx = 1
    strReturn = {str(idx) : 'Pool Deletion Report'}
    idx += 1

    logging.info("Pool Deletion process has been initiated. Pool Name: " + p_name)
    
    # Phase zero - Update pool properties
    try:
        p_loaded = mr.tm.ltm.pools.pool.load(partition=p_part, name=p_name)
        p_loaded.delete()
    except Exception as e:
        logging.info("Exception during Pool deletion process")
        strReturn[str(idx)] = "Exception error: " + str(e)
        idx += 1
        logging.info("Pool deletion exception: " + str(e))
        return json.dumps(strReturn)

    logging.info("Pool deletion has been successfully completed.")
    strReturn[str(idx)] = "Pool deletion has been successfully completed."
    idx += 1

    return json.dumps(strReturn)


if __name__ == "__main__":
    print del_pool_ajax(sys.argv[1], sys.argv[2], sys.argv[3])
