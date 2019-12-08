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

def resetpass_ajax(db_ip, pass1):
    
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
        #logging.info("Try to connection established DB IP: " + db_ip + " Passwd: " + pass1)
        con = mysql.connector.connect(user=username, password=password, database=dbname)
        logging.info("Connection established")
        
        hashed_pass = get_hashed_password(pass1)
        logging.info("Hashed Pass: " + hashed_pass)
        
        # Update hashed password
        mycursor = con.cursor()
        sql = "UPDATE bigip_pass SET pass='" + hashed_pass + "' WHERE module='LTM' and adminname='admin'"
        logging.info("SQL String: " + sql)
        mycursor.execute(sql)
        
        con.commit()
        
    except Exception as e:
        logging.info("Exception during DB connection: " + str(e))
        strReturn[str(idx)] = 'DB Connection failed. Error Details: ' + str(e)
        idx += 1
        return json.dumps(strReturn)    
    strReturn[str(idx)] = 'Password has been successfully reset'
    idx += 1
        
    return json.dumps(strReturn)


if __name__ == "__main__":
    print resetpass_ajax(sys.argv[1], sys.argv[2])
