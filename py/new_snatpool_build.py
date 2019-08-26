from f5.bigip import ManagementRoot
import sys
import logging
import json

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

def new_snatpool_build(active_ltm, snat_name, snat_addresses):
    
    mr = ManagementRoot(str(active_ltm), 'admin', 'rlatkdcks')
    
    idx = 1
    strReturn = {str(idx) : 'Snatpool Creation Report'}
    idx += 1
    
    logging.info(str(active_ltm) + " Snatpool DNS:" + str(snat_name) + " Snatpool DEST:" + str(snat_addresses))
    logging.info("Snatpool Creation process has been initiated. Snatpool Name: " + snat_name)
     
    try:
        snat_members=[]
        for aMember in snat_addresses.split(':'):
            snat_members.append(aMember)

        mysnat = mr.tm.ltm.snatpools.snatpool.create(name=snat_name, members=snat_members)
        
        strReturn[str(idx)] = 'Snatpool (' + snat_name + ')  has been succssfully created'
        idx += 1
        
    except Exception as e:
        logging.info("Exception during Snatpool creation")
        strReturn[str(idx)] = "Exception fired!: " + str(e)
        idx += 1
        return json.dumps(strReturn)

    return json.dumps(strReturn)


if __name__ == "__main__":
    print new_snatpool_build(sys.argv[1], sys.argv[2], sys.argv[3])