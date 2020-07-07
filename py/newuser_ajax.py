import sys
import logging
import json
import mysql.connector
from mysql.connector import errorcode
import ConfigParser
import bcrypt
from cryptography.fernet import Fernet

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def validate_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)

def encrypt_pw(plain_text_password, key):
    try:
        cipher_suite = Fernet(key.encode('utf-8'))
        cipher_pw = cipher_suite.encrypt(plain_text_password)
    except Exception as e:
        logger.info("Error in encrypt_pw(). Error details: " + str(e))
        strReturn[str(idx)] = "Error in encrypt_pw(). Error details: " + str(e)
        idx += 1
        return json.dumps(strReturn)
    return cipher_pw 

def decrypt_pw(encrypted_pw, key):
    try:
        cipher_suite = Fernet(key.encode('utf-8'))
        plain_pw = cipher_suite.decrypt(encrypted_pw.encode('utf-8'))
    except Exception as e:
        logger.info("Error in decrypt_pw(). Error details: " + str(e))
        logger.info(traceback.format_exc())
        strReturn[str(idx)] = "Error in decrypt_pw(). Error details: " + str(e)
        idx += 1
        return json.dumps(strReturn)
            
    return plain_pw

def generate_symkey():
    return Fernet.generate_key()

def retrieve_symkey(dbcon, bigip_type):
    
    mycursor = dbcon.cursor()
    
    # Validate if the current password is correct
    if bigip_type == 'LTM':
        sql = "SELECT enckey FROM bigip_pass WHERE module='LTM' and adminname='admin'"
    elif bigip_type == 'GTM':
        sql = "SELECT enckey FROM bigip_pass WHERE module='GTM' and adminname='admin'"
    
    mycursor.execute(sql)
    return mycursor.fetchone()[0]

def newuser_ajax(db_ip, un, userrole, pass1):
    
    idx = 1
    strReturn = {str(idx) : 'CHAN-IQ User Creation Report'}
    idx += 1
    
    # Read DB name, DB Admin name and Password
    config = ConfigParser.ConfigParser()
    try:
        config.read('../admin/db.ini')
    except Exception as e:
        logger.info("File Read error: " + str(e))
        strReturn[str(idx)] = 'Failed to read db.ini Error Details: ' + str(e)
        idx += 1
        return json.dumps(strReturn)
    
    strReturn[str(idx)] = 'Successfully read db.ini'
    idx += 1
    
    dbname = config.get('DB_ADMIN', 'DB')
    username = config.get('DB_ADMIN', 'UN')
    password = config.get('DB_ADMIN', 'PW')
    
    #config.close()
    #logger.info("DB name: " + dbname + " username: " + username + " password: " + password)
    
    try:
        #logger.info("Try to connection established DB IP: " + db_ip + " Passwd: " + pass1)
        con = mysql.connector.connect(user=username, password=password, database=dbname, auth_plugin='mysql_native_password')
        logger.info("Connection established")

        #Create hashed password
        hashed_pass = get_hashed_password(pass1)
        #logger.info("Hashed PW: " + hashed_pass)
        # Insert the new user with the hashed password into DB
        mycursor = con.cursor()
        sql = "INSERT INTO users(un,pw,role) VALUES('" + un + "', '" + hashed_pass + "', '" + userrole + "')"
        logger.info("SQL String: " + sql)
        mycursor.execute(sql)
        
        con.commit()
        
    except Exception as e:
        logger.info("Exception during DB connection or SQL execution: " + str(e))
        strReturn[str(idx)] = 'DB Connection or SQL execution failed. Error Details: ' + str(e)
        idx += 1
        return json.dumps(strReturn)    
    strReturn[str(idx)] = 'New user ' + un + ' has been created successfully'
    idx += 1
        
    return json.dumps(strReturn)


if __name__ == "__main__":
    print newuser_ajax(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
