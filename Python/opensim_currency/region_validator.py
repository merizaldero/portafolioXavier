from contextlib import closing
import sqlite3
import os
from xmlrpc.client import ServerProxy

OS_DB_PATH = os.getenv('OS_BD_PATH',None)
REGION_DB = OS_DB_PATH + os.pathsep + 'OpenSim.db'
DUMMY_MODE = True
OS_SERVER = 'http://xpidersim:9000/'


def __connect_db( database ):
    """Returns a new connection to the database."""
    return sqlite3.connect(database)

def __consultar_escalar(sql,parametros,database):
    resultado = None
    with closing( __connect_db( database ) ) as db:
        cur = db.execute( sql , parametros )
        res = cur.fetchall()
        if len(res) == 1:
            resultado = res[0][0]
    return resultado

def validar_session(agentid, sessionid, sin_region_id = True , regionid = 'abcd'):
    if DUMMY_MODE:
        return agentid
    consulta = "select UserID from Presence where UserID = ? and SecureSessionID = ? "
    parametros = [agentid, sessionid]
    if sin_region_id is False:
        consultas += " and RegionID = ? "
        parametros.append( regionid )
    return __consultar_escalar( consulta, parametros, REGION_DB)

def validar_region(regionid , secret):
    if DUMMY_MODE:
        return regionid
    return __consultar_escalar( "select uuid from regions where uuid = ? and regionSecret = ? ", [regionid, secret], REGION_DB)

def agent_name(agentid):
    if DUMMY_MODE:
        return agentid
    return __consultar_escalar( "select FirstName || ' ' || LastName from UserAccounts where PrincipalID = ? ", [agentid,], REGION_DB)

def user_alert(agentid, soundid, text):
    parametros = [{ 'agentId' : agentid, 'soundID' : soundid, 'text' : text, 'secret' : regionSecret },]
    try:
        with ServerProxy( OS_SERVER ) as proxy:
            proxy.userAlert(parametros)
    except Exception as e:
        print("Error enviando mensaje a agente " + agentid + agentid+"\n" + str(e))

def actualizar_saldo_simulador(agentid):
    try:
        with ServerProxy( OS_SERVER ) as proxy:
            proxy.UpdateBalance({'agentId':agentid})
    except Exception as e:
        print("Error actualizacion de saldo de gente " + agentid+"\n" + str(e))

def actualizar_region(agentid, sessionid, regionid):

    pass
