import xpd_orm as orm
from os.path import abspath , dirname, exists

from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH
from bottle import Bottle

import xpd_usr

from hashlib import sha256

from uuid import uuid4

PATH_BDD = dirname(abspath(__file__)) + "/data/base.db"
PATH_INIT = dirname(abspath(__file__)) + "/data/init_pymvu.sql"
PATH_DELTA = dirname(abspath(__file__)) + "/data/delta_pymvu.sql"

RUTA_BASE = ""

TiposModelo = orm.Entidad()
TiposModelo.setMetamodelo({
    "nombreTabla":"TIPO_MODELO",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDSTRING, "tamano":16, "pk":True, },
        { "nombre":"nombre", "nombreCampo":"NOMBRE", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"activo", "nombreCampo":"ACTIVO", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findAll", "orderByClause":["nombre"] },
        ]
    })

Modelos = orm.Entidad()
Modelos.setMetamodelo({
    "nombreTabla":"MODELO",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDSTRING, "tamano":64, "pk":True, },
        { "nombre":"descripcion", "nombreCampo":"DESCRIPCION", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"id_tipo_modelo", "nombreCampo":"ID_TIPO_MODELO", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"url", "nombreCampo":"URL", "tipo":orm.XPDSTRING, "tamano":128, },
        { "nombre":"activo", "nombreCampo":"ACTIVO", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findByAmistad", "whereClause":["id_amistad"] },
        ]
    })

TiposPrenda = orm.Entidad()
TiposPrenda.setMetamodelo({
    "nombreTabla":"TIPO_PRENDA",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDSTRING, "tamano":16, "pk":True, },
        { "nombre":"nombre", "nombreCampo":"NOMBRE", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"activo", "nombreCampo":"ACTIVO", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findAll", "orderByClause":["nombre"] },
        { "nombre":"findByActivo", "whereClause":["activo"], "orderByClause":["nombre"] },
        ]
    })

TiposAvatar = orm.Entidad()
TiposAvatar.setMetamodelo({
    "nombreTabla":"TIPO_AVATAR",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDSTRING, "tamano":16, "pk":True, },
        { "nombre":"nombre", "nombreCampo":"NOMBRE", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"activo", "nombreCampo":"ACTIVO", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findAll", "orderByClause":["nombre"] },
        { "nombre":"findByActivo", "whereClause":["activo"], "orderByClause":["nombre"] },
        ]
    })

TiposPrendaTipoAvatar = orm.Entidad()
TiposPrendaTipoAvatar.setMetamodelo({
    "nombreTabla":"TIPO_PRENDA_TIPO_AVATAR",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"id_tipo_avatar", "nombreCampo":"ID_TIPO_AVATAR", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"id_tipo_prenda", "nombreCampo":"ID_TIPO_PRENDA", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"activo", "nombreCampo":"ACTIVO", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findByTipoAvatar", "whereClause":["id_tipo_avatar","activo"], },
        ]
    })

Prendas = orm.Entidad()
Prendas.setMetamodelo({
    "nombreTabla":"PRENDA",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"nombre", "nombreCampo":"NOMBRE", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"descripcion", "nombreCampo":"DESCRIPCION", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"id_tipo_avatar", "nombreCampo":"ID_TIPO_AVATAR", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"id_tipo_prenda", "nombreCampo":"ID_TIPO_PRENDA", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"id_modelo", "nombreCampo":"ID_MODELO", "tipo":orm.XPDSTRING, "tamano":64, },
        { "nombre":"default_tipo_prenda", "nombreCampo":"DEFAULT_TIPO_PRENDA", "tipo":orm.XPDINTEGER, },
        { "nombre":"activo", "nombreCampo":"ACTIVO", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findByTipoPrenda", "whereClause":["id_tipo_prenda","activo"] },
        { "nombre":"findByTipoAvatarDefault", "whereClause":["id_tipo_avatar","default_tipo_prenda","activo"] },
        { "nombre":"findByTipoAvatarTipoPrenda", "whereClause":["id_tipo_avatar","id_tipo_prenda","activo"] },
        ]
    })

