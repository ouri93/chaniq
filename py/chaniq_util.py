import ConfigParser
import logging

logging.basicConfig(filename='/var/log/chaniq-py.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

# Given INI Type, read the ini file path info from main configuration file, chaniq.ini
def loadConfigPath(iniType):
    
    config = ConfigParser.ConfigParser()
    try:
        config.read('/var/www/chaniq/config/chaniq.ini')
        logging.info('Sections in INI Config read: ' + str(config.sections()))
    except Exception as e:
        logging.info("File Read error: " + str(e))
    
    return config.get('CONFIG_PATH_INFO', iniType)

#objName: Object Name, PropName: Property Name of an object, propToCom: Property to compare
#Return true if a given string property of an object is modified. Otherwise return false.
def isStrPropModified(objName, propName, propToCom):
    #logging.info("PropName: " + propName + " GUI Val: " + propToCom)
    try:
        if hasattr(objName, propName):
            logging.info("Loaded PropName: " + getattr(objName, propName))
            if propToCom.rstrip('\r\n') == '' and propToCom.rstrip('\r\n') == 'none':
                #logging.info("Has attribute and GUI val is none:" + propToCom) 
                return True
            else:
                if getattr(objName, propName) != propToCom.rstrip('\r\n'):
                    #logging.info("Has attribute and GUI val is not matching with a loaded val:" + propToCom) 
                    return True
                else: return False
        else:
            if propToCom.rstrip('\r\n') != '' and propToCom.rstrip('\r\n') != 'none':
                #logging.info("No attribute and GUI val is not none:" + propToCom)
                return True
            else: return False
    except Exception as e:
        logging.info("isStrPropModified() exception - Checking String modification failed: " + str(e))
        return False

#objName: Object Name, PropName: Property Name of an object, propToCom: Property to compare, defPropVal: Integer property default value
#Return true if a given Integer property of an object is modified. Otherwise return false.
def isIntPropModified(objName, propName, propToCom, defPropVal):
    try:
        if hasattr(objName, propName):
            if int(propToCom) != defPropVal: return True
            else:
                if getattr(objName, propName) != int(propToCom): return True
                else: return False
        else:
            if int(propToCom) != defPropVal:
                return True
            else: return False
    except Exception as e:
        logging.info("isIntPropModified() exception - Checking String modification failed: " + str(e))
        return False
    

#objName: Object Name, PropName: Property Name of an object, propToCom: List to compare
#Return true if a given List of an object is modified. Otherwise return false.
def isListPropModified(objName, propName, propToCom):
    try:
        if hasattr(objName, propName):
            # If List property is empty
            if not propToCom: return True
            else:
                # Sort list for the comparison
                L1 = getattr(objName, propName)
                L2 = propToCom
                L1.sort()
                L2.sort()
                if L1 != L2: return True
                else: return False
        else:
            if propToCom:
                return True
            else: return False
    except Exception as e:
        logging.info("isListPropModified() exception - Checking List modification failed: " + str(e))
        return False

#objName: Object Name, PropName: Property Name of an object, propToCom: Dictionary to compare
#Return true if a given Dictionary of an object is modified. Otherwise return false.
def isDictPropModified(objName, propName, propToCom):
    try:
        if hasattr(objName, propName):
            # If Dictionary is empty
            if not propToCom: return True
            else:
                # Dictionary comparions
                for k in propToCom.iterkeys():
                    if objName[k] == propToCom[k]:
                        pass
                    else:
                        return True
                return False
        else:
            if propToCom:
                return True
            else: return False
    except Exception as e:
        logging.info("isDictPropModified() exception - Checking Dictionary modification failed: " + str(e))
        return False