from f5.bigip import ManagementRoot
import sys
import logging
import getpass

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def get_tcpprofiles(mr):
	tcppf =mr.tm.ltm.profile.tcps.get_collection()
	#logger.info("after get-tcpprofiles()")
	output = ''

	for atcppf in tcppf:
		if output != '':
			output = output + ':'
		#logger.info('TCP Profile: %s' % atcppf.name)
		output = output + atcppf.name
	return output

def get_udpprofiles(mr):
	udppf =mr.tm.ltm.profile.udps.get_collection()
	#logger.info("after get-tcpprofiles()")
	output = ''

	for audppf in udppf:
		if output != '':
			output = output + ':'
		#logger.info('TCP Profile: %s' % atcppf.name)
		output = output + audppf.name
	return output

def get_fastl4profiles(mr):
	fastl4pf =mr.tm.ltm.profile.fastl4s.get_collection()
	#logger.info("after get-tcpprofiles()")
	output = ''

	for apf in fastl4pf:
		if output != '':
			output = output + ':'
		#logger.info('TCP Profile: %s' % atcppf.name)
		output = output + apf.name
	return output
	
def get_httpprofiles(mr):
	httppf = mr.tm.ltm.profile.https.get_collection()
	output = 'none'
	
	for pf in httppf:
		if output != '':
			output = output + ':'
		#logger.info('HTTP profile: %s' % pf.name)
		output = output + pf.name
	#logger.info('output in get_httpprofile: %s' % output)
	return output

def get_pxyhttpprofiles(mr):
	httppf = mr.tm.ltm.profile.https.get_collection()
	output = ''
	
	for pf in httppf:
		if output != '' and pf.proxyType == 'reverse':
			output = output + ':'
		#logger.info('HTTP profile: %s' % pf.name)
		if pf.proxyType == 'reverse':
			output = output + pf.name
	#logger.info('output in get_pxyhttpprofile: %s' % output)
	return output

def get_exphttpprofiles(mr):
	httppf = mr.tm.ltm.profile.https.get_collection()
	output = 'none'
	
	for pf in httppf:
		if output != '' and pf.proxyType == 'explicit':
			output = output + ':'
		#logger.info('HTTP profile: %s' % pf.name)
		if pf.proxyType == 'explicit':
			output = output + pf.name
	#logger.info('output in get_httpprofile: %s' % output)
	return output

def get_transhttpprofiles(mr):
	httppf = mr.tm.ltm.profile.https.get_collection()
	output = 'none'
	
	for pf in httppf:
		if output != '' and pf.proxyType == 'transparent':
			output = output + ':'
		#logger.info('HTTP profile: %s' % pf.name)
		if pf.proxyType == 'transparent':
			output = output + pf.name		

	#logger.info('output in get_httpprofile: %s' % output)
	return output
def get_dnsresolverprofiles(mr):
	dnsRzvs = mr.tm.net.dns_resolvers.get_collection()
	output = 'none'
	
	for pf in dnsRzvs:
		if output != '':
			output = output + ':'
		#logger.info('HTTP profile: %s' % pf.name)
		output = output + pf.name
	#logger.info('output in get_httpprofile: %s' % output)
	return output	

def get_dnsprofiles(mr):
	dnspf = mr.tm.ltm.profile.dns_s.get_collection()
	output = 'none'
	
	for pf in dnspf:
		if output != '':
			output = output + ':'
		#logger.info('HTTP profile: %s' % pf.name)
		output = output + pf.name
	#logger.info('output in get_httpprofile: %s' % output)
	return output
	
def get_clisslprofiles(mr):
	clisslpf = mr.tm.ltm.profile.client_ssls.get_collection()
	output = 'none'
	
	for pf in clisslpf:
		if output != '':
			output = output + ':'
		#logger.info('Client SSL profile: %s' % pf.name)
		output = output + pf.name
	return output	
	
def get_srvsslprofiles(mr):
	srvsslpf = mr.tm.ltm.profile.server_ssls.get_collection()
	output = 'none'
	
	for pf in srvsslpf:
		if output != '':
			output = output + ':'
		#logger.info('Server SSL profile: %s' % pf.name)
		output = output + pf.name
	return output	
		
def get_persistprofiles(mr):
	output = 'none:'
	output = output + get_srcprofiles(mr) + ':'
	output = output + get_dstprofiles(mr) + ':'
	output = output + get_cookieprofiles(mr) + ':'
	output = output + get_sslprofiles(mr) + ':'
	output = output + get_hashprofiles(mr) + ':'
	output = output + get_univprofiles(mr)
	return output
		
def get_cookieprofiles(mr):
	ckppf = mr.tm.ltm.persistence.cookies.get_collection()
	output = ''
	for pf in ckppf:
		if output != '':
			output = output + ':'
		#logger.info('Cookie profile: %s' % pf.name)
		output = output + pf.name
	return output

def get_srcprofiles(mr):
	srcpf = mr.tm.ltm.persistence.source_addrs.get_collection()
	output = ''
	for pf in srcpf:
		if output != '':
			output = output + ':'
		#logger.info('Source profile: %s' % pf.name)
		output = output + pf.name
	return output
		
def get_dstprofiles(mr):
	dstpf = mr.tm.ltm.persistence.dest_addrs.get_collection()
	output = ''
	for pf in dstpf:
		if output != '':
			output = output + ':'
		logger.info('Destination persistence profile: %s' % pf.name)
		output = output + pf.name
	return output
	
def get_hashprofiles(mr):
	hspf = mr.tm.ltm.persistence.hashs.get_collection()
	output = ''
	for pf in hspf:
		if output != '':
			output = output + ':'
		#logger.info('Hash profile: %s' % pf.name)
		output = output + pf.name
	return output
	
	
