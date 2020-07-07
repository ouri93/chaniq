import sys
import logging
import mysql.connector
from mysql.connector import errorcode
import ConfigParser
from cryptography.fernet import Fernet
import traceback

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def decrypt_pw(encrypted_pw, key):
    try:
        cipher_suite = Fernet(key.encode('utf-8'))
        plain_pw = cipher_suite.decrypt(encrypted_pw.encode('utf-8'))
    except Exception as e:
        logger.info("Error in decrypt_pw(). Error details: " + str(e))
        logger.info(traceback.format_exc())
        return "Error in decrypt_pw(). Error details: " + str(e)
            
    return plain_pw

def retrieve_symkey(dbcon, bigip_type, username):
    
    mycursor = dbcon.cursor()
    
    # Validate if the current password is correct
    sql = "SELECT enckey FROM bigip_pass WHERE module='" + bigip_type + "' and adminname='" + username + "'"
    logger.info("SQL query: " + sql)

    mycursor.execute(sql)
    return mycursor.fetchone()[0]

def retrieve_cipher_pw(dbcon, bigip_type, username):
    
    mycursor = dbcon.cursor()
    
    # Validate if the current password is correct
    sql = "SELECT pass FROM bigip_pass WHERE module='" + bigip_type + "' and adminname='" + username + "'"
    logger.info("SQL query: " + sql)
    
    mycursor.execute(sql)
    return mycursor.fetchone()[0]

# bigip_type: LMT|GTM, un (Username)
def getpass(bigip_type, un):
    
    # Read DB name, DB Admin name and Password
    config = ConfigParser.ConfigParser()
    try:
        config.read('../admin/db.ini')
    except Exception as e:
        logger.info("File Read error: " + str(e))
    
    dbname = config.get('DB_ADMIN', 'DB')
    username = config.get('DB_ADMIN', 'UN')
    password = config.get('DB_ADMIN', 'PW')
    
    #config.close()
    #logger.info("DB name: " + dbname + " username: " + username + " password: " + password)
    
    try:
        con = mysql.connector.connect(user=username, password=password, database=dbname, auth_plugin='mysql_native_password')
        logger.info("Connection established")
        mycursor = con.cursor()
        
        #''' Code using Cryptography lib
        # Retrieve encryption key from DB
        enc_key = retrieve_symkey(con, bigip_type, un)
        cur_saved_cipher_pw = retrieve_cipher_pw(con, bigip_type, un)
        
        cur_saved_plain_pw = decrypt_pw(cur_saved_cipher_pw, enc_key) 
        #logger.info("Decrypted PW: " + cur_saved_plain_pw)

    except Exception as e:
        logger.info("Exception during DB connection: " + str(e))
  
    return cur_saved_plain_pw