import xpd_orm as orm
from os.path import abspath , dirname, join, exists
from os import makedirs
from os import remove as remove_file

from bottle import run, debug, route, error, static_file, template, request, response, redirect
from bottle import Bottle

import xpd_usr

PATH_BDD = dirname(abspath(__file__)) + "/data/xpd_asistente.db"
CONFIG = {'rutas': []}

Modelos = orm.Entidad()
Modelos.setMetamodelo({
    'nombreTabla' : 'MODELO',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'nombre', 'nombreCampo':'NOMBRE', 'tipo':orm.XPDSTRING, 'tamano':32, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'contenido', 'nombreCampo':'CONTENIDO', 'tipo':orm.XPDLONGBINARY, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'mesh_body', 'nombreCampo':'MESH_BODY', 'tipo':orm.XPDSTRING, 'tamano':48, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'armature', 'nombreCampo':'ARMATURE', 'tipo':orm.XPDSTRING, 'tamano':48, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'orden', 'nombreCampo':'ORDEN', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'camposWhere':['id'], },
        { 'nombre':'findAll', 'camposOrderBy':['orden'], },
        ]
    })

Avatars = orm.Entidad()
Avatars.setMetamodelo({
    'nombreTabla' : 'AVATAR',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'nombre', 'nombreCampo':'NOMBRE', 'tipo':orm.XPDSTRING, 'tamano':32, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'foto', 'nombreCampo':'FOTO', 'tipo':orm.XPDLONGBINARY, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_modelo', 'nombreCampo':'ID_MODELO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_pose', 'nombreCampo':'ID_POSE', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'orden', 'nombreCampo':'ORDEN', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_user', 'nombreCampo':'ID_USER', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'camposWhere':['id'], },
        { 'nombre':'findByUser', 'camposWhere':['id_user'], 'camposOrderBy':['orden'], },
        ]
    })

Meshs = orm.Entidad()
Meshs.setMetamodelo({
    'nombreTabla' : 'MESH',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'nombre', 'nombreCampo':'NOMBRE', 'tipo':orm.XPDSTRING, 'tamano':48, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'es_default', 'nombreCampo':'ES_DEFAULT', 'tipo':orm.XPDBOOLEAN, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'orden', 'nombreCampo':'ORDEN', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_modelo', 'nombreCampo':'ID_MODELO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'camposWhere':['id'], },
        { 'nombre':'findByModelo', 'camposWhere':['id_modelo'], 'camposOrderBy':['orden'], },
        ]
    })

VariacionFacials = orm.Entidad()
VariacionFacials.setMetamodelo({
    'nombreTabla' : 'VARIACION_FACIAL',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'nombre', 'nombreCampo':'NOMBRE', 'tipo':orm.XPDSTRING, 'tamano':64, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'orden', 'nombreCampo':'ORDEN', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_modelo', 'nombreCampo':'ID_MODELO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'camposWhere':['id'], },
        { 'nombre':'findByModelo', 'camposWhere':['id_modelo'], 'camposOrderBy':['orden'], },
        ]
    })

Colors = orm.Entidad()
Colors.setMetamodelo({
    'nombreTabla' : 'COLOR',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'nombre', 'nombreCampo':'NOMBRE', 'tipo':orm.XPDSTRING, 'tamano':32, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'label', 'nombreCampo':'LABEL', 'tipo':orm.XPDSTRING, 'tamano':48, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'default_color', 'nombreCampo':'DEFAULT_COLOR', 'tipo':orm.XPDSTRING, 'tamano':7, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_modelo', 'nombreCampo':'ID_MODELO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'camposWhere':['id'], },
        { 'nombre':'findByModelo', 'camposWhere':['id_modelo'], },
        ]
    })

