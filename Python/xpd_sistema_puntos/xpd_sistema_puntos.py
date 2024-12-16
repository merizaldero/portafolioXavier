import xpd_orm as orm
from os.path import abspath , dirname, join, exists
from os import makedirs
from os import remove as remove_file

from bottle import run, debug, route, abort, static_file, template, request, response, redirect
from bottle import Bottle
import datetime

import xpd_usr

PATH_BDD = dirname(abspath(__file__)) + "/data/xpd_sistema_puntos.db"
CONFIG = {'rutas': []}

import datetime

def fecha_js_to_iso(fecha_hora):
    try:
        fecha_hora_obj = datetime.datetime.strptime(fecha_hora, '%m/%d/%Y %I:%M %p')
        fecha_hora_iso = fecha_hora_obj.strftime('%Y-%m-%d %H:%M')
        return fecha_hora_iso
    except ValueError:
        raise ValueError("Formato de fecha y hora inválido. Debe ser mm/dd/yyyy HH:MM AM/PM")

def fecha_iso_to_js(fecha_hora):
    try:
        fecha_hora_obj = datetime.datetime.strptime(fecha_hora, '%Y-%m-%d %H:%M')
        fecha_hora_js = fecha_hora_obj.strftime('%m/%d/%Y %I:%M %p')
        return fecha_hora_js
    except:
        return ""


Evaluados = orm.Entidad()
Evaluados.setMetamodelo({
    'nombreTabla' : 'EVALUADO',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'nombre', 'nombreCampo':'NOMBRE', 'tipo':orm.XPDSTRING, 'tamano':16, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_icono', 'nombreCampo':'ID_ICONO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'saldo', 'nombreCampo':'SALDO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'orden', 'nombreCampo':'ORDEN', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_user', 'nombreCampo':'ID_USER', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'fkIcono', 'whereClause':['id_icono'], },
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByUser', 'whereClause':['id_user'], 'orderBy':['orden'], },
        ]
    })

Premios = orm.Entidad()
Premios.setMetamodelo({
    'nombreTabla' : 'PREMIO',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'id_icono', 'nombreCampo':'ID_ICONO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'descripcion', 'nombreCampo':'DESCRIPCION', 'tipo':orm.XPDSTRING, 'tamano':256, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'puntos_requeridos', 'nombreCampo':'PUNTOS_REQUERIDOS', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'puntos_logro', 'nombreCampo':'PUNTOS_LOGRO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_user', 'nombreCampo':'ID_USER', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'fkIcono', 'whereClause':['id_icono'], },
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByUser', 'whereClause':['id_user'], },
        ]
    })

PlantillaTransaccions = orm.Entidad()
PlantillaTransaccions.setMetamodelo({
    'nombreTabla' : 'PLANTILLA_TRANSACCION',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'descripcion', 'nombreCampo':'DESCRIPCION', 'tipo':orm.XPDSTRING, 'tamano':256, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'puntos', 'nombreCampo':'PUNTOS', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findAll', },
        ]
    })

Iconos = orm.Entidad()
Iconos.setMetamodelo({
    'nombreTabla' : 'ICONO',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'icono', 'nombreCampo':'ICONO', 'tipo':orm.XPDSTRING, 'tamano':4, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'orden', 'nombreCampo':'ORDEN', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findAll', 'orderBy':['orden'], },
        ]
    })

Transaccions = orm.Entidad()
Transaccions.setMetamodelo({
    'nombreTabla' : 'TRANSACCION',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'fecha', 'nombreCampo':'FECHA', 'tipo':orm.XPDDATE, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'id_icono', 'nombreCampo':'ID_ICONO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'descripcion', 'nombreCampo':'DESCRIPCION', 'tipo':orm.XPDSTRING, 'tamano':128, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'monto', 'nombreCampo':'MONTO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'saldo', 'nombreCampo':'SALDO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'id_evaluado', 'nombreCampo':'ID_EVALUADO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'fkIcono', 'whereClause':['id_icono'], },
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByEvaluado', 'whereClause':['id_evaluado'], },
        ]
    })

Metas = orm.Entidad()
Metas.setMetamodelo({
    'nombreTabla' : 'META',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'descripcion', 'nombreCampo':'DESCRIPCION', 'tipo':orm.XPDSTRING, 'tamano':128, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_icono', 'nombreCampo':'ID_ICONO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'puntos_requeridos', 'nombreCampo':'PUNTOS_REQUERIDOS', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'puntos_logro', 'nombreCampo':'PUNTOS_LOGRO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'fecha_creacion', 'nombreCampo':'FECHA_CREACION', 'tipo':orm.XPDDATE, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'fecha_vencimiento', 'nombreCampo':'FECHA_VENCIMIENTO', 'tipo':orm.XPDDATE, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_evaluado', 'nombreCampo':'ID_EVALUADO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'fkIcono', 'whereClause':['id_icono'], },
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByEvaluado', 'whereClause':['id_evaluado'], },
        ]
    })

