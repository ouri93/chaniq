import ConfigParser
import logging

logging.basicConfig(level=logging.INFO, filename='/var/www/chaniq/log/chaniq-py.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

''' Given Section name and Key name of chaniq.ini file, return corresponding key value from chaniq.ini file '''
def loadIniConfigVal(secName, keyVal):
    
    config = ConfigParser.ConfigParser()
    try:
        config.read('/var/www/chaniq/config/chaniq.ini')
        logger.info('Sections in INI Config read: ' + str(config.sections()))
    except Exception as e:
        logger.info("File Read error: " + str(e))
    
    return config.get(secName, keyVal)

#objName: Object Name, PropName: Property Name of an object, propToCom: Property to compare
#Return true if a given string property of an object is modified. Otherwise return false.
def isStrPropModified(objName, propName, propToCom):
    #logger.info("PropName: " + propName + " GUI Val: " + propToCom)
    try:
        if hasattr(objName, propName):
            logger.info("Loaded PropName: " + getattr(objName, propName))
            if propToCom.rstrip('\r\n') == '' and propToCom.rstrip('\r\n') == 'none':
                #logger.info("Has attribute and GUI val is none:" + propToCom) 
                return True
            else:
                if getattr(objName, propName) != propToCom.rstrip('\r\n'):
                    #logger.info("Has attribute and GUI val is not matching with a loaded val:" + propToCom) 
                    return True
                else: return False
        else:
            if propToCom.rstrip('\r\n') != '' and propToCom.rstrip('\r\n') != 'none':
                #logger.info("No attribute and GUI val is not none:" + propToCom)
                return True
            else: return False
    except Exception as e:
        logger.info("isStrPropModified() exception - Checking String modification failed: " + str(e))
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
        logger.info("isIntPropModified() exception - Checking String modification failed: " + str(e))
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
        logger.info("isListPropModified() exception - Checking List modification failed: " + str(e))
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
        logger.info("isDictPropModified() exception - Checking Dictionary modification failed: " + str(e))
        return False