Poses = orm.Entidad()
Poses.setMetamodelo({
    'nombreTabla' : 'POSE',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'nombre', 'nombreCampo':'NOMBRE', 'tipo':orm.XPDSTRING, 'tamano':32, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'contenido', 'nombreCampo':'CONTENIDO', 'tipo':orm.XPDLONGBINARY, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'nombre_pose', 'nombreCampo':'NOMBRE_POSE', 'tipo':orm.XPDSTRING, 'tamano':48, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'orden', 'nombreCampo':'ORDEN', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_modelo', 'nombreCampo':'ID_MODELO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'camposWhere':['id'], },
        { 'nombre':'findByModelo', 'camposWhere':['id_modelo'], 'camposOrderBy':['orden'], },
        ]
    })

VariacionAvatars = orm.Entidad()
VariacionAvatars.setMetamodelo({
    'nombreTabla' : 'VARIACION_AVATAR',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'nombre', 'nombreCampo':'NOMBRE', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'valor', 'nombreCampo':'VALOR', 'tipo':orm.XPDREAL, 'tamano': 4, 'precision': 2, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_avatar', 'nombreCampo':'ID_AVATAR', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'camposWhere':['id'], },
        { 'nombre':'findByAvatar', 'camposWhere':['id_avatar'], },
        ]
    })

MeshAvatars = orm.Entidad()
MeshAvatars.setMetamodelo({
    'nombreTabla' : 'MESH_AVATAR',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'nombre', 'nombreCampo':'NOMBRE', 'tipo':orm.XPDSTRING, 'tamano':48, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'es_visible', 'nombreCampo':'ES_VISIBLE', 'tipo':orm.XPDBOOLEAN, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_avatar', 'nombreCampo':'ID_AVATAR', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'camposWhere':['id'], },
        { 'nombre':'findByAvatar', 'camposWhere':['id_avatar'], },
        ]
    })

ColorAvatars = orm.Entidad()
ColorAvatars.setMetamodelo({
    'nombreTabla' : 'COLOR_AVATAR',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'nombre', 'nombreCampo':'NOMBRE', 'tipo':orm.XPDSTRING, 'tamano':48, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'color', 'nombreCampo':'COLOR', 'tipo':orm.XPDSTRING, 'tamano':7, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_avatar', 'nombreCampo':'ID_AVATAR', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'camposWhere':['id'], },
        { 'nombre':'findByAvatar', 'camposWhere':['id_avatar'], },
        ]
    })


def inicializar():
    entidades = [Modelos, Avatars, Meshs, VariacionFacials, Colors, Poses, VariacionAvatars, MeshAvatars, ColorAvatars]
    con = orm.Conexion(PATH_BDD)
    try:
        for entidad in entidades:
            entidad.crearTabla(con)
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
    

def avatar_getowner(conexion, id_avatar):
    objeto = Avatars.getNamedQuery(conexion, 'findById', {'id': id_avatar})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, objeto['id_user'])

def variacionavatar_getowner(conexion, id_variacionavatar):
    objeto = VariacionAvatars.getNamedQuery(conexion, 'findById', {'id': id_variacionavatar})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, avatar_getowner(conexion, objeto['id_avatar'])[1] )

def meshavatar_getowner(conexion, id_meshavatar):
    objeto = MeshAvatars.getNamedQuery(conexion, 'findById', {'id': id_meshavatar})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, avatar_getowner(conexion, objeto['id_avatar'])[1] )

def coloravatar_getowner(conexion, id_coloravatar):
    objeto = ColorAvatars.getNamedQuery(conexion, 'findById', {'id': id_coloravatar})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, avatar_getowner(conexion, objeto['id_avatar'])[1] )

def servir_download_modelo_contenido(id, extension):    

    con = orm.Conexion(PATH_BDD)
    modelo = Modelos.getNamedQuery(con, 'findById', { 'id' : id } )
    con.close()
    if len(modelo) == 0:
        error(404, "No existe")
    modelo = modelo[0]
    
    contenido = modelo['contenido']
    if len(contenido) == 0:
        error(404, "No se dispone de contenido")
    response.add_header('Content-Type',"application/" + extension)
    return contenido

CONFIG['rutas'].append({'ruta':'/modelos/<id>/contenido.<extension>', 'metodos':['GET'], 'funcion': servir_download_modelo_contenido })