Apariencias = orm.Entidad()
Apariencias.setMetamodelo({
    "nombreTabla":"APARIENCIA",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"nombre", "nombreCampo":"NOMBRE", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"descripcion", "nombreCampo":"DESCRIPCION", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"id_usuario", "nombreCampo":"ID_USUARIO", "tipo":orm.XPDINTEGER, },
        { "nombre":"id_tipo_avatar", "nombreCampo":"ID_TIPO_AVATAR", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"es_default", "nombreCampo":"ES_DEFAULT", "tipo":orm.XPDINTEGER, },
        { "nombre":"activo", "nombreCampo":"ACTIVO", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findById", "whereClause":["id"], },
        { "nombre":"findByUsuario", "whereClause":["id_usuario", "activo"], "orderByClause":["es_default", "nombre"] },
        ]
    })

PrendasApariencia = orm.Entidad()
PrendasApariencia.setMetamodelo({
    "nombreTabla":"PRENDA_APARIENCIA",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"id_apariencia", "nombreCampo":"ID_APARIENCIA", "tipo":orm.XPDINTEGER, },
        { "nombre":"id_tipo_prenda", "nombreCampo":"ID_TIPO_PRENDA", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"id_prenda", "nombreCampo":"ID_PRENDA", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findByApariencia", "whereClause":["id_apariencia"], "orderByClause":["id_prenda"] },
        { "nombre":"findByAparienciaTipoPrenda", "whereClause":["id_apariencia", "id_tipo_prenda"], },
        { "nombre":"findById", "whereClause":["id"], },
        ]
    })

Salas = orm.Entidad()
Salas.setMetamodelo({
    "nombreTabla":"SALA",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"nombre", "nombreCampo":"NOMBRE", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"descripcion", "nombreCampo":"DESCRIPCION", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"id_usuario_propietario", "nombreCampo":"ID_USUARIO_PROPIETARIO", "tipo":orm.XPDINTEGER, },
        { "nombre":"id_modelo", "nombreCampo":"ID_MODELO", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"privado", "nombreCampo":"PRIVADO", "tipo":orm.XPDINTEGER, },
        { "nombre":"activo", "nombreCampo":"ACTIVO", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findByPrivadoActivo", "whereClause":["privado", "activo"], "orderByClause":["nombre"] },
        { "nombre":"findByUsuarioPrivadoActivo", "whereClause":["id_usuario_propietario","privado", "activo"], "orderByClause":["nombre"] },
        ]
    })

def inicializar():
    entidades = [ TiposModelo, Modelos, TiposPrenda, TiposAvatar, TiposPrendaTipoAvatar, Prendas, Apariencias, PrendasApariencia, Salas ]
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
    
def transaccionar(llamado,objeto):
    con = orm.Conexion(PATH_BDD)
    try:
        llamado(con, objeto)
        con.commit()
    except Exception as ex:
        con.rollback()
        print(repr(ex))
        raise Exception( str(ex) )
    finally:
        con.close()
    return objeto

def consultar( EntityManager:orm.Entidad ,namedQuery, parametros):
    con = orm.Conexion(PATH_BDD)
    try:
        resultado = EntityManager.getNamedQuery(con, namedQuery , parametros)
    except Exception as ex:
        print(repr(ex))
        raise Exception( str(ex) )
    finally:
        con.close()
    return resultado
      
# Caso de Uso: Pagina Principal

def servir_main():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    else:
        return template('main', usuario = usuario)
    
def servir_inicializar():
    inicializar()
    return 'PIMVU inicializado'

# Caso de Uso Gestionar Apariencias

def servir_pag_apariencias():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    return template("apariencia", usuario = usuario)

