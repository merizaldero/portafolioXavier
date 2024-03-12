import xpd_orm as orm
from os.path import abspath , dirname, exists

from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH
from bottle import Bottle

from hashlib import sha256

from uuid import uuid4

PATH_BDD = dirname(abspath(__file__)) + "/data/base.db"
PATH_INIT = dirname(abspath(__file__)) + "/data/init_usr.sql"
RUTA_BASE = ""

Usuarios = orm.Entidad()
Usuarios.setMetamodelo({
    "nombreTabla":"USUARIOS",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            "incremental":True,
            },
        {
            "nombre":"username",
            "nombreCampo":"USERNAME",
            "tipo":orm.XPDSTRING,
            "tamano":32,
            },
        {
            "nombre":"pwd",
            "nombreCampo":"PWD",
            "tipo":orm.XPDSTRING,
            "tamano":128,
            },
        {
            "nombre":"email",
            "nombreCampo":"EMAIL",
            "tipo":orm.XPDSTRING,
            "tamano":32,
            },
        {
            "nombre":"sessiontoken",
            "nombreCampo":"SESSIONTOKEN",
            "tipo":orm.XPDSTRING,
            "tamano":36,
            },
        {
            "nombre":"activo",
            "nombreCampo":"ACTIVO",
            "tipo":orm.XPDINTEGER,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findall",
            "whereClause":["activo",] ,
            "orderBy":["username",]
            },
        {
            "nombre":"findById",
            "whereClause":["id",]
            },
        {
            "nombre":"findByUsername",
            "whereClause":["username",]
            },
        {
            "nombre":"findBySessiontoken",
            "whereClause":["sessiontoken",]
            },
        {
            "nombre":"findByEmail",
            "whereClause":["email",]
            }
        ]
    })

Roles = orm.Entidad()
Roles.setMetamodelo({
    "nombreTabla":"ROLES",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            "incremental":True,
            },
        {
            "nombre":"rolename",
            "nombreCampo":"ROLENAME",
            "tipo":orm.XPDSTRING,
            "tamano":32,
            },
        {
            "nombre":"descripcion",
            "nombreCampo":"DESCRIPCION",
            "tipo":orm.XPDSTRING,
            "tamano":128,
            },
        {
            "nombre":"activo",
            "nombreCampo":"ACTIVO",
            "tipo":orm.XPDINTEGER,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findall",
            "whereClause":["activo",] ,
            "orderBy":["username",]
            },
        {
            "nombre":"findByRolename",
            "whereClause":["rolename",]
            },
        ]
    })

UsuarioRoles = orm.Entidad()
UsuarioRoles.setMetamodelo({
    "nombreTabla":"USUARIOS_ROLES",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            "incremental":True,
            },
        {
            "nombre":"id_usuario",
            "nombreCampo":"ID_USUARIO",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"id_rol",
            "nombreCampo":"ID_ROL",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"activo",
            "nombreCampo":"ACTIVO",
            "tipo":orm.XPDINTEGER,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findByUser",
            "whereClause":["id_usuario","activo"] ,
            "orderBy":["id_rol",]
            },
        {
            "nombre":"findByRol",
            "whereClause":["id_rol","activo"] ,
            "orderBy":["id_usuario",]
            },
        {
            "nombre":"findByUsuarioRol",
            "whereClause":["id_usuario","id_rol"] ,
            "orderBy":["id_usuario",]
            },
        ]
    })

SolicitudesCambioClave = orm.Entidad()
SolicitudesCambioClave.setMetamodelo({
    "nombreTabla":"SOLICITUDES_CLAVE",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDSTRING,
            "tamano":36,
            "pk":True,
            },
        {
            "nombre":"id_usuario",
            "nombreCampo":"ID_USUARIO",
            "tipo":orm.XPDINTEGER,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findById",
            "whereClause":["id"] ,
            },
        ]
    })

def inicializar():
    entidades = [Usuarios, Roles, UsuarioRoles, SolicitudesCambioClave]
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

# sha256

def encriptar_sha256(cadena):
    """
    Encripta una cadena con el algoritmo SHA256.

    Parámetros:
    cadena (str): La cadena a encriptar.

    Retorno:
    str: La cadena encriptada en formato hexadecimal.
    """
    # Convertimos la cadena a bytes
    cadena_bytes = cadena.encode('utf-8')
    # Creamos un objeto hash SHA256
    sha256_hash = sha256()
    # Actualizamos el objeto hash con la cadena
    sha256_hash.update(cadena_bytes)
    # Obtenemos el resumen del hash en formato hexadecimal
    hash_hexadecimal = sha256_hash.hexdigest()
    return hash_hexadecimal

# Caso de Uso: iniciar Sesion