def servir_page_insertar_modelo():

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )

    modelo = Modelos.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_asistente/editar_Modelo", objeto = modelo, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_asistente/modelos")
    # A partir de este punto se asume POST
    mensajes_error = []

    modelo["nombre"] = request.forms.get( "nombre", "").strip()
        
    if len(modelo["nombre"]) == 0:
        mensajes_error.append("nombre es requerido")

    if len(modelo["nombre"]) > 32:
        mensajes_error.append("El tamaño de nombre excede el permitido")

    file_contenido = request.files.get("contenido")
    filename_contenido = file_contenido.filename
    temppath_contenido = join( dirname(abspath(__file__)), "upload", filename_contenido )
    if not exists( dirname(temppath_contenido) ):
        makedirs( dirname(temppath_contenido) )
    file_contenido.save(temppath_contenido)
    with open( temppath_contenido , 'rb' ) as stream_contenido:
        modelo["contenido"] = stream_contenido.read()
    remove_file(temppath_contenido)

    modelo["mesh_body"] = request.forms.get( "mesh_body", "").strip()
        
    if len(modelo["mesh_body"]) > 48:
        mensajes_error.append("El tamaño de mesh_body excede el permitido")

    modelo["armature"] = request.forms.get( "armature", "").strip()
        
    if len(modelo["armature"]) > 48:
        mensajes_error.append("El tamaño de armature excede el permitido")

    if len(mensajes_error) > 0:
        return template("xpd_asistente/editar_Modelo", objeto = modelo, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_asistente/modelos" )    
    try:
        transaccionar(Modelos.insertar, modelo)
    except:
        return template("xpd_asistente/editar_Modelo", objeto = modelo, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_asistente/modelos" )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_asistente/modelos/{{modelo['id']}}")

CONFIG['rutas'].append({'ruta':'/modelos/nuevo', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_modelo })

def servir_page_get_modelo_lista():
    conexion = orm.Conexion(PATH_BDD)

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )    
    conexion = orm.Conexion(PATH_BDD)

    lista = Modelos.getNamedQuery(conexion, 'findAll', {})
    conexion.close()

    return template("xpd_asistente/listar_Modelo", lista = lista, usuario = usuario)
    
CONFIG['rutas'].append({'ruta':'/modelos', 'metodos':['GET'], 'funcion': servir_page_get_modelo_lista })

def servir_page_get_modelo_byid(id_modelo):    

    conexion = orm.Conexion(PATH_BDD)
    objeto = Modelos.getNamedQuery(conexion, 'findById', {'id': id_modelo})
    if len(objeto) == 0:
        conexion.close()
        error( 404, "El recurso solicitado no existe" )
    objeto = objeto[0]
    
    meshs = Meshs.getNamedQuery( conexion, "findByModelo", {'id_modelo':objeto['id_modelo']} )

    variacionfacials = VariacionFacials.getNamedQuery( conexion, "findByModelo", {'id_modelo':objeto['id_modelo']} )

    colors = Colors.getNamedQuery( conexion, "findByModelo", {'id_modelo':objeto['id_modelo']} )

    poses = Poses.getNamedQuery( conexion, "findByModelo", {'id_modelo':objeto['id_modelo']} )

    conexion.close()
    return template("xpd_asistente/show_Modelo", objeto = objeto , meshs = meshs, variacionfacials = variacionfacials, colors = colors, poses = poses)

CONFIG['rutas'].append({'ruta':'/modelos/<id_modelo>', 'metodos':['GET'], 'funcion': servir_page_get_modelo_byid })

def servir_download_avatar_foto(id, extension):    

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )
    con = orm.Conexion(PATH_BDD)
    avatar, id_usuario_owner = avatar_getowner(con, id)
    con.close()
    if avatar is None or usuario['id'] != id_usuario_owner:
        error( 403, "Acceso no autorizado")
    
    contenido = avatar['foto']
    if len(contenido) == 0:
        error(404, "No se dispone de contenido")
    response.add_header('Content-Type',"application/" + extension)
    return contenido

CONFIG['rutas'].append({'ruta':'/avatars/<id>/foto.<extension>', 'metodos':['GET'], 'funcion': servir_download_avatar_foto })

