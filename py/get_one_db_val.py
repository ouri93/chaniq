import sys
import logging
import json
import mysql.connector
from mysql.connector import errorcode
import ConfigParser
import os
import chaniq_util

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

def get_one_db_val(tabId, colId, un, userPass):
    
    # Read ini path info
    stdNameIniFile = chaniq_util.loadConfigPath('DB_INI_PATH') + 'db.ini'
    logging.info("get_one_db_val() Config File Path:" + stdNameIniFile)
    # Read DB name, DB Admin name and Password
    config = ConfigParser.ConfigParser()
    try:
        # Current working directory decision is tricky as python file is called from php. So I used Absolute Path
        config.read(stdNameIniFile)
        #config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'admin', 'db.ini'))
    except Exception as e:
        logging.info("File Read error: " + str(e))
        return 'ERR'
    logging.info("get_one_db_val() Config Section read:" + str(config.sections()))
    
    try:
        dbname = config.get('DB_ADMIN', 'DB')
        username = config.get('DB_ADMIN', 'UN')
        password = config.get('DB_ADMIN', 'PW')
    except Exception as e:
        logging.info("DB info reading failed: " + str(e))
    #config.close()
    
    logging.info("DB name: " + dbname + " username: " + username + " password: " + password)
    
    try:
        #logging.info("Try to connection established DB IP: " + db_ip + " Passwd: " + userPass)
        con = mysql.connector.connect(user=username, password=password, database=dbname)
        logging.info("Connection established")

        # Update hashed password
        mycursor = con.cursor()
        sql = "SELECT " + colId + " FROM " + tabId + " WHERE un='" + un + "'"
        logging.info("SQL String: " + sql)
        mycursor.execute(sql)
        myresult = mycursor.fetchone()
        
        # Convert tuple to String by using join()
        if myresult:
            strMyresult = ''.join(myresult)
        else:
            strMyresult = ''
        logging.info("User entered PW: " + userPass + " returned sql result: " + strMyresult)

        return strMyresult

    except Exception as e:
        logging.info("Exception during DB connection or SQL Execution: " + str(e))
        return 'ERR'    
        
if __name__ == "__main__":
    logging.info("get_one_db_val() main")
    print get_one_db_val(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])