def loginUsuario(con, info):
    
    username = info['username']
    clave = info['clave']
    generar_token = info['generar_token'] if 'generar_token' in info.keys() else True

    usuarios = Usuarios.getNamedQuery(con, 'findByUsername', {'username':username})
    if len(usuarios) == 0 or usuarios[0]['activo'] == 0 :
        print('No se encuentra usuario {0}'.format( username ))
        return None
    
    if usuarios[0]['pwd'] != encriptar_sha256(clave) :
        return None
    
    if(generar_token):
        usuarios[0]['sessiontoken'] = str(uuid4())
        Usuarios.actualizar(con, usuarios[0])

    for campo in usuarios[0].keys():
        info[campo] = usuarios[0][campo]

    return usuarios[0]    
    
def servir_login():

    if request.method == "GET":
        return template('xpd_usr/login', username = '', lvl= '', mensaje ='')

    username = request.forms.get("username","").strip()
    password = request.forms.get("password","").strip()
    user = transaccionar( loginUsuario , {'username': username, 'clave': password })

    if not 'sessiontoken' in user.keys():
        return template('xpd_usr/login', username = username, lvl= 'danger', mensaje ='Usuario / Clave no válidos')

    request.session['sessiontoken'] = user['sessiontoken']
    return template('xpd_usr/redireccion', url ='/')

def getCurrentUser(request1):
    sessiontoken = request1.session.get('sessiontoken', None)
    if sessiontoken is None or sessiontoken == '':
        return None
    con = orm.Conexion(PATH_BDD)
    usuarios = Usuarios.getNamedQuery(con, 'findBySessiontoken', {'sessiontoken': sessiontoken})
    if len(usuarios) == 0:
        return None
    return usuarios[0]

# Caso de Uso: Logout
    
def removerSessionToken(con, sessiontoken):
    usuarios = Usuarios.getNamedQuery(con, 'findBySessiontoken', {'sessiontoken': sessiontoken})
    for usuario in usuarios:
        usuario['sessiontoken'] = ''
        Usuarios.actualizar(con, usuario)

def servir_logout():
    transaccionar( removerSessionToken, request.session['sessiontoken'] )
    request.session['sessiontoken'] = None
    return template('xpd_usr/login', username = '', lvl= 'success', mensaje ='Sesión finalizada exitosamente')

# Caso de uso Recuperar Clave

def getUserByEmail(email):
    con = orm.Conexion(PATH_BDD)
    usuarios = Usuarios.getNamedQuery(con, 'findByEmail', {'email':email})
    con.close()
    if len(usuarios) == 0:
        return None
    return usuarios[0]

def getSolicitudById(id_solicitud):
    con = orm.Conexion(PATH_BDD)
    solicitudes = SolicitudesCambioClave.getNamedQuery(con, 'findById', {'id':id_solicitud})
    con.close()
    if len(solicitudes) == 0:
        return None
    return solicitudes[0]

def servir_solicitar_recuperar_clave():
    if request.method == "GET":
        return template('xpd_usr/solicitar_recuperar_clave')
    
    # Si es POST
    
    email = request.forms.get("email","").strip()
    usuario = getUserByEmail(email)
    if usuario is None or usuario['activo'] == 0:
        return template('xpd_usr/mensaje', lvl ='danger', mensaje = 'Correo electronico no válido', href = '/' )
    
    solicitud = {'id': str(uuid4()),'id_usuario':usuario['id']}    
    transaccionar(SolicitudesCambioClave.insertar, solicitud)
    redirect( '/recuperar_clave/{0}'.format( solicitud['id'] ) )

def recuperar_clave(con, info ):    
    cambiar_clave(con, info)
    # Elimina registro de solicitud
    SolicitudesCambioClave.eliminar(con, {'id': info['id_solicitud'] })

def servir_recuperar_clave(id_solicitud):
    solicitud = getSolicitudById(id_solicitud)
    
    if solicitud is None:
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'Informacion no valida', href = '/' )
    
    if request.method == "GET":
        return template('xpd_usr/recuperar_clave', id_solicitud = id_solicitud, lvl= '', mensaje = '')   
    
    password = request.forms.get("password","").strip()
    password1 = request.forms.get("password1","").strip()
    if password != password1:
        return template('xpd_usr/recuperar_clave', id_solicitud = id_solicitud, lvl = 'danger', mensaje = 'Las claves no son iguales')
    
    transaccionar(recuperar_clave, {'id_solicitud': solicitud['id'], 'id_usuario': solicitud['id_usuario'], 'clave': password})
    
    return template('xpd_usr/mensaje', lvl='success', mensaje = 'Clave cambiada con Exito', href = '/' )

# Caso de uso: Cambiar Clave
    