def servir_page_insertar_avatar():

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )

    avatar = Avatars.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_asistente/editar_Avatar", objeto = avatar, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_asistente/avatars")
    # A partir de este punto se asume POST
    mensajes_error = []

    avatar["nombre"] = request.forms.get( "nombre", "").strip()
        
    if len(avatar["nombre"]) == 0:
        mensajes_error.append("nombre es requerido")

    if len(avatar["nombre"]) > 32:
        mensajes_error.append("El tamaño de nombre excede el permitido")

    file_foto = request.files.get("foto")
    filename_foto = file_foto.filename
    temppath_foto = join( dirname(abspath(__file__)), "upload", filename_foto )
    if not exists( dirname(temppath_foto) ):
        makedirs( dirname(temppath_foto) )
    file_foto.save(temppath_foto)
    with open( temppath_foto , 'rb' ) as stream_foto:
        avatar["foto"] = stream_foto.read()
    remove_file(temppath_foto)

    avatar["id_modelo"] = request.forms.get( "id_modelo", "").strip()
        
    if len(avatar["id_modelo"]) == 0:
        mensajes_error.append("id_modelo es requerido")

    try:
        avatar["id_modelo"] = int( avatar["id_modelo"] )
    except:
        mensajes_error.append("El valor de id_modelo no es válido")

    avatar["id_pose"] = request.forms.get( "id_pose", "").strip()
        
    try:
        avatar["id_pose"] = int( avatar["id_pose"] )
    except:
        mensajes_error.append("El valor de id_pose no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_asistente/editar_Avatar", objeto = avatar, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_asistente/avatars" )    
    try:
        transaccionar(Avatars.insertar, avatar)
    except:
        return template("xpd_asistente/editar_Avatar", objeto = avatar, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_asistente/avatars" )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_asistente/avatars/{{avatar['id']}}")

CONFIG['rutas'].append({'ruta':'/avatars/nuevo', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_avatar })

def servir_page_get_avatar_lista():
    conexion = orm.Conexion(PATH_BDD)

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )    
    conexion = orm.Conexion(PATH_BDD)

    lista = Avatars.getNamedQuery(conexion, 'findByUser', {'id_user':usuario['id']})

    conexion.close()

    return template("xpd_asistente/listar_Avatar", lista = lista, usuario = usuario)
    
CONFIG['rutas'].append({'ruta':'/avatars', 'metodos':['GET'], 'funcion': servir_page_get_avatar_lista })

