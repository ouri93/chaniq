from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def get_active_ltm(dev_name, active_ltm):
	logger.info("get_active_ltm()")
	
	admpass = getpass.getpass('LTM', 'admin')
	mr = ManagementRoot(str(active_ltm), 'admin', admpass)
	#mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
	fostat = mr.tm.sys.failover.load()
	if "active" in fostat:
		return 1
	else:
		return 0
	
if __name__ == "__main__":
	print get_active_ltm(sys.argv[1], sys.argv[2])
