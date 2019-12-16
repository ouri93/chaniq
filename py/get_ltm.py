from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

def get_active_ltm(dev_name, active_ltm):
	#===========================================================================
	# logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
	# logging.info('Dev Name: %s' % dev_name)
	# logging.info('Dev IP: %s' % dev_ip)
	#===========================================================================
	logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
	logging.info("get_active_ltm()")
	
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
