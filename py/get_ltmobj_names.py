from f5.bigip import ManagementRoot
import sys
import logging

def get_vs_names(mr):
	logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
	logger=logging.getLogger(__name__)
	
	vsNames = mr.tm.ltm.virtuals.get_collection()
	#logging.info("after get-tcpprofiles()")
	output = ''

	for avsNames in vsNames:
		if output != '':
			output = output + ':'
		#logging.info('TCP Object: %s' % avsNames.name)
		output = output + avsNames.name
	return output

def get_pool_names(mr):
	poolNames =mr.tm.ltm.pools.get_collection()
	#logging.info("after get-tcpprofiles()")
	output = ''

	for apoolNames in poolNames:
		if output != '':
			output = output + ':'
		#logging.info('TCP Object: %s' % atcppf.name)
		output = output + apoolNames.name
	return output

	
def get_ltmobj_names(dev_ip, obj_type):
	logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
	#logging.info('Called get_profiles(): %s %s' % (dev_ip, obj_type))
	
	mr = ManagementRoot(dev_ip, 'admin', 'rlatkdcks')
	output = ''
	
	'''
	Retrive the name list of a given object type from the given LTM
	Suppported Object types
	1. VS - Virtual Server
	2. POOL - Pool name
	3. MONITOR - Monitor name
	'''
	logging.info('Object Types: %s' % obj_type)
	if obj_type == "VS":
		output = get_vs_names(mr)
	elif obj_type == "POOL":
		output = get_pool_names(mr)
		
	logging.info('output in get_ltmobj_names: %s' % output)
	return output

if __name__ == "__main__":
	#logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
	#logging.info('main called: param1: ')
	print get_ltmobj_names(sys.argv[1], sys.argv[2])
