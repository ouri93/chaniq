from f5.bigip import ManagementRoot
import sys
import logging
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def get_vs_names(mr):
	
	vsNames = mr.tm.ltm.virtuals.get_collection()
	#logger.info("after get-tcpprofiles()")
	output = ''

	for avsNames in vsNames:
		if output != '':
			output = output + ':'
		#logger.info('TCP Object: %s' % avsNames.name)
		output = output + avsNames.name
	return output

def get_pool_names(mr):
	poolNames =mr.tm.ltm.pools.get_collection()
	#logger.info("after get-tcpprofiles()")
	output = ''

	for apoolNames in poolNames:
		if output != '':
			output = output + ':'
		#logger.info('TCP Object: %s' % atcppf.name)
		output = output + apoolNames.name
	return output

	
def get_ltmobj_names(active_ltm, obj_type):
	#logger.info('Called get_profiles(): %s %s' % (dev_ip, obj_type))
	
	admpass = getpass.getpass('LTM', 'admin')
	mr = ManagementRoot(str(active_ltm), 'admin', admpass)
	#mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
	output = ''
	
	'''
	Retrive the name list of a given object type from the given LTM
	Suppported Object types
	1. VS - Virtual Server
	2. POOL - Pool name
	3. MONITOR - Monitor name
	'''
	logger.info('Object Types: %s' % obj_type)
	if obj_type == "VS":
		output = get_vs_names(mr)
	elif obj_type == "POOL":
		output = get_pool_names(mr)
		
	logger.info('output in get_ltmobj_names: %s' % output)
	return output

if __name__ == "__main__":
	#logger.info('main called: param1: ')
	print get_ltmobj_names(sys.argv[1], sys.argv[2])