def servir_page_get_avatar_byid(id_avatar):    

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = avatar_getowner(conexion, id_avatar)
    if objeto is None:
        conexion.close()
        error( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        error( 403, "Acceso no autorizado") 
    
    variacionavatars = VariacionAvatars.getNamedQuery( conexion, "findByAvatar", {'id_avatar':objeto['id_avatar']} )

    meshavatars = MeshAvatars.getNamedQuery( conexion, "findByAvatar", {'id_avatar':objeto['id_avatar']} )

    coloravatars = ColorAvatars.getNamedQuery( conexion, "findByAvatar", {'id_avatar':objeto['id_avatar']} )

    conexion.close()
    return template("xpd_asistente/show_avatar", avatar = objeto, usuario = usuario , variacionavatars = variacionavatars, meshavatars = meshavatars, coloravatars = coloravatars)

CONFIG['rutas'].append({'ruta':'/avatars/<id_avatar>', 'metodos':['GET'], 'funcion': servir_page_get_avatar_byid })

def servir_page_insertar_mesh(id_modelo):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )

    mesh = Meshs.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_asistente/editar_Mesh", objeto = mesh, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_asistente/modelos/{{objeto['id_modelo']}}")
    # A partir de este punto se asume POST
    mensajes_error = []

    mesh['id_modelo'] = id_modelo

    mesh["nombre"] = request.forms.get( "nombre", "").strip()
        
    if len(mesh["nombre"]) == 0:
        mensajes_error.append("nombre es requerido")

    if len(mesh["nombre"]) > 48:
        mensajes_error.append("El tamaño de nombre excede el permitido")

    mesh["es_default"] = request.forms.get( "es_default", "").strip()
        
    mesh["es_default"] = mesh["es_default"] == "1"

    if len(mensajes_error) > 0:
        return template("xpd_asistente/editar_Mesh", objeto = mesh, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_asistente/modelos/{{objeto['id_modelo']}}" )    
    try:
        transaccionar(Meshs.insertar, mesh)
    except:
        return template("xpd_asistente/editar_Mesh", objeto = mesh, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_asistente/modelos/{{objeto['id_modelo']}}" )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_asistente/meshs/{{mesh['id']}}")

CONFIG['rutas'].append({'ruta':'/modelos/<id_modelo>/nuevomesh', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_mesh })

def servir_page_get_mesh_byid(id_mesh):    

    conexion = orm.Conexion(PATH_BDD)
    objeto = Meshs.getNamedQuery(conexion, 'findById', {'id': id_mesh})
    if len(objeto) == 0:
        conexion.close()
        error( 404, "El recurso solicitado no existe" )
    objeto = objeto[0]
    
    conexion.close()
    return template("xpd_asistente/show_Mesh", objeto = objeto )

CONFIG['rutas'].append({'ruta':'/meshs/<id_mesh>', 'metodos':['GET'], 'funcion': servir_page_get_mesh_byid })

def servir_page_insertar_variacionfacial(id_modelo):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )

    variacionfacial = VariacionFacials.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_asistente/editar_VariacionFacial", objeto = variacionfacial, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_asistente/modelos/{{objeto['id_modelo']}}")
    # A partir de este punto se asume POST
    mensajes_error = []

    variacionfacial['id_modelo'] = id_modelo

    variacionfacial["nombre"] = request.forms.get( "nombre", "").strip()
        
    if len(variacionfacial["nombre"]) == 0:
        mensajes_error.append("nombre es requerido")

    if len(variacionfacial["nombre"]) > 64:
        mensajes_error.append("El tamaño de nombre excede el permitido")

    if len(mensajes_error) > 0:
        return template("xpd_asistente/editar_VariacionFacial", objeto = variacionfacial, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_asistente/modelos/{{objeto['id_modelo']}}" )    
    try:
        transaccionar(VariacionFacials.insertar, variacionfacial)
    except:
        return template("xpd_asistente/editar_VariacionFacial", objeto = variacionfacial, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_asistente/modelos/{{objeto['id_modelo']}}" )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_asistente/variacionfacials/{{variacionfacial['id']}}")

CONFIG['rutas'].append({'ruta':'/modelos/<id_modelo>/nuevovariacionfacial', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_variacionfacial })

def servir_page_get_variacionfacial_byid(id_variacionfacial):    

    conexion = orm.Conexion(PATH_BDD)
    objeto = VariacionFacials.getNamedQuery(conexion, 'findById', {'id': id_variacionfacial})
    if len(objeto) == 0:
        conexion.close()
        error( 404, "El recurso solicitado no existe" )
    objeto = objeto[0]
    
    conexion.close()
    return template("xpd_asistente/show_VariacionFacial", objeto = objeto )

CONFIG['rutas'].append({'ruta':'/variacionfacials/<id_variacionfacial>', 'metodos':['GET'], 'funcion': servir_page_get_variacionfacial_byid })

def servir_page_insertar_color(id_modelo):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )

    color = Colors.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_asistente/editar_Color", objeto = color, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_asistente/modelos/{{objeto['id_modelo']}}")
    # A partir de este punto se asume POST
    mensajes_error = []

    color['id_modelo'] = id_modelo

    color["nombre"] = request.forms.get( "nombre", "").strip()
        
    if len(color["nombre"]) == 0:
        mensajes_error.append("nombre es requerido")

    if len(color["nombre"]) > 32:
        mensajes_error.append("El tamaño de nombre excede el permitido")

    color["label"] = request.forms.get( "label", "").strip()
        
    if len(color["label"]) == 0:
        mensajes_error.append("label es requerido")

    if len(color["label"]) > 48:
        mensajes_error.append("El tamaño de label excede el permitido")

    color["default_color"] = request.forms.get( "default_color", "").strip()
        
    if len(color["default_color"]) == 0:
        mensajes_error.append("default_color es requerido")

    if len(color["default_color"]) > 7:
        mensajes_error.append("El tamaño de default_color excede el permitido")

    if len(mensajes_error) > 0:
        return template("xpd_asistente/editar_Color", objeto = color, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_asistente/modelos/{{objeto['id_modelo']}}" )    
    try:
        transaccionar(Colors.insertar, color)
    except:
        return template("xpd_asistente/editar_Color", objeto = color, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_asistente/modelos/{{objeto['id_modelo']}}" )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_asistente/colors/{{color['id']}}")

CONFIG['rutas'].append({'ruta':'/modelos/<id_modelo>/nuevocolor', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_color })

def servir_page_get_color_byid(id_color):    

    conexion = orm.Conexion(PATH_BDD)
    objeto = Colors.getNamedQuery(conexion, 'findById', {'id': id_color})
    if len(objeto) == 0:
        conexion.close()
        error( 404, "El recurso solicitado no existe" )
    objeto = objeto[0]
    
    conexion.close()
    return template("xpd_asistente/show_Color", objeto = objeto )

CONFIG['rutas'].append({'ruta':'/colors/<id_color>', 'metodos':['GET'], 'funcion': servir_page_get_color_byid })

def servir_download_pose_contenido(id, extension):    

    con = orm.Conexion(PATH_BDD)
    pose = Poses.getNamedQuery(con, 'findById', { 'id' : id } )
    con.close()
    if len(pose) == 0:
        error(404, "No existe")
    pose = pose[0]
    
    contenido = pose['contenido']
    if len(contenido) == 0:
        error(404, "No se dispone de contenido")
    response.add_header('Content-Type',"application/" + extension)
    return contenido

CONFIG['rutas'].append({'ruta':'/poses/<id>/contenido.<extension>', 'metodos':['GET'], 'funcion': servir_download_pose_contenido })

def servir_page_insertar_pose(id_modelo):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )

    pose = Poses.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_asistente/editar_Pose", objeto = pose, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_asistente/modelos/{{objeto['id_modelo']}}")
    # A partir de este punto se asume POST
    mensajes_error = []

    pose['id_modelo'] = id_modelo

    pose["nombre"] = request.forms.get( "nombre", "").strip()
        
    if len(pose["nombre"]) == 0:
        mensajes_error.append("nombre es requerido")

    if len(pose["nombre"]) > 32:
        mensajes_error.append("El tamaño de nombre excede el permitido")

    file_contenido = request.files.get("contenido")
    filename_contenido = file_contenido.filename
    temppath_contenido = join( dirname(abspath(__file__)), "upload", filename_contenido )
    if not exists( dirname(temppath_contenido) ):
        makedirs( dirname(temppath_contenido) )
    file_contenido.save(temppath_contenido)
    with open( temppath_contenido , 'rb' ) as stream_contenido:
        pose["contenido"] = stream_contenido.read()
    remove_file(temppath_contenido)

    pose["nombre_pose"] = request.forms.get( "nombre_pose", "").strip()
        
    if len(pose["nombre_pose"]) > 48:
        mensajes_error.append("El tamaño de nombre_pose excede el permitido")

    if len(mensajes_error) > 0:
        return template("xpd_asistente/editar_Pose", objeto = pose, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_asistente/modelos/{{objeto['id_modelo']}}" )    
    try:
        transaccionar(Poses.insertar, pose)
    except:
        return template("xpd_asistente/editar_Pose", objeto = pose, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_asistente/modelos/{{objeto['id_modelo']}}" )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_asistente/poses/{{pose['id']}}")

CONFIG['rutas'].append({'ruta':'/modelos/<id_modelo>/nuevopose', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_pose })

def servir_page_get_pose_byid(id_pose):    

    conexion = orm.Conexion(PATH_BDD)
    objeto = Poses.getNamedQuery(conexion, 'findById', {'id': id_pose})
    if len(objeto) == 0:
        conexion.close()
        error( 404, "El recurso solicitado no existe" )
    objeto = objeto[0]
    
    conexion.close()
    return template("xpd_asistente/show_Pose", objeto = objeto )

CONFIG['rutas'].append({'ruta':'/poses/<id_pose>', 'metodos':['GET'], 'funcion': servir_page_get_pose_byid })

def servir_page_insertar_variacionavatar(id_avatar):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    avatar, id_usuario_owner = avatar_getowner( conexion , id_avatar)
    conexion.close()
    if avatar is None or usuario['id'] != id_usuario_owner:
        error( 403, "Acceso no autorizado" )

    variacionavatar = VariacionAvatars.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_asistente/editar_VariacionAvatar", objeto = variacionavatar, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_asistente/avatars/{{objeto['id_avatar']}}")
    # A partir de este punto se asume POST
    mensajes_error = []

    variacionavatar['id_avatar'] = id_avatar

    variacionavatar["nombre"] = request.forms.get( "nombre", "").strip()
        
    if len(variacionavatar["nombre"]) == 0:
        mensajes_error.append("nombre es requerido")

    try:
        variacionavatar["nombre"] = int( variacionavatar["nombre"] )
    except:
        mensajes_error.append("El valor de nombre no es válido")

    variacionavatar["valor"] = request.forms.get( "valor", "").strip()
        
    if len(variacionavatar["valor"]) == 0:
        mensajes_error.append("valor es requerido")

    try:
        variacionavatar["valor"] = float( variacionavatar["valor"] )
    except:
        mensajes_error.append("El valor de valor no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_asistente/editar_VariacionAvatar", objeto = variacionavatar, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_asistente/avatars/{{objeto['id_avatar']}}" )    
    try:
        transaccionar(VariacionAvatars.insertar, variacionavatar)
    except:
        return template("xpd_asistente/editar_VariacionAvatar", objeto = variacionavatar, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_asistente/avatars/{{objeto['id_avatar']}}" )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_asistente/variacionavatars/{{variacionavatar['id']}}")

CONFIG['rutas'].append({'ruta':'/avatars/<id_avatar>/nuevovariacionavatar', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_variacionavatar })

def servir_page_get_variacionavatar_byid(id_variacionavatar):    

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = variacionavatar_getowner(conexion, id_variacionavatar)
    if objeto is None:
        conexion.close()
        error( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        error( 403, "Acceso no autorizado") 
    
    conexion.close()
    return template("xpd_asistente/show_variacionavatar", variacionavatar = objeto, usuario = usuario )

CONFIG['rutas'].append({'ruta':'/variacionavatars/<id_variacionavatar>', 'metodos':['GET'], 'funcion': servir_page_get_variacionavatar_byid })

def servir_page_insertar_meshavatar(id_avatar):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    avatar, id_usuario_owner = avatar_getowner( conexion , id_avatar)
    conexion.close()
    if avatar is None or usuario['id'] != id_usuario_owner:
        error( 403, "Acceso no autorizado" )

    meshavatar = MeshAvatars.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_asistente/editar_MeshAvatar", objeto = meshavatar, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_asistente/avatars/{{objeto['id_avatar']}}")
    # A partir de este punto se asume POST
    mensajes_error = []

    meshavatar['id_avatar'] = id_avatar

    meshavatar["nombre"] = request.forms.get( "nombre", "").strip()
        
    if len(meshavatar["nombre"]) == 0:
        mensajes_error.append("nombre es requerido")

    if len(meshavatar["nombre"]) > 48:
        mensajes_error.append("El tamaño de nombre excede el permitido")

    meshavatar["es_visible"] = request.forms.get( "es_visible", "").strip()
        
    meshavatar["es_visible"] = meshavatar["es_visible"] == "1"

    if len(mensajes_error) > 0:
        return template("xpd_asistente/editar_MeshAvatar", objeto = meshavatar, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_asistente/avatars/{{objeto['id_avatar']}}" )    
    try:
        transaccionar(MeshAvatars.insertar, meshavatar)
    except:
        return template("xpd_asistente/editar_MeshAvatar", objeto = meshavatar, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_asistente/avatars/{{objeto['id_avatar']}}" )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_asistente/meshavatars/{{meshavatar['id']}}")

CONFIG['rutas'].append({'ruta':'/avatars/<id_avatar>/nuevomeshavatar', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_meshavatar })

def servir_page_get_meshavatar_byid(id_meshavatar):    

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = meshavatar_getowner(conexion, id_meshavatar)
    if objeto is None:
        conexion.close()
        error( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        error( 403, "Acceso no autorizado") 
    
    conexion.close()
    return template("xpd_asistente/show_meshavatar", meshavatar = objeto, usuario = usuario )

CONFIG['rutas'].append({'ruta':'/meshavatars/<id_meshavatar>', 'metodos':['GET'], 'funcion': servir_page_get_meshavatar_byid })

def servir_page_insertar_coloravatar(id_avatar):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    avatar, id_usuario_owner = avatar_getowner( conexion , id_avatar)
    conexion.close()
    if avatar is None or usuario['id'] != id_usuario_owner:
        error( 403, "Acceso no autorizado" )

    coloravatar = ColorAvatars.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_asistente/editar_ColorAvatar", objeto = coloravatar, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_asistente/avatars/{{objeto['id_avatar']}}")
    # A partir de este punto se asume POST
    mensajes_error = []

    coloravatar['id_avatar'] = id_avatar

    coloravatar["nombre"] = request.forms.get( "nombre", "").strip()
        
    if len(coloravatar["nombre"]) == 0:
        mensajes_error.append("nombre es requerido")

    if len(coloravatar["nombre"]) > 48:
        mensajes_error.append("El tamaño de nombre excede el permitido")

    coloravatar["color"] = request.forms.get( "color", "").strip()
        
    if len(coloravatar["color"]) == 0:
        mensajes_error.append("color es requerido")

    if len(coloravatar["color"]) > 7:
        mensajes_error.append("El tamaño de color excede el permitido")

    if len(mensajes_error) > 0:
        return template("xpd_asistente/editar_ColorAvatar", objeto = coloravatar, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_asistente/avatars/{{objeto['id_avatar']}}" )    
    try:
        transaccionar(ColorAvatars.insertar, coloravatar)
    except:
        return template("xpd_asistente/editar_ColorAvatar", objeto = coloravatar, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_asistente/avatars/{{objeto['id_avatar']}}" )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_asistente/coloravatars/{{coloravatar['id']}}")

CONFIG['rutas'].append({'ruta':'/avatars/<id_avatar>/nuevocoloravatar', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_coloravatar })

def servir_page_get_coloravatar_byid(id_coloravatar):    

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = coloravatar_getowner(conexion, id_coloravatar)
    if objeto is None:
        conexion.close()
        error( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        error( 403, "Acceso no autorizado") 
    
    conexion.close()
    return template("xpd_asistente/show_coloravatar", coloravatar = objeto, usuario = usuario )

CONFIG['rutas'].append({'ruta':'/coloravatars/<id_coloravatar>', 'metodos':['GET'], 'funcion': servir_page_get_coloravatar_byid })

def servir_page_main():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )

    redirect('/xpd_asistente/avatars')    

CONFIG['rutas'].append({'ruta':'/main', 'metodos':['GET'], 'funcion': servir_page_main })

def servir_page_admin_main():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error( 401, "Acceso no autorizado" )
    if 'Administrador' not in usuario['roles']:
        error(403,"Acceso Denegado")  

    redirect('/xpd_asistente/modelos')    

CONFIG['rutas'].append({'ruta':'/admin', 'metodos':['GET'], 'funcion': servir_page_admin_main })

def rutearModulo( app : Bottle, ruta_base : str ):
    CONFIG['RUTA_BASE'] = ruta_base
    for item in CONFIG['rutas']:
        app.route( ruta_base + item['ruta'], method = item['metodos'] )( item['funcion'])
