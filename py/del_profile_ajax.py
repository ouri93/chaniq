from f5.bigip import ManagementRoot
import sys
import logging
import json
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def delete_profile(mr, partition, pf_type, pf_name):
	
	output = ''
	# Load a given profile name to delete - load() method only requires profile name. If a partition information is given, the query fails with
	# the error of 404 Unexpected Error: Not Found for uri: https://192.168.144.11:443/mgmt/tm/ltm/profile/dns/~common~prf_dns_0829_7
	# Text: u'{"code":404,"message":"01020036:3: The requested DNS Profile (/common/prf_dns_0829_7) was not found.","errorStack":[],"apiError":3}'
	try:
		if pf_type == 'TCP':
			loaded_prf = mr.tm.ltm.profile.tcps.tcp.load(name=pf_name)
		elif pf_type == 'UDP':
			loaded_prf = mr.tm.ltm.profile.udps.udp.load(name=pf_name)
		elif pf_type == 'FastL4':
			loaded_prf = mr.tm.ltm.profile.fastl4s.fastl4.load(name=pf_name)
		elif pf_type == 'HTTP':
			loaded_prf = mr.tm.ltm.profile.https.http.load(name=pf_name)
		elif pf_type == 'DNS':
			loaded_prf = mr.tm.ltm.profile.dns_s.dns.load(name=pf_name)
		elif pf_type == 'CLIENTSSL':
			loaded_prf = mr.tm.ltm.profile.client_ssls.client_ssl.load(name=pf_name)
		elif pf_type == 'SERVERSSL':
			loaded_prf = mr.tm.ltm.profile.server_ssls.server_ssl.load(name=pf_name)
		elif pf_type == 'OneConnect':
			loaded_prf = mr.tm.ltm.profile.one_connects.one_connect.load(name=pf_name)
		elif pf_type == 'Stream':
			loaded_prf = mr.tm.ltm.profile.streams.stream.load(name=pf_name)
		elif pf_type == 'Cookie':
			loaded_prf = mr.tm.ltm.persistence.cookies.cookie.load(name=pf_name)
		elif pf_type == 'DestAddrAffinity':
			loaded_prf = mr.tm.ltm.persistence.dest_addrs.dest_addr.load(name=pf_name)
		elif pf_type == 'SrcAddrAffinity':
			loaded_prf = mr.tm.ltm.persistence.source_addrs.source_addr.load(name=pf_name)
		elif pf_type == 'Hash':
			loaded_prf = mr.tm.ltm.persistence.hashs.hash.load(name=pf_name)
		elif pf_type == 'SSL':
			loaded_prf = mr.tm.ltm.persistence.ssls.ssl.load(name=pf_name)
		elif pf_type == 'Universal':
			loaded_prf = mr.tm.ltm.persistence.universals.universal.load(name=pf_name)
	except Exception as e:
		logger.info("Exception fired during loading profile(" + pf_name + ")")
		output = "Exception fired!: " + str(e)
		logger.info("Loading Profile exception fired: " + str(e))
		return output
	output = output + "Profile loading has been completed\n"
	# Delete a loaded profile
	try:
		loaded_prf.delete()
	except Exception as e:
		logger.info("Exception fired during deleting profile(" + pf_name + ")")
		output = output + "Exception fired!: " + str(e)
		logger.info("Deleting Profile exception fired: " + str(e))
		return output
	output = output + "Profile deletion has been completed\n"
	logger.info('Returing output: %s' % output)
	
	return output

# Data format: {method:'jsonDATA', DevIP:ltmIP, LoadTypeName:prfType, Partition:partition, PrfName:prfName}
def del_profile_ajax(active_ltm, pf_type, partition, pf_name):
	
	admpass = getpass.getpass('LTM', 'admin')
	mr = ManagementRoot(str(active_ltm), 'admin', admpass)
	
	idx = 1
	strReturn = {str(idx) : 'Profile Deletion Report'}
	idx += 1
	
	logger.info('Profile Types: %s' % pf_type)
	logger.info('Profile Deletion process has been initiated')
	strReturn[str(idx)] = 'Profile Deletion process has been initiated'
	idx += 1

	output = delete_profile(mr, partition, pf_type, pf_name)
	strReturn[str(idx)] = output
	#strReturn[str(idx)] = 'Profile loading has been completed.\nProfile deletion has been completed'
	idx += 1
	
	logger.info('Profile Deletion process has been completed')
	strReturn[str(idx)] = 'Profile Deletion process has been completed'
	idx += 1

	return json.dumps(strReturn)
	
if __name__ == "__main__":
	#logger.info('main called: param1: ')
	print del_profile_ajax(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
