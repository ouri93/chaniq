import sys
import logging
import json
import mysql.connector
from mysql.connector import errorcode
import ConfigParser
import os
import chaniq_util

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def get_one_db_val(tabId, colId, un, userPass):
    
    # Read ini path info
    stdNameIniFile = chaniq_util.loadIniConfigVal('CONFIG_PATH_INFO', 'DB_INI_PATH') + 'db.ini'
    logger.info("get_one_db_val() Config File Path:" + stdNameIniFile)
    # Read DB name, DB Admin name and Password
    config = ConfigParser.ConfigParser()
    try:
        # Current working directory decision is tricky as python file is called from php. So I used Absolute Path
        config.read(stdNameIniFile)
        #config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'admin', 'db.ini'))
    except Exception as e:
        logger.info("File Read error: " + str(e))
        return 'ERR'
    logger.info("get_one_db_val() Config Section read:" + str(config.sections()))
    
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
        con = mysql.connector.connect(user=username, password=password, database=dbname)
        logger.info("Connection established")

        # Update hashed password
        mycursor = con.cursor()
        sql = "SELECT " + colId + " FROM " + tabId + " WHERE un='" + un + "'"
        logger.info("SQL String: " + sql)
        mycursor.execute(sql)
        myresult = mycursor.fetchone()
        
        # Convert tuple to String by using join()
        if myresult:
            strMyresult = ''.join(myresult)
        else:
            strMyresult = ''
        #logger.info("User entered PW: " + userPass + " returned sql result: " + strMyresult)

        return strMyresult

    except Exception as e:
        logger.info("Exception during DB connection or SQL Execution: " + str(e))
        return 'ERR'    
        
if __name__ == "__main__":
    logger.info("get_one_db_val() main")
    print get_one_db_val(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])