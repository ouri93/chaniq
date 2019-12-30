from f5.bigip import ManagementRoot
import sys
import logging
import json
from f5.bigip.tm.ltm.node import Node
import getpass
import loadStdNames

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO)

# Module global
idx = 0
namebit = 0
ipbit = 0

def check_node_conflict(mr, nodeip, nodename):
    logging.info("Build_nodes - check_node_conflict() nodeip: " + str(nodeip) + " Node Name: " + str(nodename))
    
    nodes = mr.tm.ltm.nodes.get_collection()
    global namebit, ipbit, idx

    for node in nodes:
        if node.exists(name=str(nodename)):
            # Set bit - A bit per node name
            namebit = namebit | (1 << idx)
            logging.info("Name Bit set")
        if node.address == str(nodeip):
            # Set bit - A bit per node IP
            ipbit = ipbit | (1 << idx)
            logging.info("IP Bit set")
    idx += 1

    logging.info("End of Build_nodes - check_node_conflict() namebit: " + str(namebit) + " ipbit: " + str(ipbit))


def build_nodes(active_ltm, pool_membername, pool_memberip):
    
    global namebit, ipbit
    admpass = getpass.getpass('LTM', 'admin')
    mr = ManagementRoot(str(active_ltm), 'admin', admpass)
    #mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    
    nodenames = json.loads(pool_membername)
    nodeips = json.loads(pool_memberip)
    
    # Check if Standard naming is used
    useGlobalNaming = loadStdNames.useStdNaming()
    logging.info("build_node()- Use Standard Global naming : " + useGlobalNaming )
    
    bitmove = 0
    idx = 1
    strReturn = {str(idx) : 'Node Creation Report'}
    logging.info("build_node() : " + str(idx) + "th Node creation")
    
    idx += 1
    
    for nodeip, nodename,  in zip(nodeips, nodenames):
        logging.info("node IP: " + nodeip + " node name: " + nodename)
        
        if useGlobalNaming == '1':
            nodename = loadStdNames.get_std_name(active_ltm, 'LOCAL', 'NODE', '', nodename)
            logging.info("build_node()- Standard Name created : " + nodename )
        nodes = mr.tm.ltm.nodes.get_collection()
        check_node_conflict(mr, nodeip, nodename)
        
        logging.info("build_node() : namebit: " + str(namebit) + " bitmove:" + str(bitmove) + " ipbit: " + str(ipbit))  
        
        # No Node name and Node IP conflict - Create a new node with standard name 
        if ( not (namebit >> bitmove) & 1) and not ( (ipbit >> bitmove) & 1):
            mr.tm.ltm.nodes.node.create(name=nodename, partition='Common', address=nodeip)
            strReturn.update({str(idx) : nodename + " has been added" })
        # Both of Node name and Node IP conflict - Use standard Name
        elif ( (namebit >> bitmove) & 1) and ( (ipbit >> bitmove) & 1):
            strReturn.update({str(idx) : "Existing node will be used" })
        else:
            pass
        idx += 1
        bitmove += 1

    return json.dumps(strReturn)


if __name__ == "__main__":
    print build_nodes(sys.argv[1], sys.argv[2], sys.argv[3])