def get_sslprofiles(mr):
	sslpf = mr.tm.ltm.persistence.ssls.get_collection()
	output = ''
	for pf in sslpf:
		if output != '':
			output = output + ':'
		#logger.info('SSL profile: %s' % pf.name)
		output = output + pf.name
	return output
	
def get_univprofiles(mr):
	unipf = mr.tm.ltm.persistence.universals.get_collection()
	output = ''
	for pf in unipf:
		if output != '':
			output = output + ':'
		#logger.info('Universal profile: %s' % pf.name)
		output = output + pf.name
	return output

def get_ocprofiles(mr):
	ocpf = mr.tm.ltm.profile.one_connects.get_collection()
	output = ''
	for pf in ocpf:
		if output != '':
			output = output + ':'
		#logger.info('Universal profile: %s' % pf.name)
		output = output + pf.name
	return output

def get_strmprofiles(mr):
	strmpf = mr.tm.ltm.profile.streams.get_collection()
	output = ''
	for pf in strmpf:
		if output != '':
			output = output + ':'
		#logger.info('Universal profile: %s' % pf.name)
		output = output + pf.name
	return output

def get_irules(mr):
	unipf = mr.tm.ltm.rules.get_collection()
	output = 'none'
	for pf in unipf:
		if output != '':
			output = output + ':'
		output = output + pf.name
	logger.info('iRules: %s' % output)
	return output
	
def get_snatpools(mr):
	unipf = mr.tm.ltm.snatpools.get_collection()
	output = 'none'
	for pf in unipf:
		if output != '':
			output = output + ':'
		output = output + pf.name
	logger.info('Snat Pools: %s' % output)
	return output

def get_policies(mr):
	unipf = mr.tm.ltm.policys.get_collection()
	output = 'none'
	for pf in unipf:
		if output != '':
			output = output + ':'
		output = output + pf.name

	return output

def get_certs(mr):
	sysCerts = mr.tm.sys.crypto.certs.get_collection()
	logger.info("get_certs() called")
	output = 'none'
	for aCert in sysCerts:
		if output != '':
			output = output + ':'
		output = output + aCert.name
	
	return output

def get_keys(mr):
	sysKeys = mr.tm.sys.crypto.keys.get_collection()
	logger.info("get_keys() called")
	output = 'none'
	for aKey in sysKeys:
		if output != '':
			output = output + ':'
		output = output + aKey.name
		logger.info('Key Name: ' + output)

	return output
	
def get_profiles(active_ltm, pf_type):
	#logger.info('Called get_profiles(): %s %s' % (active_ltm, pf_type))
	
	admpass = getpass.getpass('LTM', 'admin')
	mr = ManagementRoot(str(active_ltm), 'admin', admpass)
	output = ''
	
	'''
	Suppported Profile types
	1. TCP, UDP, Fast L4
	2. PERSIST (Cookie, Source and Destination Affinity, Hash, SSL, Universal)
	3. HTTP, DNS
	4. CLIENTSSL, SERVERSSL
	5. OneConnect
	6. IRULE
	7. SNATPOOL
	8. POLICY
	9. Cert (Updated on Feb 14, 2018)
	10. Key (Updated on Feb 14, 2018)
	'''
	logger.info('Profile Types: %s' % pf_type)
	if pf_type == "TCP":
		output = get_tcpprofiles(mr)
	elif pf_type == "UDP":
		output = get_udpprofiles(mr)
	elif pf_type == "FastL4":
		output = get_fastl4profiles(mr)
	elif pf_type == "PERSIST":
		output = get_persistprofiles(mr)
	elif pf_type == "Cookie":
		output = get_cookieprofiles(mr)
	elif pf_type == "DestAddrAffinity":
		output = get_dstprofiles(mr)
	elif pf_type == "SrcAddrAffinity":
		output = get_srcprofiles(mr)
	elif pf_type == "Hash":
		output = get_hashprofiles(mr)
	elif pf_type == "SSL":
		output = get_sslprofiles(mr)
	elif pf_type == "Universal":
		output = get_univprofiles(mr)
	elif pf_type == "HTTP:reverse":
		output = get_pxyhttpprofiles(mr)
	elif pf_type == "HTTP:explicit":
		output = get_exphttpprofiles(mr)
	elif pf_type == "HTTP:transparent":
		output = get_transhttpprofiles(mr)
	elif pf_type == "HTTP:dnsresolver":
		output = get_dnsresolverprofiles(mr)
	elif pf_type == "HTTP":
		output = get_httpprofiles(mr)
	elif pf_type == "DNS":
		output = get_dnsprofiles(mr)
	elif pf_type == "CLIENTSSL":
		output = get_clisslprofiles(mr)
	elif pf_type == "SERVERSSL":
		output = get_srvsslprofiles(mr)
	elif pf_type == "OneConnect":
		output = get_ocprofiles(mr)
	elif pf_type == "Stream":
		output = get_strmprofiles(mr)
	elif pf_type == "IRULE":
		output = get_irules(mr)
	elif pf_type == "SNATPOOL":
		output = get_snatpools(mr)
	elif pf_type == "POLICY":
		output = get_policies(mr)
	elif pf_type == "CERT":
		logger.info("Cert profile identified!")
		output = get_certs(mr)
	elif pf_type == "KEY":
		logger.info("Key profile identified!")
		output = get_keys(mr)
	
		
	logger.info('output in get_profiles: %s' % output)
	return output

if __name__ == "__main__":
	#logger.info('main called: param1: ')
	print get_profiles(sys.argv[1], sys.argv[2])
