import sys
import logging
import json
import mysql.connector
from mysql.connector import errorcode
import ConfigParser
import bcrypt


logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def validate_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)

def modpass_ajax(db_ip, curpass, newpass, bigip_type):
    
    idx = 1
    strReturn = {str(idx) : 'Password Administration Report'}
    idx += 1
    
    # Read DB name, DB Admin name and Password
    config = ConfigParser.ConfigParser()
    try:
        config.read('../admin/db.ini')
    except Exception as e:
        logging.info("File Read error: " + str(e))
        strReturn[str(idx)] = 'Failed to read db.ini Error Details: ' + str(e)
        idx += 1
        return json.dumps(strReturn)
    
    strReturn[str(idx)] = 'Successfully read db.ini'
    idx += 1
    
    dbname = config.get('DB_ADMIN', 'DB')
    username = config.get('DB_ADMIN', 'UN')
    password = config.get('DB_ADMIN', 'PW')
    
    #config.close()
    logging.info("DB name: " + dbname + " username: " + username + " password: " + password)
    
    try:
        #logging.info("Try to connection established DB IP: " + db_ip + " Passwd: " + curpass)
        con = mysql.connector.connect(user=username, password=password, database=dbname)
        logging.info("Connection established")
        
        # Update hashed password
        mycursor = con.cursor()
        
        # Validate if the current password is correct
        if bigip_type == 'LTM':
            sql = "SELECT pass FROM bigip_pass WHERE module='LTM' and adminname='admin'"
        elif bigip_type == 'GTM':
            sql = "SELECT pass FROM bigip_pass WHERE module='GTM' and adminname='admin'"
        
        mycursor.execute(sql)
        saved_hashed_pass = mycursor.fetchone()[0]

        logging.info("Entered current PW: " + curpass + " Saved Hashed PW: " + saved_hashed_pass) 
        
        # If the hash of a given current password is matched to saved hashed password, update the password with a new password 
        if validate_password(curpass, saved_hashed_pass):
            newpass_hashed = get_hashed_password(newpass)
            if bigip_type == 'LTM':
                sql = "UPDATE bigip_pass SET pass='" + newpass_hashed + "' WHERE module='LTM' and adminname='admin'"
            elif bigip_type == 'GTM':
                sql = "UPDATE bigip_pass SET pass='" + newpass_hashed + "' WHERE module='GTM' and adminname='admin'"
            logging.info("SQL String: " + sql)
            mycursor.execute(sql)
            con.commit()
        else:
            logging.info("Typed current password is not correct")
            strReturn[str(idx)] = "Typed Current password is not correct"
            idx += 1
            return json.dumps(strReturn)
        
    except Exception as e:
        logging.info("Exception during DB Connection or DB Operation: " + str(e))
        strReturn[str(idx)] = 'Exception during DB Connection or DB Operation. Error Details: ' + str(e)
        idx += 1
        return json.dumps(strReturn)    
    strReturn[str(idx)] = 'Password has been updated successfully'
    idx += 1
        
    return json.dumps(strReturn)


if __name__ == "__main__":
    print modpass_ajax(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
