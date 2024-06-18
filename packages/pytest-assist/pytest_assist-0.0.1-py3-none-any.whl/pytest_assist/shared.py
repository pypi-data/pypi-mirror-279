import os

LIB_PATH = os.path.dirname(os.path.abspath(__file__))

class Testing_State:
    inTesting = False
    curTestName = ''
    saveRecord = False
    quitTesting = False

    te = None


class Settings:
    host = '0.0.0.0'
    http_port = 48530
    ws_port = 48531

    # don't change the following settings, in case of fatal files removing
    
    PTC_DIR  =     '.pytest_assist'
    RECORDS_DIR  = f'{PTC_DIR}/records'
    RULES_DIR    = f'{PTC_DIR}/rules_select'
    DOWNLAOD_DIR = f'{PTC_DIR}/download'

    