def cambiar_clave(con, info):
    usuarios = []
    if 'id_usuario' in info.keys():
        usuarios = Usuarios.getNamedQuery(con, 'findById', { 'id' : info['id_usuario'] } )        
    elif 'username' in info.keys():
        usuarios = Usuarios.getNamedQuery(con, 'findByUsername', { 'username' : info['username'] } )
    if len(usuarios) == 0 :
        raise Exception('Usuario no existe')
    usuarios[0]['pwd'] = encriptar_sha256( info['clave'] )
    Usuarios.actualizar(con, usuarios[0])

def servir_cambiar_clave():
    usuario = getCurrentUser(request)
    if usuario is None :
        redirect('/login')
    
    if request.method == "GET":
        return template('xpd_usr/cambiar_clave', lvl= '', mensaje = '')

    password = request.forms.get("password","").strip()
    password1 = request.forms.get("password1","").strip()
    if password != password1:
        return template('xpd_usr/cambiar_clave', lvl = 'danger', mensaje = 'Las claves no son iguales')

    password_actual = request.forms.get("password_actual","").strip()
    usuario_cambiar = transaccionar(loginUsuario, {'username':usuario['username'], 'clave':password_actual, 'generar_token': False})

    if not 'sessiontoken' in usuario_cambiar.keys():
        return template('xpd_usr/cambiar_clave', lvl = 'danger', mensaje = 'Clave actual es incorrecta')

    transaccionar(cambiar_clave, {'username': usuario['username'], 'clave': password} )

    return template('xpd_usr/mensaje', lvl = 'success', mensaje = 'Clave cambiada con Exito', href = '/' )

# Caso de Uso: Registrar usuario

def registrar_usuario(con, usuario):
    # valida que el usuario no haya otros usuarios con el mismo username y el mismo email
    usuarios_repetidos = Usuarios.getNamedQuery(con, 'findByUsername', { 'username' : usuario['username'] } )
    if len(usuarios_repetidos) > 0 :
        raise Exception("Usuario {0} ya existe".format(usuario['username']))
    usuarios_repetidos = Usuarios.getNamedQuery(con, 'findByEmail', { 'email' : usuario['email'] } )
    if len(usuarios_repetidos) > 0 :
        raise Exception("El correo {0} ya se encuentra ocupado por otro usuario".format(usuario['email']))
    # forma el nuevo objeto usuario
    usuario_persistir = {'username': usuario['username'], 'pwd': encriptar_sha256(usuario['password']), 'email':usuario['email'], 'sessiontoken': '','activo': 1 }
    print(repr(usuario_persistir))
    Usuarios.insertar(con, usuario_persistir)
    usuario['id'] = usuario_persistir['id'] 
    return usuario

def servir_registrar_usuario():
    campos = ['username','password','password1','email']
    if request.method == 'GET':
        return template('xpd_usr/registrar_usuario', usuario = {x : '' for x in campos} , lvl = '', mensaje = '')
    
    usuario = { x : request.forms.get(x,'').strip() for x in ['username','password','password1','email'] }

    # valida que ninguno de los campos sea Nullo
    if len([x for x in usuario.values() if x == '' ]) > 0 :
        return template('xpd_usr/registrar_usuario', usuario = usuario , lvl = 'danger', mensaje = 'No se ha ingresado toda la información requerida')
    if usuario['password'] != usuario['password1'] :
        return template('xpd_usr/registrar_usuario', usuario = usuario , lvl = 'danger', mensaje = 'Las claves no coinciden')
    
    # Realiza registro del usuario
    usuario['pwd'] = usuario['password']
    
    try:
        transaccionar( registrar_usuario, usuario)
        return template('xpd_usr/mensaje', lvl ="success", mensaje = 'Usuario creado exitosamente', href = '/login' )
    except Exception as ex:
        return template('xpd_usr/registrar_usuario', usuario = {x : '' for x in campos}, lvl = 'danger', mensaje = str(ex) )

# Agregar Mapeos para Bottle
    
def rutearModulo( app : Bottle, ruta_base : str ):
    # encapsula Session Middleware
    RUTA_BASE = ruta_base

    app.route( '/login' , method = ['GET','POST'])(servir_login)
    app.route( '/logout' )(servir_logout)
    app.route( '/solicitar_recuperar_clave' , method = ['GET','POST'])(servir_solicitar_recuperar_clave)
    app.route( '/recuperar_clave/<id_solicitud>' , method = ['GET','POST'])(servir_recuperar_clave)
    app.route( '/cambiar_clave' , method = ['GET','POST'])(servir_cambiar_clave)
    app.route( '/registrar_usuario' , method = ['GET','POST'])(servir_registrar_usuario)
    