Logros = orm.Entidad()
Logros.setMetamodelo({
    'nombreTabla' : 'LOGRO',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'id_icono', 'nombreCampo':'ID_ICONO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'descripcion', 'nombreCampo':'DESCRIPCION', 'tipo':orm.XPDDATE, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'fecha', 'nombreCampo':'FECHA', 'tipo':orm.XPDDATE, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'puntos_requeridos', 'nombreCampo':'PUNTOS_REQUERIDOS', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'puntos_logro', 'nombreCampo':'PUNTOS_LOGRO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'id_evaluado', 'nombreCampo':'ID_EVALUADO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'fk_icono', 'whereClause':['id_icono'], },
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByEvaluado', 'whereClause':['id_evaluado'], },
        ]
    })


def inicializar():
    entidades = [Evaluados, Premios, PlantillaTransaccions, Iconos, Transaccions, Metas, Logros]
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
    

def evaluado_getowner(conexion, id_evaluado):
    objeto = Evaluados.getNamedQuery(conexion, 'findById', {'id': id_evaluado})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, objeto['id_user'])

def premio_getowner(conexion, id_premio):
    objeto = Premios.getNamedQuery(conexion, 'findById', {'id': id_premio})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, objeto['id_user'])

def transaccion_getowner(conexion, id_transaccion):
    objeto = Transaccions.getNamedQuery(conexion, 'findById', {'id': id_transaccion})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, evaluado_getowner(conexion, objeto['id_evaluado'])[1] )

def meta_getowner(conexion, id_meta):
    objeto = Metas.getNamedQuery(conexion, 'findById', {'id': id_meta})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, evaluado_getowner(conexion, objeto['id_evaluado'])[1] )

def logro_getowner(conexion, id_logro):
    objeto = Logros.getNamedQuery(conexion, 'findById', {'id': id_logro})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, evaluado_getowner(conexion, objeto['id_evaluado'])[1] )