def crearPrendaAparienciaDefaultPorTipoAvatar( con, id_apariencia, id_tipo_avatar ):
    tipos_prenda = TiposPrenda.getNamedQuery(con, 'findByActivo', { 'activo': 1 })
    prendas = Prendas.getNamedQuery(con, 'findByTipoAvatarDefault', { "id_tipo_avatar":id_tipo_avatar, "default_tipo_prenda":1, "activo":1 })
    prendas_apariencia_actual = PrendasApariencia.getNamedQuery(con, 'findByApariencia', { 'id_apariencia' : id_apariencia } )
    for tipo_prenda in tipos_prenda:
        id_tipo_prenda = tipo_prenda['id']
        id_prenda = [x['id'] for x in prendas if x['id_tipo_prenda'] == id_tipo_prenda]
        if len(id_prenda) == 0:
            id_prenda = None
        else:
            id_prenda = id_prenda[0]
        prenda_apariencia_actual = [x for x in prendas_apariencia_actual if x['id_tipo_prenda'] == id_tipo_prenda ]
        if len(prenda_apariencia_actual) == 0:
            prenda_apariencia_actual = { "id_apariencia":id_apariencia, 'id_tipo_prenda': id_tipo_prenda, 'id_prenda': id_prenda}
            PrendasApariencia.insertar(con, prenda_apariencia_actual)
            print('Creado Prenda Apariencia {0}'.format(repr(prenda_apariencia_actual)))
        else:
            prenda_apariencia_actual = prenda_apariencia_actual[0]
            prenda_apariencia_actual['id_prenda'] = id_prenda
            PrendasApariencia.actualizar(con, prenda_apariencia_actual)
            print('Actualizado Prenda Apariencia {0}'.format(repr(prenda_apariencia_actual)))

def crearApariencia(con, apariencia):
    Apariencias.insertar(con, apariencia)
    crearPrendaAparienciaDefaultPorTipoAvatar(con, apariencia['id'],apariencia['id_tipo_avatar'])
    return apariencia

def servir_api_get_apariencias():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error(401)
    print('Recuperando apariencias para usuario {0}'.format(usuario['username']))
    lista = consultar(Apariencias, 'findByUsuario', {'id_usuario':usuario['id'] , 'activo' : 1})
    if len(lista) == 0:
        # Si no hay listas, crea una por defecto
        apariencia = transaccionar( crearApariencia, {'nombre':'Default', 'descripcion':'Apariencia Default', 'id_usuario': usuario['id'], 'id_tipo_avatar': 'FEMALE', 'es_default':1, 'activo': 1})
        lista.append(apariencia)
    return { 'apariencias': lista }

def servir_api_crear_apariencia():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error(401)
    nombre = request.forms.get('nombre','Nuevo')
    nueva_apariencia = {'nombre':nombre, 'descripcion':'Nueva apariencia', 'id_usuario': usuario['id'], 'id_tipo_avatar': 'FEMALE', 'es_default':0, 'activo': 1}
    transaccionar( crearApariencia, nueva_apariencia )
    return { 'apariencia':nueva_apariencia }

def servir_api_get_tipos_prenda():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        return error(401)
    lista = consultar(TiposPrenda, 'findByActivo', { 'activo' : 1})
    return { 'tipos_prenda': lista }

def servir_api_get_tipos_avatar():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        return error(401)
    lista = consultar(TiposAvatar, 'findByActivo', { 'activo' : 1})
    return { 'tipos_avatar': lista }

def servir_api_get_prendas_apariencia(id_apariencia):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        return error(401)
    sql = """
select a.id as id, a.id_apariencia id_apariencia, a.id_tipo_prenda id_tipo_prenda, a.id_prenda id_prenda, b.nombre nombre, c.url url, b.id_modelo id_modelo
from PRENDA_APARIENCIA a left join PRENDA b on b.id = a.id_prenda and b.activo = :activo left join MODELO c on c.id = b.id_modelo
where a.id_apariencia = :id_apariencia
order by a.id_tipo_prenda
"""
    con = orm.Conexion(PATH_BDD)
    lista = con.consultar(sql,{'id_apariencia':id_apariencia, 'activo':1 },['id', 'id_apariencia','id_tipo_prenda','id_prenda','nombre','url', 'id_modelo'])
    con.close()
    return {'prendas_apariencia' : lista}
    
