import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
XPDBASEPATH = (APP_ROOT + "/data/modelador.db")
INIT_SCRIPT = (APP_ROOT + "/initdata.sql")
WEB_ROOT = (APP_ROOT+"/sitio")
TEMP_ROOT = (APP_ROOT+"/temporal")
PARCHE_ROOT = (APP_ROOT+"/parches")
DELETE_TEMP = False
DEBUG_MODE = False
DOWNLOAD_ENABLED = True
FS_ROOT = ("/storage/emulated/0")
LOCAL_CONFIG = { "DEBUG_MODE" : DEBUG_MODE, "DOWNLOAD_ENABLED" : DOWNLOAD_ENABLED }