def servir_page_editar_evaluado(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    evaluado, id_usuario_owner = evaluado_getowner( conexion , id)
    conexion.close()
    if evaluado is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_sistema_puntos/editar_Evaluado", objeto = evaluado, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_sistema_puntos/evaluados/" + str(evaluado['id']), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    evaluado["nombre"] = request.forms.get( "nombre", "").strip()
        
    if len(evaluado["nombre"]) == 0:
        mensajes_error.append("nombre es requerido")

    if len(evaluado["nombre"]) > 16:
        mensajes_error.append("El tamaño de nombre excede el permitido")

    evaluado["id_icono"] = request.forms.get( "id_icono", "").strip()
        
    try:
        evaluado["id_icono"] = int( evaluado["id_icono"] )
    except:
        mensajes_error.append("El valor de id_icono no es válido")

    evaluado["saldo"] = request.forms.get( "saldo", "").strip()
        
    if len(evaluado["saldo"]) == 0:
        mensajes_error.append("saldo es requerido")

    try:
        evaluado["saldo"] = int( evaluado["saldo"] )
    except:
        mensajes_error.append("El valor de saldo no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_sistema_puntos/editar_Evaluado", objeto = evaluado, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_sistema_puntos/evaluados/" + str(evaluado['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Evaluados.actualizar, evaluado)
    except:
        return template("xpd_sistema_puntos/editar_Evaluado", objeto = evaluado, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_sistema_puntos/evaluados/" + str(evaluado['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_sistema_puntos/editar_Evaluado", objeto = evaluado, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_sistema_puntos/evaluados/" + str(evaluado['id']), fecha_iso_to_js = fecha_iso_to_js )

CONFIG['rutas'].append({'ruta':'/evaluados/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_evaluado })

def servir_page_insertar_evaluado():

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    evaluado = Evaluados.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_sistema_puntos/editar_Evaluado", objeto = evaluado, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_sistema_puntos/evaluados", fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    evaluado['id_user'] = usuario['id']

    evaluado["nombre"] = request.forms.get( "nombre", "").strip()
        
    if len(evaluado["nombre"]) == 0:
        mensajes_error.append("nombre es requerido")

    if len(evaluado["nombre"]) > 16:
        mensajes_error.append("El tamaño de nombre excede el permitido")

    evaluado["id_icono"] = request.forms.get( "id_icono", "").strip()
        
    try:
        evaluado["id_icono"] = int( evaluado["id_icono"] )
    except:
        mensajes_error.append("El valor de id_icono no es válido")

    evaluado["saldo"] = request.forms.get( "saldo", "").strip()
        
    if len(evaluado["saldo"]) == 0:
        mensajes_error.append("saldo es requerido")

    try:
        evaluado["saldo"] = int( evaluado["saldo"] )
    except:
        mensajes_error.append("El valor de saldo no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_sistema_puntos/editar_Evaluado", objeto = evaluado, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_sistema_puntos/evaluados", fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Evaluados.insertar, evaluado)
    except:
        return template("xpd_sistema_puntos/editar_Evaluado", objeto = evaluado, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_sistema_puntos/evaluados", fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_sistema_puntos/evaluados/" + str(evaluado['id']) )

CONFIG['rutas'].append({'ruta':'/evaluados/nuevo', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_evaluado })

def servir_page_get_evaluado_lista():
    conexion = orm.Conexion(PATH_BDD)

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    
    conexion = orm.Conexion(PATH_BDD)

    lista = Evaluados.getNamedQuery(conexion, 'findByUser', {'id_user':usuario['id']})

    conexion.close()

    return template("xpd_sistema_puntos/listar_Evaluado", lista = lista, usuario = usuario)
    
CONFIG['rutas'].append({'ruta':'/evaluados', 'metodos':['GET'], 'funcion': servir_page_get_evaluado_lista })

def servir_page_get_evaluado_byid(id_evaluado):    

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = evaluado_getowner(conexion, id_evaluado)
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    
    transaccions = Transaccions.getNamedQuery( conexion, "findByEvaluado", {'id_evaluado':objeto['id']} )

    metas = Metas.getNamedQuery( conexion, "findByEvaluado", {'id_evaluado':objeto['id']} )

    logros = Logros.getNamedQuery( conexion, "findByEvaluado", {'id_evaluado':objeto['id']} )

    conexion.close()
    return template("xpd_sistema_puntos/show_evaluado", objeto = objeto, usuario = usuario , transaccions = transaccions, metas = metas, logros = logros)

CONFIG['rutas'].append({'ruta':'/evaluados/<id_evaluado>', 'metodos':['GET'], 'funcion': servir_page_get_evaluado_byid })

def servir_page_editar_premio(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    premio, id_usuario_owner = premio_getowner( conexion , id)
    conexion.close()
    if premio is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_sistema_puntos/editar_Premio", objeto = premio, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_sistema_puntos/premios/" + str(premio['id']), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    premio["id_icono"] = request.forms.get( "id_icono", "").strip()
        
    try:
        premio["id_icono"] = int( premio["id_icono"] )
    except:
        mensajes_error.append("El valor de id_icono no es válido")

    premio["descripcion"] = request.forms.get( "descripcion", "").strip()
        
    if len(premio["descripcion"]) == 0:
        mensajes_error.append("descripcion es requerido")

    if len(premio["descripcion"]) > 256:
        mensajes_error.append("El tamaño de descripcion excede el permitido")

    premio["puntos_requeridos"] = request.forms.get( "puntos_requeridos", "").strip()
        
    if len(premio["puntos_requeridos"]) == 0:
        mensajes_error.append("puntos_requeridos es requerido")

    try:
        premio["puntos_requeridos"] = int( premio["puntos_requeridos"] )
    except:
        mensajes_error.append("El valor de puntos_requeridos no es válido")

    premio["puntos_logro"] = request.forms.get( "puntos_logro", "").strip()
        
    if len(premio["puntos_logro"]) == 0:
        mensajes_error.append("puntos_logro es requerido")

    try:
        premio["puntos_logro"] = int( premio["puntos_logro"] )
    except:
        mensajes_error.append("El valor de puntos_logro no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_sistema_puntos/editar_Premio", objeto = premio, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_sistema_puntos/premios/" + str(premio['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Premios.actualizar, premio)
    except:
        return template("xpd_sistema_puntos/editar_Premio", objeto = premio, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_sistema_puntos/premios/" + str(premio['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_sistema_puntos/editar_Premio", objeto = premio, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_sistema_puntos/premios/" + str(premio['id']), fecha_iso_to_js = fecha_iso_to_js )

CONFIG['rutas'].append({'ruta':'/premios/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_premio })

def servir_page_insertar_premio():

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    premio = Premios.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_sistema_puntos/editar_Premio", objeto = premio, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_sistema_puntos/premios", fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    premio['id_user'] = usuario['id']

    premio["id_icono"] = request.forms.get( "id_icono", "").strip()
        
    try:
        premio["id_icono"] = int( premio["id_icono"] )
    except:
        mensajes_error.append("El valor de id_icono no es válido")

    premio["descripcion"] = request.forms.get( "descripcion", "").strip()
        
    if len(premio["descripcion"]) == 0:
        mensajes_error.append("descripcion es requerido")

    if len(premio["descripcion"]) > 256:
        mensajes_error.append("El tamaño de descripcion excede el permitido")

    premio["puntos_requeridos"] = request.forms.get( "puntos_requeridos", "").strip()
        
    if len(premio["puntos_requeridos"]) == 0:
        mensajes_error.append("puntos_requeridos es requerido")

    try:
        premio["puntos_requeridos"] = int( premio["puntos_requeridos"] )
    except:
        mensajes_error.append("El valor de puntos_requeridos no es válido")

    premio["puntos_logro"] = request.forms.get( "puntos_logro", "").strip()
        
    if len(premio["puntos_logro"]) == 0:
        mensajes_error.append("puntos_logro es requerido")

    try:
        premio["puntos_logro"] = int( premio["puntos_logro"] )
    except:
        mensajes_error.append("El valor de puntos_logro no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_sistema_puntos/editar_Premio", objeto = premio, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_sistema_puntos/premios", fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Premios.insertar, premio)
    except:
        return template("xpd_sistema_puntos/editar_Premio", objeto = premio, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_sistema_puntos/premios", fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_sistema_puntos/premios/" + str(premio['id']) )

CONFIG['rutas'].append({'ruta':'/premios/nuevo', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_premio })

def servir_page_get_premio_lista():
    conexion = orm.Conexion(PATH_BDD)

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    
    conexion = orm.Conexion(PATH_BDD)

    lista = Premios.getNamedQuery(conexion, 'findByUser', {'id_user':usuario['id']})

    conexion.close()

    return template("xpd_sistema_puntos/listar_Premio", lista = lista, usuario = usuario)
    
CONFIG['rutas'].append({'ruta':'/premios', 'metodos':['GET'], 'funcion': servir_page_get_premio_lista })

def servir_page_get_premio_byid(id_premio):    

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = premio_getowner(conexion, id_premio)
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    
    conexion.close()
    return template("xpd_sistema_puntos/show_premio", objeto = objeto, usuario = usuario )

CONFIG['rutas'].append({'ruta':'/premios/<id_premio>', 'metodos':['GET'], 'funcion': servir_page_get_premio_byid })

def servir_page_editar_plantillatransaccion(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    plantillatransaccion, id_usuario_owner = plantillatransaccion_getowner( conexion , id)
    conexion.close()
    if plantillatransaccion is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_sistema_puntos/editar_PlantillaTransaccion", objeto = plantillatransaccion, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_sistema_puntos/plantillatransaccions/" + str(plantillatransaccion['id']), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    plantillatransaccion["descripcion"] = request.forms.get( "descripcion", "").strip()
        
    if len(plantillatransaccion["descripcion"]) == 0:
        mensajes_error.append("descripcion es requerido")

    if len(plantillatransaccion["descripcion"]) > 256:
        mensajes_error.append("El tamaño de descripcion excede el permitido")

    plantillatransaccion["puntos"] = request.forms.get( "puntos", "").strip()
        
    if len(plantillatransaccion["puntos"]) == 0:
        mensajes_error.append("puntos es requerido")

    try:
        plantillatransaccion["puntos"] = int( plantillatransaccion["puntos"] )
    except:
        mensajes_error.append("El valor de puntos no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_sistema_puntos/editar_PlantillaTransaccion", objeto = plantillatransaccion, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_sistema_puntos/plantillatransaccions/" + str(plantillatransaccion['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(PlantillaTransaccions.actualizar, plantillatransaccion)
    except:
        return template("xpd_sistema_puntos/editar_PlantillaTransaccion", objeto = plantillatransaccion, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_sistema_puntos/plantillatransaccions/" + str(plantillatransaccion['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_sistema_puntos/editar_PlantillaTransaccion", objeto = plantillatransaccion, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_sistema_puntos/plantillatransaccions/" + str(plantillatransaccion['id']), fecha_iso_to_js = fecha_iso_to_js )

CONFIG['rutas'].append({'ruta':'/plantillatransaccions/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_plantillatransaccion })

def servir_page_insertar_plantillatransaccion():

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    plantillatransaccion = PlantillaTransaccions.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_sistema_puntos/editar_PlantillaTransaccion", objeto = plantillatransaccion, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_sistema_puntos/plantillatransaccions", fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    plantillatransaccion["descripcion"] = request.forms.get( "descripcion", "").strip()
        
    if len(plantillatransaccion["descripcion"]) == 0:
        mensajes_error.append("descripcion es requerido")

    if len(plantillatransaccion["descripcion"]) > 256:
        mensajes_error.append("El tamaño de descripcion excede el permitido")

    plantillatransaccion["puntos"] = request.forms.get( "puntos", "").strip()
        
    if len(plantillatransaccion["puntos"]) == 0:
        mensajes_error.append("puntos es requerido")

    try:
        plantillatransaccion["puntos"] = int( plantillatransaccion["puntos"] )
    except:
        mensajes_error.append("El valor de puntos no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_sistema_puntos/editar_PlantillaTransaccion", objeto = plantillatransaccion, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_sistema_puntos/plantillatransaccions", fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(PlantillaTransaccions.insertar, plantillatransaccion)
    except:
        return template("xpd_sistema_puntos/editar_PlantillaTransaccion", objeto = plantillatransaccion, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_sistema_puntos/plantillatransaccions", fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_sistema_puntos/plantillatransaccions/" + str(plantillatransaccion['id']) )

CONFIG['rutas'].append({'ruta':'/plantillatransaccions/nuevo', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_plantillatransaccion })

def servir_page_get_plantillatransaccion_lista():
    conexion = orm.Conexion(PATH_BDD)

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    
    conexion = orm.Conexion(PATH_BDD)

    lista = PlantillaTransaccions.getNamedQuery(conexion, 'findAll', {})
    conexion.close()

    return template("xpd_sistema_puntos/listar_PlantillaTransaccion", lista = lista, usuario = usuario)
    
CONFIG['rutas'].append({'ruta':'/plantillatransaccions', 'metodos':['GET'], 'funcion': servir_page_get_plantillatransaccion_lista })

def servir_page_get_plantillatransaccion_byid(id_plantillatransaccion):    

    conexion = orm.Conexion(PATH_BDD)
    objeto = PlantillaTransaccions.getNamedQuery(conexion, 'findById', {'id': id_plantillatransaccion})
    if len(objeto) == 0:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )
    objeto = objeto[0]
    
    conexion.close()
    return template("xpd_sistema_puntos/show_PlantillaTransaccion", objeto = objeto )

CONFIG['rutas'].append({'ruta':'/plantillatransaccions/<id_plantillatransaccion>', 'metodos':['GET'], 'funcion': servir_page_get_plantillatransaccion_byid })

def servir_page_editar_icono(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    icono, id_usuario_owner = icono_getowner( conexion , id)
    conexion.close()
    if icono is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_sistema_puntos/editar_Icono", objeto = icono, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_sistema_puntos/iconos/" + str(icono['id']), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    icono["icono"] = request.forms.get( "icono", "").strip()
        
    if len(icono["icono"]) == 0:
        mensajes_error.append("icono es requerido")

    if len(icono["icono"]) > 4:
        mensajes_error.append("El tamaño de icono excede el permitido")

    if len(mensajes_error) > 0:
        return template("xpd_sistema_puntos/editar_Icono", objeto = icono, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_sistema_puntos/iconos/" + str(icono['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Iconos.actualizar, icono)
    except:
        return template("xpd_sistema_puntos/editar_Icono", objeto = icono, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_sistema_puntos/iconos/" + str(icono['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_sistema_puntos/editar_Icono", objeto = icono, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_sistema_puntos/iconos/" + str(icono['id']), fecha_iso_to_js = fecha_iso_to_js )

CONFIG['rutas'].append({'ruta':'/iconos/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_icono })

def servir_page_insertar_icono():

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    icono = Iconos.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_sistema_puntos/editar_Icono", objeto = icono, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_sistema_puntos/iconos", fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    icono["icono"] = request.forms.get( "icono", "").strip()
        
    if len(icono["icono"]) == 0:
        mensajes_error.append("icono es requerido")

    if len(icono["icono"]) > 4:
        mensajes_error.append("El tamaño de icono excede el permitido")

    if len(mensajes_error) > 0:
        return template("xpd_sistema_puntos/editar_Icono", objeto = icono, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_sistema_puntos/iconos", fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Iconos.insertar, icono)
    except:
        return template("xpd_sistema_puntos/editar_Icono", objeto = icono, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_sistema_puntos/iconos", fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_sistema_puntos/iconos/" + str(icono['id']) )

CONFIG['rutas'].append({'ruta':'/iconos/nuevo', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_icono })

def servir_page_get_icono_lista():
    conexion = orm.Conexion(PATH_BDD)

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    
    conexion = orm.Conexion(PATH_BDD)

    lista = Iconos.getNamedQuery(conexion, 'findAll', {})
    conexion.close()

    return template("xpd_sistema_puntos/listar_Icono", lista = lista, usuario = usuario)
    
CONFIG['rutas'].append({'ruta':'/iconos', 'metodos':['GET'], 'funcion': servir_page_get_icono_lista })

def servir_page_get_icono_byid(id_icono):    

    conexion = orm.Conexion(PATH_BDD)
    objeto = Iconos.getNamedQuery(conexion, 'findById', {'id': id_icono})
    if len(objeto) == 0:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )
    objeto = objeto[0]
    
    conexion.close()
    return template("xpd_sistema_puntos/show_Icono", objeto = objeto )

CONFIG['rutas'].append({'ruta':'/iconos/<id_icono>', 'metodos':['GET'], 'funcion': servir_page_get_icono_byid })

def servir_page_editar_transaccion(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    transaccion, id_usuario_owner = transaccion_getowner( conexion , id)
    conexion.close()
    if transaccion is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_sistema_puntos/editar_Transaccion", objeto = transaccion, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_sistema_puntos/transaccions/" + str(transaccion['id']), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    transaccion["fecha"] = request.forms.get( "fecha", "").strip()
        
    if len(transaccion["fecha"]) == 0:
        mensajes_error.append("fecha es requerido")

    try:
        if len(transaccion["fecha"]) > 0:
            transaccion["fecha"] = fecha_js_to_iso(transaccion["fecha"])
    except:
        mensajes_error.append("fecha no es una fecha válida")

    transaccion["id_icono"] = request.forms.get( "id_icono", "").strip()
        
    try:
        transaccion["id_icono"] = int( transaccion["id_icono"] )
    except:
        mensajes_error.append("El valor de id_icono no es válido")

    transaccion["descripcion"] = request.forms.get( "descripcion", "").strip()
        
    if len(transaccion["descripcion"]) == 0:
        mensajes_error.append("descripcion es requerido")

    if len(transaccion["descripcion"]) > 128:
        mensajes_error.append("El tamaño de descripcion excede el permitido")

    transaccion["monto"] = request.forms.get( "monto", "").strip()
        
    if len(transaccion["monto"]) == 0:
        mensajes_error.append("monto es requerido")

    try:
        transaccion["monto"] = int( transaccion["monto"] )
    except:
        mensajes_error.append("El valor de monto no es válido")

    transaccion["saldo"] = request.forms.get( "saldo", "").strip()
        
    if len(transaccion["saldo"]) == 0:
        mensajes_error.append("saldo es requerido")

    try:
        transaccion["saldo"] = int( transaccion["saldo"] )
    except:
        mensajes_error.append("El valor de saldo no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_sistema_puntos/editar_Transaccion", objeto = transaccion, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_sistema_puntos/transaccions/" + str(transaccion['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Transaccions.actualizar, transaccion)
    except:
        return template("xpd_sistema_puntos/editar_Transaccion", objeto = transaccion, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_sistema_puntos/transaccions/" + str(transaccion['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_sistema_puntos/editar_Transaccion", objeto = transaccion, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_sistema_puntos/transaccions/" + str(transaccion['id']), fecha_iso_to_js = fecha_iso_to_js )

CONFIG['rutas'].append({'ruta':'/transaccions/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_transaccion })

def servir_page_insertar_transaccion(id_evaluado):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    evaluado, id_usuario_owner = evaluado_getowner( conexion , id_evaluado)
    conexion.close()
    if evaluado is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )

    transaccion = Transaccions.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_sistema_puntos/editar_Transaccion", objeto = transaccion, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_sistema_puntos/evaluados/" + str(id_evaluado), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    transaccion['id_evaluado'] = id_evaluado

    transaccion["fecha"] = request.forms.get( "fecha", "").strip()
        
    if len(transaccion["fecha"]) == 0:
        mensajes_error.append("fecha es requerido")

    transaccion["id_icono"] = request.forms.get( "id_icono", "").strip()
        
    try:
        transaccion["id_icono"] = int( transaccion["id_icono"] )
    except:
        mensajes_error.append("El valor de id_icono no es válido")

    transaccion["descripcion"] = request.forms.get( "descripcion", "").strip()
        
    if len(transaccion["descripcion"]) == 0:
        mensajes_error.append("descripcion es requerido")

    if len(transaccion["descripcion"]) > 128:
        mensajes_error.append("El tamaño de descripcion excede el permitido")

    transaccion["monto"] = request.forms.get( "monto", "").strip()
        
    if len(transaccion["monto"]) == 0:
        mensajes_error.append("monto es requerido")

    try:
        transaccion["monto"] = int( transaccion["monto"] )
    except:
        mensajes_error.append("El valor de monto no es válido")

    transaccion["saldo"] = request.forms.get( "saldo", "").strip()
        
    if len(transaccion["saldo"]) == 0:
        mensajes_error.append("saldo es requerido")

    try:
        transaccion["saldo"] = int( transaccion["saldo"] )
    except:
        mensajes_error.append("El valor de saldo no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_sistema_puntos/editar_Transaccion", objeto = transaccion, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_sistema_puntos/evaluados/" + str(id_evaluado), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Transaccions.insertar, transaccion)
    except:
        return template("xpd_sistema_puntos/editar_Transaccion", objeto = transaccion, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_sistema_puntos/evaluados/" + str(id_evaluado), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_sistema_puntos/transaccions/" + str(transaccion['id']) )

CONFIG['rutas'].append({'ruta':'/evaluados/<id_evaluado>/nuevotransaccion', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_transaccion })

def servir_page_get_transaccion_byid(id_transaccion):    

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = transaccion_getowner(conexion, id_transaccion)
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    
    conexion.close()
    return template("xpd_sistema_puntos/show_transaccion", objeto = objeto, usuario = usuario )

CONFIG['rutas'].append({'ruta':'/transaccions/<id_transaccion>', 'metodos':['GET'], 'funcion': servir_page_get_transaccion_byid })

def servir_page_editar_meta(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    meta, id_usuario_owner = meta_getowner( conexion , id)
    conexion.close()
    if meta is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_sistema_puntos/editar_Meta", objeto = meta, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_sistema_puntos/metas/" + str(meta['id']), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    meta["descripcion"] = request.forms.get( "descripcion", "").strip()
        
    if len(meta["descripcion"]) == 0:
        mensajes_error.append("descripcion es requerido")

    if len(meta["descripcion"]) > 128:
        mensajes_error.append("El tamaño de descripcion excede el permitido")

    meta["id_icono"] = request.forms.get( "id_icono", "").strip()
        
    try:
        meta["id_icono"] = int( meta["id_icono"] )
    except:
        mensajes_error.append("El valor de id_icono no es válido")

    meta["puntos_requeridos"] = request.forms.get( "puntos_requeridos", "").strip()
        
    if len(meta["puntos_requeridos"]) == 0:
        mensajes_error.append("puntos_requeridos es requerido")

    try:
        meta["puntos_requeridos"] = int( meta["puntos_requeridos"] )
    except:
        mensajes_error.append("El valor de puntos_requeridos no es válido")

    meta["puntos_logro"] = request.forms.get( "puntos_logro", "").strip()
        
    if len(meta["puntos_logro"]) == 0:
        mensajes_error.append("puntos_logro es requerido")

    try:
        meta["puntos_logro"] = int( meta["puntos_logro"] )
    except:
        mensajes_error.append("El valor de puntos_logro no es válido")

    meta["fecha_creacion"] = request.forms.get( "fecha_creacion", "").strip()
        
    if len(meta["fecha_creacion"]) == 0:
        mensajes_error.append("fecha_creacion es requerido")

    try:
        if len(meta["fecha_creacion"]) > 0:
            meta["fecha_creacion"] = fecha_js_to_iso(meta["fecha_creacion"])
    except:
        mensajes_error.append("fecha_creacion no es una fecha válida")

    meta["fecha_vencimiento"] = request.forms.get( "fecha_vencimiento", "").strip()
        
    if len(meta["fecha_vencimiento"]) == 0:
        mensajes_error.append("fecha_vencimiento es requerido")

    try:
        if len(meta["fecha_vencimiento"]) > 0:
            meta["fecha_vencimiento"] = fecha_js_to_iso(meta["fecha_vencimiento"])
    except:
        mensajes_error.append("fecha_vencimiento no es una fecha válida")

    if len(mensajes_error) > 0:
        return template("xpd_sistema_puntos/editar_Meta", objeto = meta, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_sistema_puntos/metas/" + str(meta['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Metas.actualizar, meta)
    except:
        return template("xpd_sistema_puntos/editar_Meta", objeto = meta, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_sistema_puntos/metas/" + str(meta['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_sistema_puntos/editar_Meta", objeto = meta, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_sistema_puntos/metas/" + str(meta['id']), fecha_iso_to_js = fecha_iso_to_js )

CONFIG['rutas'].append({'ruta':'/metas/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_meta })

def servir_page_insertar_meta(id_evaluado):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    evaluado, id_usuario_owner = evaluado_getowner( conexion , id_evaluado)
    conexion.close()
    if evaluado is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )

    meta = Metas.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_sistema_puntos/editar_Meta", objeto = meta, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_sistema_puntos/evaluados/" + str(id_evaluado), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    meta['id_evaluado'] = id_evaluado

    meta["descripcion"] = request.forms.get( "descripcion", "").strip()
        
    if len(meta["descripcion"]) == 0:
        mensajes_error.append("descripcion es requerido")

    if len(meta["descripcion"]) > 128:
        mensajes_error.append("El tamaño de descripcion excede el permitido")

    meta["id_icono"] = request.forms.get( "id_icono", "").strip()
        
    try:
        meta["id_icono"] = int( meta["id_icono"] )
    except:
        mensajes_error.append("El valor de id_icono no es válido")

    meta["puntos_requeridos"] = request.forms.get( "puntos_requeridos", "").strip()
        
    if len(meta["puntos_requeridos"]) == 0:
        mensajes_error.append("puntos_requeridos es requerido")

    try:
        meta["puntos_requeridos"] = int( meta["puntos_requeridos"] )
    except:
        mensajes_error.append("El valor de puntos_requeridos no es válido")

    meta["puntos_logro"] = request.forms.get( "puntos_logro", "").strip()
        
    if len(meta["puntos_logro"]) == 0:
        mensajes_error.append("puntos_logro es requerido")

    try:
        meta["puntos_logro"] = int( meta["puntos_logro"] )
    except:
        mensajes_error.append("El valor de puntos_logro no es válido")

    meta["fecha_creacion"] = request.forms.get( "fecha_creacion", "").strip()
        
    if len(meta["fecha_creacion"]) == 0:
        mensajes_error.append("fecha_creacion es requerido")

    meta["fecha_vencimiento"] = request.forms.get( "fecha_vencimiento", "").strip()
        
    if len(meta["fecha_vencimiento"]) == 0:
        mensajes_error.append("fecha_vencimiento es requerido")

    if len(mensajes_error) > 0:
        return template("xpd_sistema_puntos/editar_Meta", objeto = meta, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_sistema_puntos/evaluados/" + str(id_evaluado), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Metas.insertar, meta)
    except:
        return template("xpd_sistema_puntos/editar_Meta", objeto = meta, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_sistema_puntos/evaluados/" + str(id_evaluado), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_sistema_puntos/metas/" + str(meta['id']) )

CONFIG['rutas'].append({'ruta':'/evaluados/<id_evaluado>/nuevometa', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_meta })

def servir_page_get_meta_byid(id_meta):    

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = meta_getowner(conexion, id_meta)
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    
    conexion.close()
    return template("xpd_sistema_puntos/show_meta", objeto = objeto, usuario = usuario )

CONFIG['rutas'].append({'ruta':'/metas/<id_meta>', 'metodos':['GET'], 'funcion': servir_page_get_meta_byid })

def servir_page_editar_logro(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    logro, id_usuario_owner = logro_getowner( conexion , id)
    conexion.close()
    if logro is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_sistema_puntos/editar_Logro", objeto = logro, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_sistema_puntos/logros/" + str(logro['id']), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    logro["id_icono"] = request.forms.get( "id_icono", "").strip()
        
    try:
        logro["id_icono"] = int( logro["id_icono"] )
    except:
        mensajes_error.append("El valor de id_icono no es válido")

    logro["descripcion"] = request.forms.get( "descripcion", "").strip()
        
    if len(logro["descripcion"]) == 0:
        mensajes_error.append("descripcion es requerido")

    try:
        if len(logro["descripcion"]) > 0:
            logro["descripcion"] = fecha_js_to_iso(logro["descripcion"])
    except:
        mensajes_error.append("descripcion no es una fecha válida")

    logro["fecha"] = request.forms.get( "fecha", "").strip()
        
    if len(logro["fecha"]) == 0:
        mensajes_error.append("fecha es requerido")

    try:
        if len(logro["fecha"]) > 0:
            logro["fecha"] = fecha_js_to_iso(logro["fecha"])
    except:
        mensajes_error.append("fecha no es una fecha válida")

    logro["puntos_requeridos"] = request.forms.get( "puntos_requeridos", "").strip()
        
    if len(logro["puntos_requeridos"]) == 0:
        mensajes_error.append("puntos_requeridos es requerido")

    try:
        logro["puntos_requeridos"] = int( logro["puntos_requeridos"] )
    except:
        mensajes_error.append("El valor de puntos_requeridos no es válido")

    logro["puntos_logro"] = request.forms.get( "puntos_logro", "").strip()
        
    if len(logro["puntos_logro"]) == 0:
        mensajes_error.append("puntos_logro es requerido")

    try:
        logro["puntos_logro"] = int( logro["puntos_logro"] )
    except:
        mensajes_error.append("El valor de puntos_logro no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_sistema_puntos/editar_Logro", objeto = logro, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_sistema_puntos/logros/" + str(logro['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Logros.actualizar, logro)
    except:
        return template("xpd_sistema_puntos/editar_Logro", objeto = logro, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_sistema_puntos/logros/" + str(logro['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_sistema_puntos/editar_Logro", objeto = logro, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_sistema_puntos/logros/" + str(logro['id']), fecha_iso_to_js = fecha_iso_to_js )

CONFIG['rutas'].append({'ruta':'/logros/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_logro })

def servir_page_insertar_logro(id_evaluado):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    evaluado, id_usuario_owner = evaluado_getowner( conexion , id_evaluado)
    conexion.close()
    if evaluado is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )

    logro = Logros.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_sistema_puntos/editar_Logro", objeto = logro, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_sistema_puntos/evaluados/" + str(id_evaluado), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    logro['id_evaluado'] = id_evaluado

    logro["id_icono"] = request.forms.get( "id_icono", "").strip()
        
    try:
        logro["id_icono"] = int( logro["id_icono"] )
    except:
        mensajes_error.append("El valor de id_icono no es válido")

    logro["descripcion"] = request.forms.get( "descripcion", "").strip()
        
    if len(logro["descripcion"]) == 0:
        mensajes_error.append("descripcion es requerido")

    logro["fecha"] = request.forms.get( "fecha", "").strip()
        
    if len(logro["fecha"]) == 0:
        mensajes_error.append("fecha es requerido")

    logro["puntos_requeridos"] = request.forms.get( "puntos_requeridos", "").strip()
        
    if len(logro["puntos_requeridos"]) == 0:
        mensajes_error.append("puntos_requeridos es requerido")

    try:
        logro["puntos_requeridos"] = int( logro["puntos_requeridos"] )
    except:
        mensajes_error.append("El valor de puntos_requeridos no es válido")

    logro["puntos_logro"] = request.forms.get( "puntos_logro", "").strip()
        
    if len(logro["puntos_logro"]) == 0:
        mensajes_error.append("puntos_logro es requerido")

    try:
        logro["puntos_logro"] = int( logro["puntos_logro"] )
    except:
        mensajes_error.append("El valor de puntos_logro no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_sistema_puntos/editar_Logro", objeto = logro, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_sistema_puntos/evaluados/" + str(id_evaluado), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Logros.insertar, logro)
    except:
        return template("xpd_sistema_puntos/editar_Logro", objeto = logro, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_sistema_puntos/evaluados/" + str(id_evaluado), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_sistema_puntos/logros/" + str(logro['id']) )

CONFIG['rutas'].append({'ruta':'/evaluados/<id_evaluado>/nuevologro', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_logro })

def servir_page_get_logro_byid(id_logro):    

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = logro_getowner(conexion, id_logro)
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    
    conexion.close()
    return template("xpd_sistema_puntos/show_logro", objeto = objeto, usuario = usuario )

CONFIG['rutas'].append({'ruta':'/logros/<id_logro>', 'metodos':['GET'], 'funcion': servir_page_get_logro_byid })

def servir_page_main():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    entidades = [
         { 'nombre': 'Evaluados', 'path':'/xpd_sistema_puntos/evaluados'  },
         { 'nombre': 'Premios', 'path':'/xpd_sistema_puntos/premios'  },

    ]
    return template("xpd_sistema_puntos/main", usuario = usuario, titulo = "xpd_sistema_puntos", entidades = entidades)

CONFIG['rutas'].append({'ruta':'/main', 'metodos':['GET'], 'funcion': servir_page_main })

def servir_page_admin_main():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    if 'Administrador' not in usuario['roles']:
        abort(403,"Acceso Denegado")  

    entidades = [
         { 'nombre': 'PlantillaTransaccions', 'path':'/xpd_sistema_puntos/plantillatransaccions'  },
         { 'nombre': 'Iconos', 'path':'/xpd_sistema_puntos/iconos'  },

    ]
    return template("xpd_sistema_puntos/main", usuario = usuario, titulo = "Administración", entidades = entidades)

CONFIG['rutas'].append({'ruta':'/admin', 'metodos':['GET'], 'funcion': servir_page_admin_main })

def rutearModulo( app : Bottle, ruta_base : str ):
    CONFIG['RUTA_BASE'] = ruta_base
    for item in CONFIG['rutas']:
        app.route( ruta_base + item['ruta'], method = item['metodos'] )( item['funcion'])