def servir_api_get_prendas_tipo_avatar_tipo_prenda(id_tipo_avatar, id_tipo_prenda):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        return error(401)
    sql = """
select a.id id, a.nombre nombre, a.descripcion descripcion, a.id_modelo id_modelo, b.url url, a.activo activo
from PRENDA a left join MODELO b on b.id = a.id_modelo
where a.id_tipo_avatar = :id_tipo_avatar and a.id_tipo_prenda = :id_tipo_prenda and a.activo = :activo  
"""
    con = orm.Conexion(PATH_BDD)
    lista = con.consultar(sql,{'id_tipo_avatar':id_tipo_avatar, 'id_tipo_prenda': id_tipo_prenda, 'activo':1 },['id', 'nombre','descripcion','id_modelo','url','activo'])
    con.close()    
    return {'prendas': lista}

def actualizar_apariencia(con, info):
    id_apariencia = info['id_apariencia']
    campo = info['campo']
    valor = info['valor']
    apariencias = Apariencias.getNamedQuery(con, 'findById', {'id': id_apariencia})
    if len(apariencias) == 0 :
        raise Exception('Apariencia no existe')
    if campo not in apariencias[0].keys():
        raise Exception('Campo no valido')
    apariencias[0][campo] = valor
    Apariencias.actualizar(con, apariencias[0])

    if campo == 'id_tipo_avatar':
        crearPrendaAparienciaDefaultPorTipoAvatar( con, id_apariencia, valor )
    
    elif campo == 'es_default':
        apariencias1 = Apariencias.getNamedQuery(con, 'findByUsuario', {'id_usuario': apariencias[0]['id_usuario'], 'activo':1})
        for apariencia_no_def in [x for x in apariencias1 if x['id'] != apariencias[0]['id']  ]:
            apariencia_no_def['es_default'] = 0
            Apariencias.actualizar(con, apariencia_no_def)    

def servir_api_actualizar_apariencia(id_apariencia):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        return error(401)
    campo = request.forms.get('campo', '')
    valor = request.forms.get('valor', None)

    transaccionar(actualizar_apariencia, {'id_apariencia':id_apariencia, 'campo':campo, 'valor':valor })

    return {'resultado':'ok'}

def actualizar_prenda_apariencia(con, prenda_pariencia):
    prenda_apariencia_actual = PrendasApariencia.getNamedQuery(con, 'findById',{'id':prenda_pariencia['id'] })
    if len(prenda_apariencia_actual) == 0:
        raise Exception("Prenda apariencia no existe")
    prenda_apariencia_actual[0]['id_prenda'] = prenda_pariencia['id_prenda']
    PrendasApariencia.actualizar(con, prenda_apariencia_actual[0])

def servir_api_post_prenda_apariencia(id_prenda_apariencia):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        return error(401)
    
    id_prenda = request.forms.get('id_prenda', None)
    if id_prenda is None:
        return error(401)
    
    transaccionar(actualizar_prenda_apariencia, {'id': id_prenda_apariencia, 'id_prenda':id_prenda})
    
    return {'resultado':'ok'}

# Caso uso script deltas:

def ejecutar_delta(con, info):
    if exists( PATH_DELTA ):
        con.ejecutarFileScript( PATH_DELTA )
        print("Delta ejecutado exitosamente")

def servir_delta():
    transaccionar(ejecutar_delta, {})
    return "Delta ejecutado exitosamente"

# Caso de Uso Listado de Salas

