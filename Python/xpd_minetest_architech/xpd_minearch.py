import xpd_orm as orm
from os.path import abspath , dirname, exists

from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH
from bottle import Bottle

from hashlib import sha256

from uuid import uuid4

import datetime

import xpd_usr

PATH_BDD = dirname(abspath(__file__)) + "/data/base.db"
PATH_INIT = dirname(abspath(__file__)) + "/data/init_usr.sql"

CONFIG = {}

Edificios = orm.Entidad()
Edificios.setMetamodelo({
    "nombreTabla":"XMA_EDIFICIO",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"id_usuario", "nombreCampo":"ID_USUARIO", "tipo":orm.XPDINTEGER, },
        { "nombre":"nombre", "nombreCampo":"NOMBRE", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"descripcion", "nombreCampo":"DESCRIPCION", "tipo":orm.XPDSTRING, "tamano":128, },
        { "nombre":"fecha_creacion", "nombreCampo":"FECHA_CREACION", "tipo":orm.XPDDATE },
        { "nombre":"es_publico", "nombreCampo":"ES_PUBLICO", "tipo":orm.XPDINTEGER, },
        { "nombre":"activo", "nombreCampo":"ACTIVO", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findById", "whereClause":["id",], },
        { "nombre":"findByUserActivo", "whereClause":["id_usuario", "activo",],  "orderBy":["fecha_creacion",],  },
        { "nombre":"findByPublicoActivo", "whereClause":["es_publico", "activo",],  "orderBy":["fecha_creacion",],  },
        ]
    })

Bloques = orm.Entidad()
Bloques.setMetamodelo({
    "nombreTabla":"XMA_BLOQUE",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"id_edificio", "nombreCampo":"ID_EDIFICIO", "tipo":orm.XPDINTEGER, },
        { "nombre":"tipo_bloque", "nombreCampo":"TIPO_BLOQUE", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"x", "nombreCampo":"X", "tipo":orm.XPDINTEGER, },
        { "nombre":"y", "nombreCampo":"Y", "tipo":orm.XPDINTEGER, },
        { "nombre":"z", "nombreCampo":"Z", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findByEdificio", "whereClause":["id_edificio",], "orderBy":["x","y","z"] },
        { "nombre":"findById", "whereClause":["id",], },
        ]
    })

def inicializar():
    entidades = [Edificios, Bloques]
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

def servir_lista_edificios():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    con = orm.Conexion(PATH_BDD)
    edificios_usuario = Edificios.getNamedQuery(con, 'findByUserActivo', {'id_usuario': usuario['id'], 'activo': 1})
    edificios_publico = Edificios.getNamedQuery(con, 'findByPublicoActivo', {'es_publico': 1, 'activo': 1})
    con.close()
    return template('xpd_minearch/edificios', usuario = usuario, edificios_usuario = edificios_usuario, edificios_publicos = edificios_publico)

def servir_bloques(id_edificio):
    con = orm.Conexion(PATH_BDD)
    edificio = Edificios.getNamedQuery(con, 'findById', {'id':id_edificio })
    bloques = Bloques.getNamedQuery(con, 'findByEdificio', {'id_edificio':id_edificio })
    con.close()
    if len(edificio) == 0:
        error(404, "No encontrado")
    edificio = edificio[0]
    edificio['bloques'] = bloques

    if edificio['es_publico'] == 0:
        usuario = xpd_usr.getCurrentUser(request)
        if usuario is None or usuario['id'] != edificio['id_usuario']:
            error(403, 'No Autorizado')

    return edificio

def servir_crear_edificio():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    
    edificio = {'nombre': '', 'descripcion': '', 'es_publico': 0}
    
    if request.method == 'GET':    
        return template('xpd_minearch/edificio', usuario = usuario, edificio = edificio , lvl='', mensaje='')
    
    # Se asume POST
    edificio['nombre'] = request.forms.get('nombre', '')
    edificio['descripcion'] = request.forms.get('descripcion', '')
    edificio['es_publico'] = int(request.forms.get('es_publico', '0'))

    if '' in [ edificio['nombre'], edificio['descripcion'] ]:
        return template('xpd_minearch/edificio', usuario = usuario, edificio = edificio , lvl='danger', mensaje='Por favor complete la información')

    con = orm.Conexion(PATH_BDD)
    try:
        edificio['id_usuario'] = usuario['id']
        edificio['activo'] = 1
        edificio['fecha_creacion'] = datetime.datetime.now().isoformat()
        Edificios.insertar(con,edificio)

        bloque = { 'id_edificio': edificio['id'], 'tipo_bloque': 'default:brick', 'x': 0, 'y': 0, 'z': 0 }
        Bloques.insertar(con, bloque)
        con.commit()
    except Exception as ex:
        print('Error al crear edificio: ' + repr(ex))
        con.rollback()        
        return template( 'xpd_minearch/edificio', usuario = usuario, edificio = edificio , lvl = 'danger', mensaje = 'Error al crear edificio: ' + repr(ex))
    finally:
        con.close()
    return template('xpd_usr/mensaje', lvl ='success', mensaje = 'Edificio Registrado exitosamente', href = CONFIG['RUTA_BASE'] + '/edificio/{0}'.format(edificio['id']) )

