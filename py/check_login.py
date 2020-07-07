import sys
import logging
import json
import mysql.connector
from mysql.connector import errorcode
import ConfigParser
import bcrypt
import os
import chaniq_util

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def validate_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))

def check_login(un, userPass):
    
    # Read ini path info
    stdNameIniFile = chaniq_util.loadIniConfigVal('CONFIG_PATH_INFO','DB_INI_PATH') + 'db.ini'
    logger.info("check_login() Config File Path:" + stdNameIniFile)
    # Read DB name, DB Admin name and Password
    config = ConfigParser.ConfigParser()
    try:
        # Current working directory decision is tricky as python file is called from php. So I used Absolute Path
        config.read(stdNameIniFile)
        #config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'admin', 'db.ini'))
    except Exception as e:
        logger.info("File Read error: " + str(e))
        return 'ERR'
    logger.info("check_login() Config Section read:" + str(config.sections()))
    
    try:
        dbname = config.get('DB_ADMIN', 'DB')
        username = config.get('DB_ADMIN', 'UN')
        password = config.get('DB_ADMIN', 'PW')
    except Exception as e:
        logger.info("DB info reading failed: " + str(e))
    #config.close()
    
    #logger.info("DB name: " + dbname + " username: " + username + " password: " + password)
    
    try:
        #logger.info("Try to connection established DB IP: " + db_ip + " Passwd: " + userPass)
        con = mysql.connector.connect(user=username, password=password, database=dbname, auth_plugin='mysql_native_password')
        logger.info("Connection established")

        # Update hashed password
        mycursor = con.cursor()
        sql = "SELECT pw FROM users where un='" + un + "'"
        logger.info("SQL String: " + sql)
        mycursor.execute(sql)
        myresult = mycursor.fetchone()
        
        # Convert tuple to String by using join()
        if myresult:
            strMyresult = ''.join(myresult)
        else:
            strMyresult = ''
            
        #logger.info("User entered PW: " + userPass + " returned sql result: " + strMyresult)
        if myresult:
            if(validate_password(userPass, strMyresult)):
                return '1'
            else:
                return '0'
        else:
            return '0'

    except Exception as e:
        logger.info("Exception during DB connection or SQL Execution: " + str(e))
        return 'ERR'    
        
if __name__ == "__main__":
    logger.info("check_login() main")
    print check_login(sys.argv[1], sys.argv[2])