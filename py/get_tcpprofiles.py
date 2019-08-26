from f5.bigip import ManagementRoot
import sys
import logging
import json

def get_active_tcpprofiles(dev_ip):
	logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
	logging.info('Dev IP in get_tcpprofiles: %s' % dev_ip)
	
	mr = ManagementRoot(dev_ip, 'admin', 'rlatkdcks')
	tcppf =mr.tm.ltm.profile.tcps.get_collection()
	output = ''

	for atcppf in tcppf:
		if output != '':
			output = output + ':'
		logging.info('TCP Profile: %s' % atcppf.name)
		output = output + atcppf.name
	return output
		
if __name__ == "__main__":
	print get_active_tcpprofiles(sys.argv[1])