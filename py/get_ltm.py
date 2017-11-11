from f5.bigip import ManagementRoot
import sys
import logging
import json

def get_active_ltm(dev_name, dev_ip):
	#===========================================================================
	# logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
	# logging.info('Dev Name: %s' % dev_name)
	# logging.info('Dev IP: %s' % dev_ip)
	#===========================================================================
	logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
	logging.info("get_active_ltm()")
	
	mr = ManagementRoot(dev_ip, 'admin', 'rlatkdcks')
	fostat = mr.tm.sys.failover.load()
	if "active" in fostat:
		return 1
	else:
		return 0
	
if __name__ == "__main__":
	print get_active_ltm(sys.argv[1], sys.argv[2])
