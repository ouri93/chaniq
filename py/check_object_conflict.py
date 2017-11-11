from f5.bigip import ManagementRoot
import sys
import logging
import json
import build_std_names

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
# Global Varibale idx
idx = 1
gFoundConflict = False

''' VS name, VIP + port '''
def check_vs_conflict(mr, vs_name, vip):
	
	vs_s = mr.tm.ltm.virtuals.get_collection()
	
	strReturn = {}
	# bitout == 0(Default Value), bitout == 1 (VS Name conflict),
	# bitout == 2 (VS Destination conflict), bitout == 3 (VS name and Destination conflict)  
	bitout = 0

	for vs in vs_s:
		if vs.exists(name=vs_name):
			bitout = bitout | (1 << 0)
		if vs.destination == vip:
			bitout = bitout | (1 << 1)
	
	if (bitout >> 0) & 1:
		strReturn[str(idx)] = 'VS Name conflict(VS Name: ' + vs_name + ')'
		global gFoundConflict
		gFoundConflict = True
	else:
		strReturn[str(idx)] = 'VS Name is unique(VS Name: ' + vs_name + ')'
	global idx
	idx += 1	
	
	if (bitout >> 1) & 1:
		strReturn[str(idx)] = 'VS Destination Conflcit(VS Destionation: ' + vip + ')'
		global gFoundConflict
		gFoundConflict = True
	else:
		strReturn[str(idx)] = 'VS Destination is unique(VS Destionation: ' + vip + ')'
	global idx
	idx += 1
	
	return strReturn

''' Check node IP and name conflict '''
def check_node_conflict(mr, nodeip, nodename):
	#logging.info("check_node_conflict() nodeip: " + nodeip + " Node Name: " + nodename)
	
	nodes = mr.tm.ltm.nodes.get_collection()
	#strReturn = ''
	strReturn = {}
	# bitout == 0(Default Value), bitout == 1 (Name Name conflict),
	# bitout == 2 (Node IP conflict), bitout == 3 (Node name and IP conflict)  
	bitout = 0

	foundConflict = False
	
	for node in nodes:
		if node.exists(name=str(nodename)):
			bitout = bitout | (1 << 0)
		if node.address == str(nodeip):
			bitout = bitout | (1 << 1)
			
	if (bitout >> 0) & 1:
		strReturn[str(idx)] = 'Node Name conflict(Node Name: ' + str(nodename) + ')'
		foundConflict = True		
	else: 
		strReturn[str(idx)] = 'Node Name is unique(Node Name: ' + str(nodename) + ')'
	global idx
	idx += 1

	#logging.info ("idx: " + str(idx) + " value: " + str(strReturn) + "\n")

	if (bitout >> 1) & 1:
		strReturn[str(idx)] = 'Node IP Conflcit(Node IP: ' + str(nodeip) + ')'
		# if both node name and IP conflicts, set gFoundConflict to True (Reuse the existing standard name)
		if not foundConflict:
			global gFoundConflict
			gFoundConflict = True
	else:
		strReturn[str(idx)] = 'Node IP is unique(Node IP: ' + str(nodeip) + ')'
		if foundConflict:
			global gFoundConflict
			gFoundConflict = True
	global idx
	idx += 1
		
	return strReturn
   
def check_pool_conflict(mr, poolname):
	pools = mr.tm.ltm.pools.get_collection()
	
	strReturn = {}
	# bitout == 0(Default Value), bitout == 1 (VS Name conflict),
	# bitout == 2 (VS Destination conflict), bitout == 3 (VS name and Destination conflict)  
	bitout = 0

	for pool in pools:
		if pool.exists(name=poolname):
			bitout = bitout | (1 << 0)
	if (bitout >> 0) & 1:
		strReturn[str(idx)] = 'Pool Name conflict(Pool Name: ' + poolname + ')'
		global gFoundConflict
		gFoundConflict = True		
	else:
		strReturn[str(idx)] = 'Pool Name is unique(Pool Name: ' + poolname + ')'
	global idx
	idx += 1
	
	#logging.info ("Pool check - idx: " + str(idx) + " value: " + str(strReturn) + "\n")
	
	return strReturn

''' Pool member name, pool memner IP'''		
def check_poolmember_conflict():
	pass
		
''' SSL: client and server SSL'''
def check_ssl_conflict():	
	pass

''' Persistence: source, destination, cookie, hash, ssl, universal '''
def check_persistence_conflict():
	pass

''' Services: http, ftp, dns, ... '''
def check_service_conflict():
	pass

''' Protocol: tcp, udp, fastl4, fast http '''
def check_protocol_conflict():
	pass

''' Argument List: active_ltm, vs_env, vs_dnsname, vs_dest, vs_port, vs_poolmembername, pool_memberip, pool_memberport, req_type 
    Checklist for Virtual Server creation (Assumption: Chosen profiles are conflict-free objects)
    - Node IP and Name conflict, Pool name conflict, Virtual Server Name and VIP:port conflict
'''
def check_object_conflict(active_ltm, vs_env, vs_dnsname, vs_dest, vs_port, vs_poolmembername, pool_memberip, pool_memberport):
	# logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)
	logging.info("check_object_conflict()")

	logging.info("LTM Name: " + active_ltm)
	#strReturn = ''
	strReturn = {str(idx):'Object Conflict Report'}
	global idx
	idx += 1
	mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
	
	results = json.loads(vs_poolmembername)
	for item in results:
		logging.info("item: " + item)
			
	# Check Node IP/name conflict
	nodeips = json.loads(pool_memberip)
	nodenames = json.loads(vs_poolmembername)
	for nodeip, nodename in zip(nodeips, nodenames):
		logging.info("node IP: " + nodeip + "node name: " + nodename)
		#strReturn += check_node_conflict(mr, nodeip, nodename)
		strReturn.update(check_node_conflict(mr, nodeip, nodename))
	
	#logging.info ("strReturn value after node check: " + str(strReturn) + "\n")
	
	# Check Pool name conflict
	poolname = build_std_names.build_std_pool_name(vs_env, vs_dnsname, vs_port)
	logging.info("Pool name created: " + poolname)
	#strReturn += check_pool_conflict(mr, poolname)
	strReturn.update(check_pool_conflict(mr, poolname))
	
	#logging.info ("strReturn value after pool check: " + str(strReturn) + "\n")
	
	# Check Virtual Server Name and VIP conflict
	vsname = build_std_names.build_std_vs_name(vs_env, vs_dnsname, vs_port)
	vip = '/Common/' + vs_dest + ':' + vs_port
	logging.info("VS name created: " + vsname + "VIP: " + vip + '\n')
	#strReturn += check_vs_conflict(mr, vsname, vip)
	strReturn.update(check_vs_conflict(mr, vsname, vip))
	
	global gFoundConflict
	if gFoundConflict:
		strReturn.update({str(idx) : '** Configuration conflict **'})
	else:
		strReturn.update({str(idx) : '** No configuration conflict **'})
	global idx
	idx += 1
		
	return json.dumps(strReturn)
'''	
	for nodeip in nodeips:
		logging.info("node IP: " + node)
		strReturn += check_node_conflict(active_ltm, nodeip, nodename)

	fostat = mr.tm.sys.failover.load()
	if "active" in fostat:
		return 1
	else:
		return 0
'''
		
if __name__ == "__main__":
	print check_object_conflict(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