def servir_get_listado_salas():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    sql = """
select a.ID id, a.NOMBRE nombre, a.DESCRIPCION descripcion, a.ID_MODELO modelo, b.URL url, a.ID_USUARIO_PROPIETARIO id_usuario_propietario, c.USERNAME username_propietario, a.PRIVADO privado, a.ACTIVO activo
from SALA a 
left join MODELO b on b.ID = a.ID_MODELO
left join USUARIOS c on c.ID = a.ID_USUARIO_PROPIETARIO
where a.ACTIVO = 1
and (a.PRIVADO = 0 or a.ID_USUARIO_PROPIETARIO = :id_usuario)
order by a.PRIVADO, a.NOMBRE
"""
    con = orm.Conexion(PATH_BDD)
    lista = con.consultar( sql, {'id_usuario':usuario['id'] }, ['id', 'nombre','descripcion','id_modelo','url', 'id_usuario_propietario', 'username_propietario', 'privado','activo'] )
    con.close()
    return template("salas", usuario = usuario, salas = lista )

# Caso de Uso Despliegue de Sala 

def servir_get_ingresar_sala(id_sala):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    sql = """
select a.ID id, a.NOMBRE nombre, a.DESCRIPCION descripcion, a.ID_MODELO modelo, b.URL url, a.ID_USUARIO_PROPIETARIO id_usuario_propietario, c.USERNAME username_propietario, a.PRIVADO privado, a.ACTIVO activo
from SALA a 
left join MODELO b on b.ID = a.ID_MODELO
left join USUARIOS c on c.ID = a.ID_USUARIO_PROPIETARIO
where a.ID = :id_sala
"""
    con = orm.Conexion(PATH_BDD)
    lista = con.consultar( sql, {'id_sala':id_sala }, ['id', 'nombre','descripcion','id_modelo','url', 'id_usuario_propietario', 'username_propietario', 'privado','activo'] )
    con.close()
    if len(lista) == 0:
        return error(404)
        
    return template("sala", usuario = usuario, sala = lista[0] )

# Ruteos hacia Bottle
def rutearModulo( app : Bottle, ruta_base : str ):
    # encapsula Session Middleware
    RUTA_BASE = ruta_base
    app.route( ruta_base + '/main' , method = ['GET'])(servir_main)
    # app.route( ruta_base + '/inicializar' , method = ['GET'])(servir_inicializar)
    app.route( ruta_base + '/delta' , method = ['GET'])(servir_delta)

    app.route( ruta_base + '/apariencia' , method = ['GET'])(servir_pag_apariencias)
    app.route( ruta_base + '/api/apariencias' , method = ['GET'])(servir_api_get_apariencias)

    app.route( ruta_base + '/api/tipos_prenda' , method = ['GET'])(servir_api_get_tipos_prenda)
    app.route( ruta_base + '/api/tipos_avatar' , method = ['GET'])(servir_api_get_tipos_avatar)

    app.route( ruta_base + '/api/tipo_avatar/<id_tipo_avatar>/tipo_prenda/<id_tipo_prenda>/prendas' , method = ['GET'])(servir_api_get_prendas_tipo_avatar_tipo_prenda)

    app.route( ruta_base + '/api/apariencia/<id_apariencia:int>/prendas_apariencia' , method = ['GET'])(servir_api_get_prendas_apariencia)
    app.route( ruta_base + '/api/apariencia/<id_apariencia:int>' , method = ['POST'])(servir_api_actualizar_apariencia)
    
    app.route( ruta_base + '/api/prenda_apariencia/<id_prenda_apariencia:int>' , method = ['POST'])(servir_api_post_prenda_apariencia)
    app.route( ruta_base + '/api/nueva_apariencia' , method = ['POST'])(servir_api_crear_apariencia)

    app.route( ruta_base + '/chats' , method = ['GET'])(servir_get_listado_salas)
    app.route( ruta_base + '/chat/<id_sala:int>' , method = ['GET'])(servir_get_ingresar_sala)

