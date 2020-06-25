from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def get_active_tcpprofiles(active_ltm):
	logger.info('Dev IP in get_tcpprofiles: %s' % active_ltm)
	
	admpass = getpass.getpass('LTM', 'admin')
	mr = ManagementRoot(str(active_ltm), 'admin', admpass)
	tcppf =mr.tm.ltm.profile.tcps.get_collection()
	output = ''

	for atcppf in tcppf:
		if output != '':
			output = output + ':'
		logger.info('TCP Profile: %s' % atcppf.name)
		output = output + atcppf.name
	return output
		
if __name__ == "__main__":
	print get_active_tcpprofiles(sys.argv[1])