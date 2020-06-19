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

def resetpass_ajax(db_ip, pass1, bigip_type):
    
    idx = 1
    strReturn = {str(idx) : 'Password Administration Report'}
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
        con = mysql.connector.connect(user=username, password=password, database=dbname)
        logger.info("Connection established")

        #generate Symetric key and encrypt password
        enc_key = generate_symkey()
        encrypted_pw = encrypt_pw(pass1, enc_key)
        #logger.info("Generated Key: " + enc_key)
        # Save the encrypted password to DB
        mycursor = con.cursor()
        if bigip_type == 'LTM':
            sql = "UPDATE bigip_pass SET pass='" + encrypted_pw + "', enckey='" + enc_key + "' WHERE module='LTM' and adminname='admin'"
        elif bigip_type == 'GTM':
            sql = "UPDATE bigip_pass SET pass='" + encrypted_pw + "', enckey='" + enc_key + "' WHERE module='GTM' and adminname='admin'"
        logger.info("SQL String: " + sql)
        mycursor.execute(sql)
        
        con.commit()
        
        
        '''
        hashed_pass = get_hashed_password(pass1)
        logger.info("Hashed Pass: " + hashed_pass)
        
        # Update hashed password
        mycursor = con.cursor()
        if bigip_type == 'LTM':
            sql = "UPDATE bigip_pass SET pass='" + hashed_pass + "' WHERE module='LTM' and adminname='admin'"
        elif bigip_type == 'GTM':
            sql = "UPDATE bigip_pass SET pass='" + hashed_pass + "' WHERE module='GTM' and adminname='admin'"
        logger.info("SQL String: " + sql)
        mycursor.execute(sql)
        
        con.commit()
        '''
    except Exception as e:
        logger.info("Exception during DB connection: " + str(e))
        strReturn[str(idx)] = 'DB Connection failed. Error Details: ' + str(e)
        idx += 1
        return json.dumps(strReturn)    
    strReturn[str(idx)] = 'Password has been successfully reset'
    idx += 1
        
    return json.dumps(strReturn)


if __name__ == "__main__":
    print resetpass_ajax(sys.argv[1], sys.argv[2], sys.argv[3])
