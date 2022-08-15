from os.path import abspath , dirname, exists
import datetime
import uuid
import hashlib
import xpd_orm as orm


PATH_BDD = dirname(abspath(__file__)) + "/data/sessions.db"
PATH_INIT = dirname(abspath(__file__)) + "/data/sessions_init.sql"

Sesiones = orm.Entidad()
Sesiones.setMetamodelo({
    "nombreTabla":"SESION",
    "propiedades":[
        {
            "nombre":"user_id",
            "nombreCampo":"USER_ID",
            "tipo":orm.XPDSTRING,
            "tamano":36,
            "pk":True,
            },
        {
            "nombre":"user_name",
            "nombreCampo":"USER_NAME",
            "tipo":orm.XPDSTRING,
            "tamano":16,
            },
        {
            "nombre":"request_id",
            "nombreCampo":"REQUEST_ID",
            "tipo":orm.XPDSTRING,
            "tamano":32,
            },
        {
            "nombre":"session_id",
            "nombreCampo":"SESSION_ID",
            "tipo":orm.XPDSTRING,
            "tamano":32,
            },
        {
            "nombre":"activa",
            "nombreCampo":"ACTIVA",
            "tipo":orm.XPDINTEGER,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findByRequestSessionId",
            "whereClause":["request_id","session_id"],
            "orderBy":["user_id"]
            },
        {
            "nombre":"findByUserId",
            "whereClause":["user_id"],
            },
        ]
    })

RequestHists = orm.Entidad()
RequestHists.setMetamodelo({
    "nombreTabla":"REQUEST_HIST",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "incremental":True,
            "pk":True,
            },
        {
            "nombre":"user_id",
            "nombreCampo":"USER_ID",
            "tipo":orm.XPDSTRING,
            "tamano":36,
            },
        {
            "nombre":"request_id",
            "nombreCampo":"REQUEST_ID",
            "tipo":orm.XPDSTRING,
            "tamano":32,
            },
        {
            "nombre":"fecha",
            "nombreCampo":"FECHA",
            "tipo":orm.XPDSTRING,
            "tamano":19,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findByUserRequestId",
            "whereClause":["user_id","request_id"],
            },
        {
            "nombre":"findByUserId",
            "whereClause":["user_id"],
            "orderBy":["fecha"],
            },
        ]
    })

no_validos = ['','None']

def inicializar():
    entidades = [Sesiones, RequestHists]
    con = orm.Conexion(PATH_BDD)
    try:
        for entidad in entidades:
            entidad.crearTabla(con)
        if exists( PATH_INIT ):
            con.ejecutarFileScript( PATH_INIT )
        con.commit()
    except Exception as ex:
        con.rollback()
        print(ex)
        raise Exception(str(ex))
    finally:
        con.close()

def crear_sesion(request_id, user_id, user_name):

    if len([ a for a in [ str(request_id).strip() , str(user_id).strip(), str(user_name).strip() ] if a in no_validos ]) > 0 :
        raise Exception('Entrada no es valida :{0}, {1}, {2}'.format(request_id, user_id, user_name));

    request_id_hash = hashlib.md5( request_id.encode() ).hexdigest()

    resultado = None

    con = orm.Conexion(PATH_BDD)
    try:

        # valida que el usuario no haya utilizado la misma request_id
        historicos = RequestHists.getNamedQuery(con , 'findByUserRequestId',{'user_id': user_id, 'request_id': request_id_hash})
        if len(historicos) > 0 :
            raise Exception('Request id ya utilizado por usuario')

        session_id = str(uuid.uuid4())
        session_id_hash = hashlib.md5( session_id.encode() ).hexdigest()

        # Asegura persistencia de sesion
        sesiones = Sesiones.getNamedQuery(con , 'findByUserId',{'user_id': user_id})
        if len(sesiones) == 1:
            sesion = sesiones[0]
            sesion['request_id'] = request_id_hash
            sesion['session_id'] = session_id_hash
            sesion['activa'] = 1
            Sesiones.actualizar(con, sesion)
        else:
            sesion = {'user_id': user_id, 'user_name': user_name,'request_id': request_id_hash, 'session_id': session_id_hash, 'activa':1}
            Sesiones.insertar(con, sesion)

        # Asegura persistencia de Historico

        historico = {'user_id': user_id, 'request_id': request_id_hash,'fecha': datetime.datetime.now().isoformat(sep = ' ')[:16] }
        RequestHists.insertar(con, historico)

        resultado = {'user_id': user_id, 'user_name': user_name,'request_id': request_id, 'session_id': session_id}

        con.commit()

    except Exception as ex:
        con.rollback()
        print(repr(ex))
        raise ex
    finally:
        con.close()
    return resultado

def validar_sesion( request_id, session_id, requerir_activa = False):

    request_id_hash = hashlib.md5( request_id.encode() ).hexdigest()
    session_id_hash = hashlib.md5( session_id.encode() ).hexdigest()

    sesion = None
    con = orm.Conexion(PATH_BDD)
    try:
        sesiones = Sesiones.getNamedQuery(con , 'findByRequestSessionId',{ 'request_id': request_id_hash, 'session_id': session_id_hash } )
        if len(sesiones) != 1:
            raise Exception('Autenticacion Rechazada')
        sesion = sesiones[0]
        if requerir_activa and sesion['activa'] == 0:
            raise Exception('Autenticacion Caducada')
        elif sesion['activa'] == 1:
            sesion['activa'] = 0
            Sesiones.actualizar(con, sesion)
        con.commit()
    except Exception as ex:
        con.rollback()
        print(repr(ex))
        raise ex
    finally:
        con.close()

    sesion['request_id'] = request_id
    sesion['session_id'] = session_id
    return sesion