def servir_editar_edificio(id_edificio):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    
    con = orm.Conexion(PATH_BDD)
    edificio = Edificios.getNamedQuery(con, 'findById', {'id':id_edificio })
    con.close()
    
    if len(edificio) == 0:
        return template('xpd_usr/mensaje', lvl ='danger', mensaje = 'Edificio no existe', href = '/' )

    edificio = edificio[0]
    if edificio['id_usuario'] != usuario['id']:
        return template('xpd_usr/mensaje', lvl ='danger', mensaje = 'Edificio no Autorizado', href = '/' )
    
    if request.method == 'GET':
        return template('xpd_minearch/edificio', usuario = usuario, edificio = edificio, lvl = '', mensaje = '' )
    
    # Se asume POST para actualizar

    edificio['nombre'] = request.forms.get('nombre', '')
    edificio['descripcion'] = request.forms.get('descripcion', '')
    edificio['es_publico'] = int(request.forms.get('es_publico', '0'))    

    if '' in [ edificio['nombre'], edificio['descripcion'] ]:
        return template('xpd_minearch/edificio', usuario = usuario, edificio = edificio , lvl='danger', mensaje='Por favor complete la información')

    try:
        edificio['fecha_creacion'] = datetime.datetime.now().isoformat()
        transaccionar(Edificios.actualizar, edificio)
    except Exception as ex:
        return template('xpd_minearch/edificio', usuario = usuario, edificio = edificio , lvl='danger', mensaje='Por favor complete la información')
    
    return template('xpd_minearch/edificio', usuario = usuario, edificio = edificio, lvl = 'success', mensaje = 'Edificio actualizado exitosamente' )

def servir_editarbloques_edificio(id_edificio):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    
    con = orm.Conexion(PATH_BDD)
    edificio = Edificios.getNamedQuery(con, 'findById', {'id':id_edificio })
    con.close()
    
    if len(edificio) == 0:
        return template('xpd_usr/mensaje', lvl ='danger', mensaje = 'Edificio no existe', href = '/' )

    edificio = edificio[0]

    return template('xpd_minearch/edificio_editar', usuario = usuario, edificio = edificio )

def servir_crear_bloque(id_edificio):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error(401, "No autorizado")
    
    con = orm.Conexion(PATH_BDD)
    edificio = Edificios.getNamedQuery(con, 'findById', {'id':id_edificio })
    con.close()
    
    if len(edificio) == 0:
        error(404, "No existente")

    edificio = edificio[0]
    if edificio['id_usuario'] != usuario['id']:
        error(403, "No autorizado")
    
    try:
        bloque = {'id_edificio': edificio['id'], 'tipo_bloque': request.forms.get('tipo_bloque'), 'x': int(request.forms.get('x')), 'y': int(request.forms.get('y')), 'z': int(request.forms.get('z')) }
    except Exception as ex:
        error(400, "No valido")
    
    try:
        transaccionar(Bloques.insertar, bloque)
    except Exception as ex:
        print("Error al crear Bloque " + repr(ex))
        error(500, "Error al crear Bloque " + repr(ex))
    
    return bloque


def servir_editar_bloque(id_edificio, id_bloque):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        error(401, "No autorizado")
    
    con = orm.Conexion(PATH_BDD)
    edificio = Edificios.getNamedQuery(con, 'findById', {'id':id_edificio })
    bloque = Bloques.getNamedQuery(con, 'findById', {'id':id_bloque })
    con.close()
    
    if len(edificio) == 0 or len(bloque) == 0:
        error(404, "No existente")
    
    edificio = edificio[0]
    bloque = bloque[0]

    if bloque['id_edificio'] != edificio['id']:
        error(404, "No existente")

    if request.method == "DELETE":
        try:
            transaccionar(Bloques.eliminar, bloque)
        except Exception as ex:
            print("Error al eliminar Bloque " + repr(ex))
            error(500, "Error al eliminar Bloque " + repr(ex))
        return {'exito': 'OK Eliminado'}
    
    # Se asume metodo POST
    try:
        bloque['tipo_bloque'] = request.forms.get('tipo_bloque')
        bloque['x'] = int(request.forms.get('x'))
        bloque['y'] = int(request.forms.get('y'))
        bloque['z'] = int(request.forms.get('z'))
    except Exception as ex:
        error(400, "No valido")

    try:
        transaccionar(Bloques.actualizar, bloque)
    except Exception as ex:
        print("Error al actualizar Bloque " + repr(ex))
        error(500, "Error al actualizar Bloque " + repr(ex))
    
    return bloque

def rutearModulo( app : Bottle, ruta_base : str ):
    # encapsula Session Middleware
    CONFIG['RUTA_BASE'] = ruta_base

    app.route( ruta_base + '/edificios' , method = ['GET'])(servir_lista_edificios)
    app.route( ruta_base + '/edificio/crear' , method = ['GET','POST'])(servir_crear_edificio)
    app.route( ruta_base + '/edificio/<id_edificio>' , method = ['GET','POST'])(servir_editar_edificio)
    app.route( ruta_base + '/edificio/<id_edificio>/editarbloques' , method = ['GET'])(servir_editarbloques_edificio)
    app.route( ruta_base + '/edificio/<id_edificio>/bloques' , method = ['GET','POST'])(servir_bloques)
    app.route( ruta_base + '/edificio/<id_edificio>/bloques/crear' , method = ['POST'])(servir_crear_bloque)
    app.route( ruta_base + '/edificio/<id_edificio>/bloques/<id_bloque>' , method = ['POST','DELETE'])(servir_editar_bloque)
