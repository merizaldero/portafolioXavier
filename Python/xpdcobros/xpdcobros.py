import xpd_orm as orm
import xpd_usr
from os.path import abspath , dirname, join, exists
from os import remove as remove_file
import datetime
from uuid import uuid4

from bottle import error, template, request, response, redirect
from bottle import Bottle

from hashlib import sha256

import json

CONFIG = {  }

CONFIG_COSTO_SOLICITUD = 'COSTO_SOLICITUD'
CONFIG_ROOT_ID_ORGANIZACION = 'ROOT_ID_ORGANIZACION'

PATH_BDD = join( dirname(abspath(__file__)) , "data", "base.db")

# TEMPLATE_PATH.append( join( dirname(abspath(__file__)) , "views" ) )

Configs = orm.Entidad()
Configs.setMetamodelo({
    "nombreTabla":"XCB_CONFIG",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDSTRING, "tamano":16, "pk":True },
        { "nombre":"descripcion", "nombreCampo":"DESCRIPCION", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"valor", "nombreCampo":"VALOR", "tipo":orm.XPDSTRING, "tamano":16, },
        ],
    "namedQueries":[
        { "nombre":"findAll", "orderByClause":["id"] },
        { "nombre":"findById", "whereClause":["id"] },
        ]
    })

Organizaciones = orm.Entidad()
Organizaciones.setMetamodelo({
    "nombreTabla":"XCB_ORGANIZACION",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"nombre", "nombreCampo":"NOMBRE", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"email", "nombreCampo":"EMAIL", "tipo":orm.XPDSTRING, "tamano":64, },
        { "nombre":"id_usuario", "nombreCampo":"ID_USUARIO", "tipo":orm.XPDINTEGER, },
        { "nombre":"uuid", "nombreCampo":"UUID", "tipo":orm.XPDSTRING, "tamano":36, },
        { "nombre":"saldo", "nombreCampo":"SALDO", "tipo":orm.XPDREAL, "tamano":8, "precision":2 },
        { "nombre":"fecha_saldo", "nombreCampo":"FECHA_SALDO", "tipo":orm.XPDDATE, },
        { "nombre":"activo", "nombreCampo":"ACTIVO", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findAll", "orderByClause":["nombre"] },
        { "nombre":"findById", "whereClause":["id"] },
        { "nombre":"findByUuid", "whereClause":["uuid"] },
        ]
    })

UsuariosOrganizacion = orm.Entidad()
UsuariosOrganizacion.setMetamodelo({
    "nombreTabla":"XCB_USUARIO_ORGANIZACION",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"id_organizacion", "nombreCampo":"ID_ORGANIZACION", "tipo":orm.XPDINTEGER, },
        { "nombre":"id_usuario", "nombreCampo":"ID_USUARIO", "tipo":orm.XPDINTEGER, },
        { "nombre":"activo", "nombreCampo":"ACTIVO", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[        
        { "nombre":"findById", "whereClause":["id"] },
        { "nombre":"findByUsuarioOrganizacion", "whereClause":["id_usuario", "id_organizacion"] },
        ]
    })

CuentasBcoOrganizacion = orm.Entidad()
CuentasBcoOrganizacion.setMetamodelo({
    "nombreTabla":"XCB_CTA_BCO_ORGANIZACION", 
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"id_organizacion", "nombreCampo":"ID_ORGANIZACION", "tipo":orm.XPDINTEGER, },
        { "nombre":"nombre_banco", "nombreCampo":"NOMBRE_BANCO", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"tipo_cuenta", "nombreCampo":"TIPO_CUENTA", "tipo":orm.XPDSTRING, "tamano":8, },
        { "nombre":"numero_cuenta", "nombreCampo":"NUMERO_CUENTA", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"saldo", "nombreCampo":"SALDO", "tipo":orm.XPDREAL, "tamano":8, "precision":2 },
        { "nombre":"fecha_saldo", "nombreCampo":"FECHA_SALDO", "tipo":orm.XPDDATE, },
        { "nombre":"activo", "nombreCampo":"ACTIVO", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findByOrganizacion", "whereClause":["id_organizacion"],'orderBuClause':['nombre_banco']  },
        { "nombre":"findByIdCobrador", "whereClause":["id", "id_organizacion"], },
        { "nombre":"findByOrganizacionActivo", "whereClause":["id_organizacion","activo"],'orderBuClause':['nombre_banco'] },
        ]
    })

Pagadores = orm.Entidad()
Pagadores.setMetamodelo({
    "nombreTabla":"XCB_PAGADOR",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"id_organizacion", "nombreCampo":"ID_ORGANIZACION", "tipo":orm.XPDINTEGER, },
        { "nombre":"email", "nombreCampo":"EMAIL", "tipo":orm.XPDSTRING, "tamano":64, },
        { "nombre":"nombre", "nombreCampo":"NOMBRE", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"saldo", "nombreCampo":"SALDO", "tipo":orm.XPDREAL, "tamano":8, "precision":2 },
        { "nombre":"fecha_saldo", "nombreCampo":"FECHA_SALDO", "tipo":orm.XPDDATE, },
        ],
    "namedQueries":[
        { "nombre":"findAll", "orderByClause":["nombre"] },
        { "nombre":"findById", "whereClause":["id"] },
        { "nombre":"findByOrganizacionEmail", "whereClause":["id_organizacion", "email"] },
        { "nombre":"findByOrganizacion", "whereClause":["id_organizacion"], 'orderByClause':['email'] },
        ]
    })

OrdenesPago = orm.Entidad()
OrdenesPago.setMetamodelo({
    "nombreTabla":"XCB_ORDEN_PAGO",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"id_organizacion", "nombreCampo":"ID_ORGANIZACION", "tipo":orm.XPDINTEGER, },
        { "nombre":"id_pagador", "nombreCampo":"ID_PAGADOR", "tipo":orm.XPDINTEGER, },
        { "nombre":"monto", "nombreCampo":"MONTO", "tipo":orm.XPDREAL, "tamano":8, "precision":2 },
        { "nombre":"fecha_emision", "nombreCampo":"FECHA_EMISION", "tipo":orm.XPDDATE, },
        { "nombre":"fecha_vencimiento", "nombreCampo":"FECHA_VENCIMIENTO", "tipo":orm.XPDDATE, },
        { "nombre":"descripcion", "nombreCampo":"DESCRIPCION", "tipo":orm.XPDSTRING, "tamano":64, },
        { "nombre":"metadatos", "nombreCampo":"METADATOS", "tipo":orm.XPDSTRING, "tamano":2048, },
        { "nombre":"fecha_pago", "nombreCampo":"FECHA_PAGO", "tipo":orm.XPDDATE, },
        { "nombre":"monto_pendiente", "nombreCampo":"MONTO_PENDIENTE", "tipo":orm.XPDREAL, "tamano":8, "precision":2 },
        { "nombre":"pagado", "nombreCampo":"PAGADO", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findById", "orderByClause":["nombre"] },
        { "nombre":"findByPagadorPagado", "whereClause":["id_pagador","pagado"], "orderByClause":["fecha_emision"] },
        ]
    })

Abonos = orm.Entidad()
Abonos.setMetamodelo({
    "nombreTabla":"XCB_ABONO",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"id_organizacion", "nombreCampo":"ID_ORGANIZACION", "tipo":orm.XPDINTEGER, },
        { "nombre":"id_pagador", "nombreCampo":"ID_PAGADOR", "tipo":orm.XPDINTEGER, },
        { "nombre":"id_orden_pago", "nombreCampo":"ID_ORDEN_PAGO", "tipo":orm.XPDINTEGER, },
        # { "nombre":"id_ctabco", "nombreCampo":"ID_CTA_BCO", "tipo":orm.XPDINTEGER, },
        { "nombre":"nombre_banco", "nombreCampo":"NOMBRE_BANCO", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"tipo_cuenta", "nombreCampo":"TIPO_CUENTA", "tipo":orm.XPDSTRING, "tamano":8, },
        { "nombre":"numero_cuenta", "nombreCampo":"NUMERO_CUENTA", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"numero_transaccion", "nombreCampo":"NUMERO_TRANSACCION", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"id_imagen", "nombreCampo":"ID_IMAGEN", "tipo":orm.XPDINTEGER, },
        { "nombre":"fecha_registro", "nombreCampo":"FECHA_REGISTRO", "tipo":orm.XPDDATE, },
        { "nombre":"fecha_transaccion", "nombreCampo":"FECHA_TRANSACCION", "tipo":orm.XPDDATE, },
        { "nombre":"monto_registrado", "nombreCampo":"MONTO_REGISTRADO", "tipo":orm.XPDREAL, "tamano":8, "precision":2 },
        { "nombre":"monto_aprobado", "nombreCampo":"MONTO_APROBADO", "tipo":orm.XPDREAL, "tamano":8, "precision":2 },
        { "nombre":"fecha_feedback", "nombreCampo":"FECHA_FEEDBACK", "tipo":orm.XPDDATE, },
        { "nombre":"id_usuario_feedback", "nombreCampo":"ID_USUARIO_FEEDBACK", "tipo":orm.XPDINTEGER, },
        { "nombre":"estado", "nombreCampo":"ESTADO", "tipo":orm.XPDSTRING, "tamano":1, },
        { "nombre":"observaciones", "nombreCampo":"OBSERVACIONES", "tipo":orm.XPDSTRING, "tamano":256, },
        # R: Registrado, A: Aprobado, X: Rechazado
        ],
    "namedQueries":[
        { "nombre":"findByPagadorEstado", "whereClause":["id_pagador","estado"], "orderByClause":["fecha_registro"] },
        { "nombre":"findByOrganizacionEstado", "whereClause":["id_organizacion","estado"], "orderByClause":["fecha_registro"] },
        { "nombre":"findByOrdenpagoEstado", "whereClause":["id_orden_pago","estado"], "orderByClause":["fecha_registro"] },
        { "nombre":"findByOrdenpago", "whereClause":["id_orden_pago"], "orderByClause":["fecha_registro"] },
        ]
    })

Imagenes = orm.Entidad()
Imagenes.setMetamodelo({
    "nombreTabla":"XCB_IMAGEN",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"nombre", "nombreCampo":"NOMBRE", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"tipo", "nombreCampo":"TIPO", "tipo":orm.XPDSTRING, "tamano":16, },
        { "nombre":"contenido", "nombreCampo":"CONTENIDO", "tipo":orm.XPDLONGBINARY, },
        { "nombre":"path_archivo", "nombreCampo":"PATH_ARCHIVO", "tipo":orm.XPDSTRING, 'tamano':512, },
        { "nombre":"transcripcion", "nombreCampo":"TRANSCRIPCION", "tipo":orm.XPDSTRING, 'tamano':2048, },
        { "nombre":"id_usuario", "nombreCampo":"ID_USUARIO", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findById", "whereClause":["id"], },
        { "nombre":"findByUsuario", "whereClause":["id_usuario"], },
        ]
    })

AbonosOrdenPago = orm.Entidad()
AbonosOrdenPago.setMetamodelo({
    "nombreTabla":"XCB_ABONO_ORDEN_PAGO",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"id_abono", "nombreCampo":"ID_ABONO", "tipo":orm.XPDINTEGER, },
        { "nombre":"id_orden_pago", "nombreCampo":"ID_ORDEN_PAGO", "tipo":orm.XPDINTEGER, },
        { "nombre":"monto", "nombreCampo":"MONTO", "tipo":orm.XPDREAL, "tamano":8, "precision":2 },
        { "nombre":"saldo_abono", "nombreCampo":"SALDO_ABONO", "tipo":orm.XPDREAL, "tamano":8, "precision":2 },
        { "nombre":"saldo_orden_pago", "nombreCampo":"SALDO_ORDEN_PAGO", "tipo":orm.XPDREAL, "tamano":8, "precision":2 },
        { "nombre":"fecha_hora", "nombreCampo":"FECHA_HORA", "tipo":orm.XPDDATE, },
        ],
    "namedQueries":[
        { "nombre":"findByAbono", "whereClause":["id_abono"], "orderByClause":["fecha_hora"] },
        { "nombre":"findByOrdenPago", "whereClause":["id_orden_pago"], "orderByClause":["fecha_hora"] },        
        ]
    })

SolicitudesOrganizacion = orm.Entidad()
SolicitudesOrganizacion.setMetamodelo({
    "nombreTabla":"XCB_SOLICITUD_ORGANIZACION",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"id_usuario", "nombreCampo":"ID_USUARIO", "tipo":orm.XPDINTEGER, },
        { "nombre":"nombre", "nombreCampo":"NOMBRE", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"email", "nombreCampo":"EMAIL", "tipo":orm.XPDSTRING, "tamano":64, },
        { "nombre":"id_orden_pago", "nombreCampo":"ID_ORDEN_PAGO", "tipo":orm.XPDINTEGER, },
        { "nombre":"pagado", "nombreCampo":"PAGADO", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findAll", "orderByClause":["nombre"] },
        { "nombre":"findById", "whereClause":["id"] },
        ]
    })

POST_INICIALIZADORES = []

def agregar_inicializador(inicializador):
    POST_INICIALIZADORES.append(inicializador)

def inicializar():
    entidades = [ Configs, Organizaciones, UsuariosOrganizacion, Pagadores, OrdenesPago, CuentasBcoOrganizacion, Abonos, Imagenes, AbonosOrdenPago, SolicitudesOrganizacion ]
    con = orm.Conexion(PATH_BDD)
    try:
        for entidad in entidades:
            entidad.crearTabla(con)

        for postinicializador in POST_INICIALIZADORES:
            postinicializador(con)
        con.commit()
    except Exception as ex:
        con.rollback()
        print(ex)
        raise Exception(str(ex))
    finally:
        con.close()

def inicializadorAdminCobros(con, usernameAdmin, claveAdmin, emailAdmin, nombreCobrador ):
    # Crea Rol Administrador
    rol = {'rolename':'Administrador', 'descripcion':'Administrador' , 'activo':1}
    xpd_usr.registrar_rol(con, rol)

    # Crea usuario inicial Administrador
    usuario = {'username':usernameAdmin, 'password':claveAdmin , 'email':emailAdmin, 'activo':1}
    xpd_usr.registrar_usuario(con, usuario)

    usuario_rol = {'id_usuario': usuario['id'], 'id_rol': rol['id'], 'activo': 1 }
    xpd_usr.UsuarioRoles.insertar(con, usuario_rol)

    # Crea cobradorInicial
    organizacion = {'nombre':nombreCobrador, 'email':emailAdmin, 'id_usuario': usuario['id'] }
    crear_organizacion(con, organizacion)

    usuario_organizacion = {'id_usuario': usuario['id'], 'id_organizacion': organizacion['id'], 'activo': 1 }
    UsuariosOrganizacion.insertar(con, usuario_organizacion)

    # Crea configuracion
    config_id_organizacion = {'id':CONFIG_ROOT_ID_ORGANIZACION , 'descripcion': 'ID de Cobrador por Defecto', 'valor':str(organizacion['id'])}
    Configs.insertar(con, config_id_organizacion)
    config_costo = {'id':CONFIG_COSTO_SOLICITUD, 'descripcion':'Costo de Solicitud de Cobrador', 'valor':'5.00' }
    Configs.insertar(con, config_costo)

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
      
def get_organizaciones_by_usuario(con: orm.Conexion, id_usuario):
    sql = """
select a.ID id, b.ID id_organizacion, b.NOMBRE nombre, b.EMAIL email 
from XCB_USUARIO_ORGANIZACION a 
inner join XCB_ORGANIZACION b on b.ID = a.ID_ORGANIZACION
where a.ID_USUARIO = :id_usuario and a.ACTIVO = 1
order by 3
"""
    lista = con.consultar(sql,{'id_usuario': id_usuario}, [ 'id', 'id_organizacion', 'nombre', 'email' ])
    return lista

def crear_organizacion(con: orm.Conexion, organizacion):
    organizacion['uuid'] = str(uuid4())
    organizacion['saldo'] = 0.0
    organizacion['fecha_saldo'] = datetime.datetime.now().isoformat() 
    organizacion['activo'] = 1
    Organizaciones.insertar(con, organizacion)
    return organizacion

def validar_insercion_organizacion(con: orm.Conexion, organizacion):
    validaciones = []

    sql_1 = """select a.id ID , a.NOMBRE nombre, a.EMAIL email from XCB_ORGANIZACION a 
where lower(a.NOMBRE) = :nombre """
    sql_2 = """select a.id ID , a.NOMBRE nombre, a.EMAIL email from XCB_ORGANIZACION a 
where lower(a.EMAIL) = :email"""
    if organizacion['nombre'] == '' or organizacion['email'] == '':
        validaciones.append('Informaci&oacute;n Incompleta')
    repetidos = con.consultar(sql_1,{'nombre':organizacion['nombre'].lower() }, ['id', 'nombre', 'email'])
    if len(repetidos) > 0:
        validaciones.append('El nombre de Cobrador ya se encuentra en uso')

    repetidos = con.consultar(sql_2,{'email':organizacion['email'].lower() }, ['id', 'nombre', 'email'])
    if len(repetidos) > 0:
        validaciones.append('El Email de Cobrador ya se encuentra en uso')

    return validaciones

def validar_actualizacion_organizacion(con: orm.Conexion, organizacion):
    validaciones = []

    sql_1 = """select a.id ID , a.NOMBRE nombre, a.EMAIL email from XCB_ORGANIZACION a 
where a.ID <> :id and lower(a.NOMBRE) = :nombre """
    sql_2 = """select a.id ID , a.NOMBRE nombre, a.EMAIL email from XCB_ORGANIZACION a 
where a.ID <> :id and lower(a.EMAIL) = :email """

    repetidos = con.consultar(sql_1,{'id': organizacion['id'] , 'nombre':organizacion['nombre'].lower() }, ['id', 'nombre', 'email'])
    if len(repetidos) > 0:
        validaciones.append('El nombre de Cobrador ya se encuentra en uso')

    repetidos = con.consultar(sql_2,{'id': organizacion['id'], 'email':organizacion['email'].lower() }, ['id', 'nombre', 'email'])
    if len(repetidos) > 0:
        validaciones.append('El Email de Cobrador ya se encuentra en uso')

    return validaciones

def get_config(con, id_config):
    lista = Configs.getNamedQuery(con, 'findById', {'id':id_config})
    if len(lista) == 0:
        return None
    return lista[0]['valor']

def crear_pagador(con:orm.Conexion, pagador):
    if 'nombre' not in pagador.keys() or pagador['nombre'] is None or pagador['nombre'].strip() == '':
        pagador['nombre'] = pagador['email']
    pagador['saldo'] = 0.0
    pagador['fecha_saldo'] = datetime.datetime.now().isoformat()
    pagador['activo'] = 1
    print('Insertando Pagador {0}'.format(pagador['email']))
    Pagadores.insertar(con, pagador)
    return pagador

def crear_orden_pago( con:orm.Conexion, orden_pago):
    if 'id_pagador' not in orden_pago.keys() or orden_pago['id_pagador'] is None:
        if 'email_pagador' not in orden_pago.keys():
            raise Exception('No se especifica información de pagador')
        pagador = Pagadores.getNamedQuery(con, 'findByOrganizacionEmail' , {'id_organizacion': orden_pago['id_organizacion'], 'email': orden_pago['email_pagador'] } )
        if len(pagador) > 0 :
            orden_pago['id_pagador'] = pagador[0]['id']
        else :
            pagador = {'id_organizacion': orden_pago['id_organizacion'], 'email':orden_pago['email_pagador'] }
            pagador = crear_pagador(con, pagador)
            orden_pago['id_pagador'] = pagador['id']
    orden_pago['fecha_pago'] = None
    orden_pago['monto_pendiente'] = orden_pago['monto']
    orden_pago['pagado'] = 0    
    print('Insertando OrdenPago {0}'.format(orden_pago['id_pagador']))
    OrdenesPago.insertar(con, orden_pago)
    return orden_pago

def incrementar_saldo_pagador(con:orm.Conexion, id_pagador, delta = 0.00):
    fecha_trx = datetime.datetime.now()
    pagador = Pagadores.getNamedQuery(con, 'findById',{'id':id_pagador})[0]
    pagador['saldo'] += delta
    pagador['fecha_saldo'] = fecha_trx
    Pagadores.actualizar(con, pagador)

def crear_solicitud_organizacion(con: orm.Conexion, solicitud):
    fecha_trx = datetime.datetime.now()

    # determina ID Cobrador
    id_organizacion = get_config(con, CONFIG_ROOT_ID_ORGANIZACION)
    if not id_organizacion is None:
        id_organizacion = int(id_organizacion)
    costo_solicitud = get_config(con, CONFIG_COSTO_SOLICITUD)
    if costo_solicitud is None:
        costo_solicitud = 0.0
    else:
        costo_solicitud = round(float(costo_solicitud), 2)
    
    orden_pago = {'id_organizacion':id_organizacion, 'email_pagador': solicitud['email_pagador'], 'monto': costo_solicitud, 
                  'fecha_emision': fecha_trx, 'fecha_vencimiento': fecha_trx + datetime.timedelta(days=2),
                  'descripcion': 'Alta Cobrador {0}'.format(solicitud['nombre']),
                  'metadatos': json.dumps( { 'data':[{'key':'nombre', 'value': solicitud['nombre'] }, {'key':'email', 'value': solicitud['email'] } ] } )
                  }
    print('Ingresa orden pago {0}'.format(repr(orden_pago)))
    orden_pago = crear_orden_pago(con, orden_pago)
    
    solicitud['pagado'] = 0
    solicitud['id_orden_pago'] = orden_pago['id']
    print('Insertando solicitud {0}'.format(solicitud['email']))
    SolicitudesOrganizacion.insertar(con, solicitud)

    # Actualiza saldo de pagador
    incrementar_saldo_pagador(con, orden_pago['id_pagador'], - orden_pago['monto'] )

    return solicitud

def get_abonos_by_parametro(con:orm.Conexion, nombre_parametro, id_parametro):
    
    sql = """SELECT a.id as id, a.id_organizacion as id_organizacion, a.id_pagador as id_pagador, a.id_orden_pago as id_orden_pago, a.nombre_banco as nombre_banco, a.tipo_cuenta as tipo_cuenta, a.numero_cuenta as numero_cuenta, a.id_imagen as id_imagen, a.fecha_registro as fecha_registro, a.fecha_transaccion as fecha_transaccion, a.monto_registrado as monto_registrado, a.monto_aprobado as monto_aprobado, a.fecha_feedback as fecha_feedback, a.id_usuario_feedback as id_usuario_feedback, a.estado as estado 
    , b.nombre as nombre_organizacion, b.email as email_organizacion, b.id_usuario as id_usuario_organizacion, b.uuid as uuid_organizacion, b.saldo as saldo_organizacion, b.fecha_saldo as fecha_saldo_organizacion, b.activo as activo_organizacion
    , c.id_organizacion as id_organizacion_pagador, c.email as email_pagador, c.nombre as nombre_pagador, c.saldo as saldo_pagador, c.fecha_saldo as fecha_saldo_pagador
    FROM XCB_ABONO a 
    inner join XCB_ORGANIZACION b on b.ID = a.ID_ORGANIZACION
    inner join XCB_PAGADOR c on c.ID = a.ID_PAGADOR     
    WHERE a.{0} = :{0}
    ORDER BY a.fecha_registro desc""".format(nombre_parametro)
    
    lista = con.consultar(sql, { nombre_parametro: id_parametro}, [ 
        'id', 'id_organizacion', 'id_pagador', 'id_orden_pago', 'nombre_banco', 'tipo_cuenta', 'numero_cuenta', 'id_imagen', 'fecha_registro', 'fecha_transaccion', 'monto_registrado', 'monto_aprobado', 'fecha_feedback', 'id_usuario_feedback', 'estado',
        'nombre_organizacion', 'email_organizacion', 'id_usuario_organizacion', 'uuid_organizacion', 'saldo_organizacion', 'fecha_saldo_organizacion', 'activo_organizacion',
        'id_organizacion_pagador', 'email_pagador', 'nombre_pagador', 'saldo_pagador', 'fecha_saldo_pagador',
        ])
    return lista

def servir_api_main():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    con = orm.Conexion(PATH_BDD)
    organizaciones = get_organizaciones_by_usuario(con, usuario['id'])
    con.close()
    return template('xpdcobros/main', usuario = usuario, organizaciones = organizaciones )

def servir_usr_solicitar_organizacion():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    
    con = orm.Conexion(PATH_BDD)
    costo_solicitud = get_config(con, CONFIG_COSTO_SOLICITUD )
    con.close()

    if request.method == 'GET':
        return template('xpdcobros/solicitar_organizacion', 
                        usuario = usuario, 
                        solicitud = {'nombre':'', 'email':''},
                        costo = costo_solicitud, 
                        acciones = 'registrar', 
                        msg_tipo='info', msg='Ingrese la informaci&oacute; del nuevo Cobrador',
                        )
    
    nombre = request.forms.get('txt_nombre','').strip()
    email = request.forms.get('txt_email', '').strip().lower()
    accion = request.forms.get('hid_accion', '')    

    solicitud = {'nombre':nombre, 'email':email}
    
    if accion == '':
        return template('xpdcobros/solicitar_organizacion', 
                        usuario = usuario, 
                        solicitud = solicitud,
                        costo = costo_solicitud,
                        acciones = 'registrar', 
                        msg_tipo='danger', msg='Acci&oacute;n no v&aacute;lida',
                        )
    elif accion == 'registrar':
        return template('xpdcobros/solicitar_organizacion', 
                        usuario = usuario, 
                        solicitud = solicitud,
                        costo = costo_solicitud, 
                        acciones = 'registrar', 
                        msg_tipo='info', msg='Ingrese la informaci&oacute; del nuevo Cobrador'
                        )
    elif accion == 'validar':        
        con = orm.Conexion(PATH_BDD)
        validaciones = validar_insercion_organizacion(con, solicitud)
        con.close()
        if len(validaciones) > 0:
            return template('xpdcobros/solicitar_organizacion', 
                        usuario = usuario, 
                        solicitud = solicitud, 
                        costo = costo_solicitud,
                        acciones = 'registrar', 
                        msg_tipo='danger', msg=' / '.join(validaciones)
                        )
        return template('xpdcobros/solicitar_organizacion', 
                        usuario = usuario, 
                        solicitud = solicitud, 
                        costo = costo_solicitud,
                        acciones = 'validar', 
                        msg_tipo='info', msg='Verifique la Informaci&oacute;n antes de Completar'
                        )
    elif accion == 'completar':
        try:
            solicitud['id_usuario'] = usuario['id']
            solicitud['email_pagador'] = usuario['email']
            print('Ingresa solicitud {0}'.format(repr(solicitud)))            
            transaccionar(crear_solicitud_organizacion,solicitud)
            return template('xpdcobros/solicitar_organizacion', 
                        usuario = usuario,
                        solicitud = solicitud, 
                        costo = costo_solicitud,
                        acciones = 'completado', 
                        msg_tipo='success', msg = 'Su solicitud ha sido registrada exitosamente. Su Organización será generada una vez que su pago sea Registrado y Aprobado'
                        )
        except orm.XpdException as xex:
            return template('xpdcobros/solicitar_organizacion', 
                        usuario = usuario,
                        solicitud = solicitud, 
                        costo = costo_solicitud,
                        acciones = 'registrar', 
                        msg_tipo='danger', msg = 'Se ha producido un error al registrar su solicitud. Por favor intente m&aacute;s tarde.'
                        )
        except Exception as ex:
            return template('xpdcobros/solicitar_organizacion', 
                        usuario = usuario,
                        solicitud = solicitud, 
                        costo = costo_solicitud,
                        acciones = 'registrar', 
                        msg_tipo='danger', msg = 'Se ha producido un error al registrar su solicitud. Por favor intente m&aacute;s tarde.'
                        )

def servir_cob_listar_pagos_pendientes(uuid_organizacion, email_pagador):
    con = orm.Conexion(PATH_BDD)

    cobrador = Organizaciones.getNamedQuery(con, 'findByUuid',{'uuid':uuid_organizacion})
    if len(cobrador) == 0:
        con.close()
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'Información de Cobrador no disponible', href='/')
    cobrador = cobrador[0]

    pagador = Pagadores.getNamedQuery(con, 'findByOrganizacionEmail',{'id_organizacion':cobrador['id'], 'email': email_pagador})
    if len(pagador) == 0:
        con.close()
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'Pagador {0} no se encuentra registrado con Cobrador {1}'.format(email_pagador, cobrador['nombre']) , href='/')
    pagador = pagador[0]

    ordenes_pago = OrdenesPago.getNamedQuery(con, 'findByPagadorPagado',{'id_pagador':pagador['id'], 'pagado':0 })
    if len(ordenes_pago) == 0:
        con.close()
        return template('xpd_usr/mensaje', lvl='info', mensaje = 'Pagador {0} no tiene pagos pendientes con {1}'.format(email_pagador, cobrador['nombre']) , href='/')   

    con.close()
    return template('xpdcobros/pagos_pendientes', cobrador = cobrador, pagador = pagador, ordenes_pago = ordenes_pago )

def servir_usr_listar_pagos_pendientes():
    
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    
    con = orm.Conexion(PATH_BDD)
    id_organizacion = get_config(con, CONFIG_ROOT_ID_ORGANIZACION)
    if id_organizacion is None:
        con.close()
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'No es posible desplegar información de Cobrador', href='/')
    id_organizacion = int(id_organizacion)
    
    cobrador = Organizaciones.getNamedQuery(con, 'findById',{'id':id_organizacion})
    if len(cobrador) == 0:
        con.close()
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'Información de Cobrador no disponible', href='/')
    cobrador = cobrador[0]

    pagador = Pagadores.getNamedQuery(con, 'findByOrganizacionEmail',{'id_organizacion':id_organizacion, 'email': usuario['email']})
    if len(pagador) == 0:
        con.close()
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'Pagador {0} no se encuentra registrado con Cobrador {1}'.format(usuario['email'], cobrador['nombre']) , href='/')
    pagador = pagador[0]

    ordenes_pago = OrdenesPago.getNamedQuery(con, 'findByPagadorPagado',{'id_pagador':pagador['id'], 'pagado':0 })
    if len(ordenes_pago) == 0:
        con.close()
        return template('xpd_usr/mensaje', lvl='info', mensaje = 'Pagador {0} no tiene pagos pendientes con {1}'.format(usuario['email'], cobrador['nombre']) , href='/')   

    con.close()
    return template('xpdcobros/usr_pagos_pendientes', usuario = usuario, cobrador = cobrador, pagador = pagador, ordenes_pago = ordenes_pago )

def servir_admin_lista_config():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        if request.method == 'POST':
            return {'lvl':'danger', 'mensaje':'Sesion no válida'}
        redirect('/login')

    if not 'roles' in usuario.keys() or 'Administrador' not in usuario['roles'] :
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'Acceso no Autorizado.' , href='/')   
    
    con = orm.Conexion(PATH_BDD)     
    lista = Configs.getNamedQuery(con, 'findAll',{})
    con.close()

    if request.method == 'POST':
        id_config = request.forms.get('id_config','').strip()
        valor_config = request.forms.get('valor_config','').strip()
        if id_config == '':
            return {'lvl':'danger', 'mensaje':'Mensaje de actualización no válido'}
        config_seleccionado = [ x for x in lista if x['id'] == id_config ]
        if len(config_seleccionado) == 0:
            return {'lvl':'danger', 'mensaje':'Configuracion no válida'}
        config_seleccionado = config_seleccionado[0]
        config_seleccionado['valor'] = valor_config
        print("Actualizando Config {0} = {1}".format(config_seleccionado['id'], config_seleccionado['valor']))
        transaccionar( Configs.actualizar, config_seleccionado)
        return {'lvl':'success', 'mensaje':'Actualizacion Existosa'}

    return template('xpdcobros/config', usuario = usuario, configs = lista)

def servir_imagen(id_imagen):
    con = orm.Conexion(PATH_BDD)     
    imagen = Imagenes.getNamedQuery(con, 'findById',{'id':id_imagen})
    con.close()
    if len(imagen) == 0:
        redirect('/static/img/no_existe.png')
    imagen = imagen[0]
    contenido = imagen['contenido']
    if not contenido:
        with open(imagen['path_archivo'], 'rb') as archivo:
            contenido = archivo.read()
    response.add_header('Content-Type',imagen['tipo'])
    return contenido

def consultar_organizacion_usuario(id_organizacion, usuario):
    con = orm.Conexion(PATH_BDD)
    cobrador = con.consultar("""select a.ID id, a.NOMBRE nombre, a.EMAIL email, a.ID_USUARIO id_usuario, a.UUID uuid, a.SALDO saldo, a.FECHA_SALDO fecha_saldo, a.ACTIVO activo from XCB_ORGANIZACION a where a.ID = :id_organizacion and exists(select 1 from XCB_USUARIO_ORGANIZACION b where b.ID_ORGANIZACION = a.ID and b.ID_USUARIO = :id_usuario and b.ACTIVO = 1 ) """, 
                  {'id_organizacion':id_organizacion, 'id_usuario':usuario['id']}, ['id','nombre','email', 'id_usuario', 'uuid','saldo','fecha_saldo','activo'])
    con.close()
    if len(cobrador) == 0:
        return None
    return cobrador[0]

def servir_usr_editar_organizacion(id_organizacion):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')

    # valida que el usuario tenga acceso al cobrador
    cobrador = consultar_organizacion_usuario(id_organizacion, usuario)    
    if cobrador is None:
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'No tiene acceso a la información solicitada' , href='/')   

    if request.method == 'GET':
        # obtiene datos adicionales y los despliega
        con = orm.Conexion(PATH_BDD)
        usuariosCobrador = con.consultar("""select a.ID id, b.ID id_usuario,b.USERNAME username, b.EMAIL email , a.ACTIVO activo from XCB_USUARIO_ORGANIZACION a inner join USUARIOS b on b.ID=a.ID_USUARIO where a.ID_ORGANIZACION = :id_organizacion order by B.USERNAME """,
                  {'id_organizacion':id_organizacion, 'id_usuario':usuario['id']}, ['id','id_usuario','username','email','activo'])
        ctasbco = CuentasBcoOrganizacion.getNamedQuery(con, 'findByOrganizacion',{'id_organizacion':id_organizacion})
        pagadores = Pagadores.getNamedQuery(con, 'findByOrganizacion',{'id_organizacion':id_organizacion})
        con.close()
        return template('xpdcobros/organizacion', usuario=usuario, cobrador=cobrador, usuariosCobrador = usuariosCobrador, ctascbo = ctasbco , pagadores = pagadores)
    
    # Lo siguiente se asume como POST con acciones
    accion = request.forms.get('accion','')
    if accion == "":
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'Accion No Valida' , href= CONFIG['root'] + '/')
    
    if accion == "form_editar_cobrador":
        return template('xpdcobros/editar_organizacion', lvl ='', mensaje= '', usuario = usuario, cobrador=cobrador)

    if accion == "post_editar_cobrador":
        cobrador['nombre'] = request.forms.get('nombre','').strip()
        cobrador['email'] = request.forms.get('email','').strip().lower()
         
        if cobrador['nombre'] == '' or cobrador['email'] == '':            
            return template('xpdcobros/editar_organizacion', lvl ='danger', mensaje= 'Favor completar la información', usuario = usuario, cobrador=cobrador)
        try:
            transaccionar(Organizaciones.actualizar, cobrador)
            return template('xpd_usr/mensaje', lvl='success', mensaje = 'Actualización exitosa' , href= CONFIG['root'] + '/usuarios/organizacion/{0}'.format(cobrador['id']) )
        except Exception as ex:
            return template('xpdcobros/editar_organizacion', lvl ='danger', mensaje=str(ex) , usuario = usuario, cobrador=cobrador)

    if accion == "agregar_usuario":
        email = request.forms.get('email','').strip()
        usuariox = xpd_usr.getUserByEmail(email)
        if usuariox is None:
            return template('xpd_usr/mensaje', lvl='danger', mensaje = 'Usuario no registrado.' , href = CONFIG['root'] + '/usuarios/organizacion/{0}'.format(cobrador['id']) )
        con = orm.Conexion(PATH_BDD)
        usuariosCobrador = con.consultar("""select a.ID id, b.ID id_usuario,b.USERNAME username, b.EMAIL email , b.ACTIVO activo from XCB_USUARIO_ORGANIZACION a inner join USUARIOS b on b.ID=a.ID_USUARIO where a.ID_ORGANIZACION = :id_organizacion order by B.USERNAME """,
                  {'id_organizacion':id_organizacion, 'id_usuario':usuario['id']}, ['id','id_usuario','username','email','activo'])
        con.close()
        if len( [ x for x in usuariosCobrador if x['id_usuario'] == usuariox['id']] ) > 0 :
            return template('xpd_usr/mensaje', lvl='danger', mensaje = 'Usuario ya registrado.' , href = CONFIG['root'] + '/usuarios/organizacion/{0}'.format(cobrador['id']) )
        usuarioCobrador = {'id_organizacion':id_organizacion, 'id_usuario':usuariox['id'], 'activo':1}
        try:
            transaccionar(UsuariosOrganizacion.insertar, usuarioCobrador)
            return template('xpd_usr/mensaje', lvl='success', mensaje = 'Usuario {0}({1}) incluido Exitosamente.'.format(usuariox['username'], usuariox['email']) , href= CONFIG['root'] + '/usuarios/organizacion/{0}'.format(cobrador['id']) )
        except Exception as ex:
            return template('xpd_usr/mensaje', lvl='danger', mensaje = str(ex) , href= CONFIG['root'] + '/usuarios/organizacion/{0}'.format(cobrador['id']) )
    if accion in ["habilitar_usuario", "deshabilitar_usuario"]:
        id_usuario_cobrador = request.forms.get('id_usuario_cobrador')
        con = orm.Conexion(PATH_BDD)
        usuarioCobrador = UsuariosOrganizacion.getNamedQuery(con, 'findById', {'id':id_usuario_cobrador})
        con.close()
        if len(usuarioCobrador) == 0 :
            return template('xpd_usr/mensaje', lvl='danger', mensaje = "Usuario no existe." , href= CONFIG['root'] + '/usuarios/organizacion/{0}'.format(cobrador['id']) )
        usuarioCobrador = usuarioCobrador[0]
        if usuarioCobrador['id_organizacion'] != cobrador['id']:
            return template('xpd_usr/mensaje', lvl='danger', mensaje = "Contexto no válido." , href= CONFIG['root'] + '/usuarios/organizacion/{0}'.format(cobrador['id']) )
        
        usuarioCobrador['activo'] = 1 if accion == "habilitar_usuario" else 0
        try:
            transaccionar(UsuariosOrganizacion.actualizar, usuarioCobrador)            
        except Exception as ex:
            print(repr(ex))
            return template('xpd_usr/mensaje', lvl='danger', mensaje = "Error "+ str(ex) , href= CONFIG['root'] + '/usuarios/organizacion/{0}'.format(cobrador['id']) )
        redirect( CONFIG['root'] + '/usuarios/organizacion/{0}#usuario_{1}'.format(cobrador['id'], usuarioCobrador['id']) )
    if accion in ["habilitar_cuenta", "deshabilitar_cuenta"]:
        id_cuenta = request.forms.get('id_cuenta')
        con = orm.Conexion(PATH_BDD)
        cuenta = CuentasBcoOrganizacion.getNamedQuery(con, 'findByIdCobrador', {'id':id_cuenta, 'id_organizacion':cobrador['id']})
        con.close()
        if len(cuenta) == 0 :
            return template('xpd_usr/mensaje', lvl='danger', mensaje = "Cuenta no existe." , href= CONFIG['root'] + '/usuarios/organizacion/{0}'.format(cobrador['id']) )
        cuenta = cuenta[0]
        
        cuenta['activo'] = 1 if accion == "habilitar_cuenta" else 0
        try:
            transaccionar(CuentasBcoOrganizacion.actualizar, cuenta)            
        except Exception as ex:
            print(repr(ex))
            return template('xpd_usr/mensaje', lvl='danger', mensaje = "Error "+ str(ex) , href= CONFIG['root'] + '/usuarios/organizacion/{0}'.format(cobrador['id']) )
        redirect( CONFIG['root'] + '/usuarios/organizacion/{0}#cuenta_{1}'.format(cobrador['id'], cuenta['id']) )

    return template('xpd_usr/mensaje', lvl='danger', mensaje = 'Accion No Implementada' , href= CONFIG['root'] + '/')

def servir_usr_crear_cuenta(id_organizacion):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    
    # valida que el usuario tenga acceso al cobrador
    cobrador = consultar_organizacion_usuario(id_organizacion, usuario)    
    if cobrador is None:
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'No tiene acceso a la información solicitada' , href='/')   
    
    cuenta = {"id_organizacion":cobrador['id'], 'nombre_banco':'', 'tipo_cuenta':'', 'numero_cuenta':'', 'saldo': 0.00 , 'fecha_saldo': datetime.datetime.now().isoformat(), 'activo':1 }
    
    if request.method == 'GET':
        return template('xpdcobros/editar_cuenta', lvl= '', mensaje= '', usuario = usuario, cobrador = cobrador, cuenta=cuenta)

    # El siguiente procesamiento se asume POST
    cuenta['nombre_banco'] = request.forms.get('nombre_banco', '').strip().upper()
    cuenta['tipo_cuenta'] = request.forms.get('tipo_cuenta', '').strip().upper()
    cuenta['numero_cuenta'] = request.forms.get('numero_cuenta', '').strip()

    if cuenta['nombre_banco'] == '' or cuenta['tipo_cuenta'] == '' or cuenta['numero_cuenta'] == '':
        return template('xpdcobros/editar_cuenta', lvl= 'danger', mensaje= 'Por favor llenar la información de Cuenta', usuario = usuario, cobrador = cobrador, cuenta=cuenta)            
    try:
        transaccionar(CuentasBcoOrganizacion.insertar, cuenta)
    except Exception as ex:
        return template('xpdcobros/editar_cuenta', lvl = 'danger', mensaje = 'Error ' + str(ex) , usuario = usuario, cobrador = cobrador, cuenta=cuenta)
    
    return template('xpd_usr/mensaje', lvl='success', mensaje = 'Cuenta Bancaria registrada exitosamente', href= CONFIG['root'] + '/usuarios/organizacion/{0}/cuentasbco/{1}'.format(cobrador['id'], cuenta['id']) )

def servir_usr_editar_cuenta(id_organizacion, id_cta_bco):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    
    # valida que el usuario tenga acceso al cobrador
    cobrador = consultar_organizacion_usuario(id_organizacion, usuario)    
    if cobrador is None:
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'No tiene acceso a la información solicitada' , href='/')   
    
    con = orm.Conexion(PATH_BDD)
    cuenta = CuentasBcoOrganizacion.getNamedQuery(con, "findByIdCobrador" , {'id':id_cta_bco, 'id_organizacion': cobrador['id'] })    
    con.close()

    if len(cuenta) == 0:
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'Información de cuenta no disponible' , href='/')
    cuenta = cuenta[0]

    if request.method == 'GET':        
        return template('xpdcobros/editar_cuenta', lvl= '', mensaje= '', usuario = usuario, cobrador = cobrador, cuenta=cuenta)

    # El siguiente procesamiento se asume POST
    cuenta['nombre_banco'] = request.forms.get('nombre_banco', '').strip().upper()
    cuenta['tipo_cuenta'] = request.forms.get('tipo_cuenta', '').strip().upper()
    cuenta['numero_cuenta'] = request.forms.get('numero_cuenta', '').strip()

    if cuenta['nombre_banco'] == '' or cuenta['tipo_cuenta'] == '' or cuenta['numero_cuenta'] == '':
        return template('xpdcobros/editar_cuenta', lvl= 'danger', mensaje= 'Por favor llenar la información de Cuenta', usuario = usuario, cobrador = cobrador, cuenta=cuenta)            
    try:
        transaccionar(CuentasBcoOrganizacion.actualizar, cuenta)
    except Exception as ex:
        return template('xpdcobros/editar_cuenta', lvl = 'danger', mensaje = 'Error ' + str(ex) , usuario = usuario, cobrador = cobrador, cuenta=cuenta)
    
    return template('xpd_usr/mensaje', lvl='success', mensaje = 'Cuenta Bancaria registrada exitosamente', href= CONFIG['root'] + '/usuarios/organizacion/{0}/cuentasbco/{1}'.format(cobrador['id'], cuenta['id']) )

def servir_usr_crear_pagador(id_organizacion):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    
    # valida que el usuario tenga acceso al cobrador
    organizacion = consultar_organizacion_usuario(id_organizacion, usuario)    
    if organizacion is None:
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'No tiene acceso a la información solicitada' , href='/')   
    
    if request.method == 'GET':
        cliente = {'nombre':'', 'email':''}
        return template('xpdcobros/editar_cliente', usuario = usuario, organizacion = organizacion, cliente = cliente, lvl='', mensaje = '')
    
    # Asume POST
    cliente = {'nombre': request.forms.get('nombre','').strip(), 'email':request.forms.get('email','').strip().lower(), 'id_organizacion': organizacion['id']}
    # valida que se entregue datos
    if '' in [ cliente['nombre'], cliente['email'] ] :
        return template('xpdcobros/editar_cliente', usuario = usuario, organizacion = organizacion, cliente = cliente, lvl='danger', mensaje = 'Por favor ingresar información requerida.')
    
    # valida que no exista otro cliente con el mismo email
    clientes_registrados = consultar( Pagadores, 'findByOrganizacionEmail', { 'id_organizacion':organizacion['id'], 'email': cliente['email']} )
    if len(clientes_registrados) > 0 :
        return template('xpd_usr/mensaje', lvl='warning', mensaje = 'Ya existe un cliente con correo {0}'.format(cliente['email']) , href='/xpdcobros/usuarios/organizacion/{0}/cliente/{1}'.format(organizacion['id'], clientes_registrados[0]['id']) )   
    
    try:
        cliente = transaccionar(crear_pagador, cliente)
    except Exception as ex:
        print(repr(ex))
        return template('xpdcobros/editar_cliente', usuario = usuario, organizacion = organizacion, cliente = cliente, lvl='danger', mensaje = 'Se ha producido un error al momento de registrar el cliente.')

    return template('xpd_usr/mensaje', lvl='success', mensaje = 'Cliente {0} registrado exitosamente'.format(cliente['nombre']) , href='/xpdcobros/usuarios/organizacion/{0}/cliente/{1}'.format(organizacion['id'], cliente['id']) )   

def servir_usr_editar_pagador(id_organizacion, id_pagador):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    
    # valida que el usuario tenga acceso al cobrador
    organizacion = consultar_organizacion_usuario(id_organizacion, usuario)    
    if organizacion is None:
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'No tiene acceso a la información solicitada' , href='/')   

    cliente = consultar(Pagadores, 'findById', {'id': id_pagador})
    if len(cliente) == 0 or cliente[0]['id_organizacion'] != organizacion['id']:
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'No tiene acceso a la información solicitada' , href='/')
    cliente = cliente[0]
    
    if request.method == 'GET':
        ordenes_pago = consultar( OrdenesPago, 'findByPagadorPagado',{'id_pagador':cliente['id'], 'pagado':0 } )
        con = orm.Conexion(PATH_BDD)
        abonos = get_abonos_by_parametro(con, 'id_pagador', cliente['id'] )        
        con.close()
        
        abonos_registrados = [ x for x in abonos if x['estado'] == 'R' ]
        abonos_aprobados = [ x for x in abonos if x['estado'] == 'A' ]
        abonos_rechazados = [ x for x in abonos if x['estado'] == 'X' ]

        return template('xpdcobros/cliente', usuario = usuario, organizacion = organizacion, cliente = cliente, ordenes_pago = ordenes_pago, abonos_registrados = abonos_registrados, abonos_aprobados=abonos_aprobados, abonos_rechazados = abonos_rechazados , lvl='', mensaje = '')

    # Se asume POST
    accion = request.forms.get('accion','').strip()

    if accion == 'editar':
        return template('xpdcobros/editar_cliente', usuario = usuario, organizacion = organizacion, cliente = cliente, lvl='', mensaje = '')
    
    # Se asume que se va a guardar

    cliente['nombre'] = request.forms.get('nombre','').strip()
    cliente['email'] = request.forms.get('email','').strip().lower()

    # valida que se entregue datos
    if '' in [ cliente['nombre'], cliente['email'] ] :
        return template('xpdcobros/editar_cliente', usuario = usuario, organizacion = organizacion, cliente = cliente, lvl='danger', mensaje = 'Por favor ingresar información requerida.')

    # valida que no exista otro cliente con el mismo email
    clientes_registrados = consultar( Pagadores, 'findByOrganizacionEmail', { 'id_organizacion':organizacion['id'], 'email': cliente['email']} )
    clientes_registrados = [x for x in clientes_registrados if x['id'] != cliente['id']]
    if len( clientes_registrados ) > 0 :
        return template('xpdcobros/editar_cliente', usuario = usuario, organizacion = organizacion, cliente = cliente, lvl='danger', mensaje = 'Existe otro Cliente con la misma dirección de correo.')
    
    try:
        cliente = transaccionar(Pagadores.actualizar, cliente)
    except Exception as ex:
        print(repr(ex))
        return template('xpdcobros/editar_cliente', usuario = usuario, organizacion = organizacion, cliente = cliente, lvl='danger', mensaje = 'Se ha producido un error al momento de actualizar el cliente.')

    return template('xpd_usr/mensaje', lvl='success', mensaje = 'Cliente {0} actualizado exitosamente'.format(cliente['nombre']) , href='/xpdcobros/usuarios/organizacion/{0}/cliente/{1}'.format(organizacion['id'], cliente['id']) )   

def servir_orden_pago(id_orden_pago):
    usuario = xpd_usr.getCurrentUser(request)
    
    con = orm.Conexion(PATH_BDD)
    orden_pago = OrdenesPago.getNamedQuery(con, 'findById', {'':id_orden_pago})
    if len(orden_pago) == 0:
        con.close()
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'Orden de Pago no disponible' , href='/')
    orden_pago = orden_pago[0]
    
    organizacion = Organizaciones.getNamedQuery(con, 'findById', {'id': orden_pago['id_organizacion'] })
    pagador = Pagadores.getNamedQuery(con, 'findById', {'id': orden_pago['id_pagador'] })
    if len(organizacion) == 0 or len(pagador) == 0:
        con.close()
        return template('xpd_usr/mensaje', lvl='danger', mensaje = 'Orden de Pago inconsistente' , href='/')
    organizacion = organizacion[0]
    pagador = pagador[0]
    cuentas = CuentasBcoOrganizacion.getNamedQuery(con,'findByOrganizacionActivo',{'id_organizacion':organizacion['id'], 'activo': 1})
    abonos = Abonos.getNamedQuery(con, 'findByOrdenpago', {'id_orden_pago':orden_pago['id']})
    con.close()

    abono = { 'id_organizacion':organizacion['id'], 'id_pagador':pagador['id'], 'id_orden_pago':orden_pago['id'], 
             'nombre_banco':'', 'tipo_cuenta':'', 'numero_cuenta':'', 'id_imagen':-1, 
             'fecha_registro':datetime.datetime.now().isoformat(), 'fecha_transaccion':datetime.datetime.now().isoformat()[:10],
             'numero_transaccion':'', 'monto_registrado': orden_pago['monto_pendiente'], 
             'monto_aprobado': None, 'fecha_feedback': None, 'id_usuario_feedback':None, 'estado':'R', 'observaciones':None,
             }

    if request.method == 'GET':
        id_cta_bco = -1
        
        return template('xpdcobros/pagar_orden_pago', usuario = usuario, orden_pago = orden_pago, cobrador = organizacion, pagador = pagador, abonos = abonos, abono = abono, cuentas = cuentas, id_cta_bco = id_cta_bco, lvl = '', mensaje = '')

    # a partir de este punto se asumen POST
    accion = request.forms.get('accion','')
    id_cta_bco = int(request.forms.get('id_cta_bco','0'))
    for campo in ['id_imagen', 'numero_transaccion', 'fecha_transaccion','monto_registrado']:
        abono[campo] = request.forms.get(campo,'')

    if accion == 'Cambiar Imagen':
        path_temporal = None
        try:
            file_imagen = request.files.get('file_imagen')
            if not file_imagen:
                raise Exception('No hay archivo de imagen registrado')
            path_temporal = join(abspath(dirname(__file__)), 'upload' , str(uuid4()) + '_' + file_imagen.filename )
            file_imagen.save(path_temporal)
            print("Se genera archivo temporal {0}".format(path_temporal))
            imagen = {'nombre': file_imagen.filename, 'tipo':'', 'contenido':None, 'path_archivo':None, 'transcripcion': None, 'id_usuario': None if usuario is None else usuario['id'], }
            if orm.DEBUG_MODE:
                print(repr(imagen))
            # Procesa la extension
            extension = file_imagen.filename.lower().split('.')[-1]
            if extension == 'png':
                imagen['tipo'] = 'image/png'
            elif extension in ['jpg','jpeg']:
                imagen['tipo'] = 'image/jpeg'
            elif extension in ['pdf']:
                imagen['tipo'] = 'application/pdf'
            else:
                raise Exception('El formato del archivo no es aceptado por la aplicación.')
            if orm.DEBUG_MODE:
                print("Se identifica tipo " + imagen['tipo'] )
            # Extrae el contenido
            with open(path_temporal, 'rb') as stream_temporal:
                imagen['contenido'] = stream_temporal.read()
            transaccionar(Imagenes.insertar, imagen)
            abono['id_imagen'] = imagen['id']
        except Exception as ex:
            print(repr(ex))
            return template('xpdcobros/pagar_orden_pago', usuario = usuario, orden_pago = orden_pago, cobrador = organizacion, pagador = pagador, abonos = abonos, abono = abono, cuentas = cuentas, id_cta_bco = id_cta_bco, lvl = 'danger', mensaje = 'Se presentó un error en la carga del archivo')
        finally:
            if path_temporal and exists(path_temporal): 
                remove_file(path_temporal)
                print("Se elimina archivo temporal {0}".format(path_temporal))

    elif accion.startswith("Registrar Abono"):

        # valida las entradas
        observaciones = []        
        if abono['id_imagen'] == "-1":
            observaciones.append('Se debe cargar una imagen correspondiente a la Constancia de la Transacción.')
        if id_cta_bco == 0:
            observaciones.append("Debe seleccionar una de las cuentas Destino disponibles")
        if len(abono['numero_transaccion']) == 0:
            observaciones.append('Se debe ingresar el numero de transacción correspondiente.')
        try:
            abono['fecha_transaccion'] = datetime.datetime.fromisoformat(abono['fecha_transaccion'])
        except:
            observaciones.append("La fecha de transacción debe estar en formato AAAA-MM-DD")
        try:
            abono['monto_registrado'] = float(abono['monto_registrado'])
            if abono['monto_registrado'] > orden_pago['monto_pendiente']:
                raise Exception("El monto supera el pendiente")
        except:
            observaciones.append("El monto registrado no es válido")        
        if len(observaciones) > 0:
            return template('xpdcobros/pagar_orden_pago', usuario = usuario, orden_pago = orden_pago, cobrador = organizacion, pagador = pagador, abonos = abonos, abono = abono, cuentas = cuentas, id_cta_bco = id_cta_bco, lvl = 'danger', mensaje = '- {0}'.format("\n- ".join(observaciones) ))
        
        # Llena campos de cuenta bancaria
        cuenta = [x for x in cuentas if x['id'] == id_cta_bco][0]
        for campo in ['nombre_banco','tipo_cuenta','numero_cuenta']:
            abono[campo] = cuenta[campo]

        # Realiza registro de abono
        try:
            transaccionar(Abonos.insertar, abono)
        except Exception as ex:
            print(repr(ex))
            return template('xpdcobros/pagar_orden_pago', usuario = usuario, orden_pago = orden_pago, cobrador = organizacion, pagador = pagador, abonos = abonos, abono = abono, cuentas = cuentas, id_cta_bco = id_cta_bco, lvl = 'danger', mensaje = 'Se ha producido un error al registrar el abono.')
        
        # Vuelve a consultar lista de abonos
        abonos = consultar(Abonos,'findByOrdenpago',{'id_orden_pago':orden_pago['id']})

        return template('xpdcobros/pagar_orden_pago', usuario = usuario, orden_pago = orden_pago, cobrador = organizacion, pagador = pagador, abonos = abonos, abono = abono, cuentas = cuentas, id_cta_bco = id_cta_bco, lvl = 'success', mensaje = 'El Abono ha sido registrado Exitosamente.')
    return template('xpdcobros/pagar_orden_pago', usuario = usuario, orden_pago = orden_pago, cobrador = organizacion, pagador = pagador, abonos = abonos, abono = abono, cuentas = cuentas, id_cta_bco = id_cta_bco, lvl = 'warning', mensaje = 'Por favor completar la información de la Transferencia antes de proceder con el registro.')

# Ruteos hacia Bottle
def rutearModulo( app : Bottle, ruta_base : str ):
    # encapsula Session Middleware
    CONFIG['root'] = ruta_base

    app.route( ruta_base + '/usuarios/solicitudcobrador/crear' , method = ['GET', 'POST'])(servir_usr_solicitar_organizacion)
    app.route( ruta_base + '/usuarios/pagos_pendientes' , method = ['GET'])(servir_usr_listar_pagos_pendientes)

    app.route( ruta_base + '/organizacion/<uuid_organizacion>/pagador/<email_pagador>/pagos_pendientes' , method = ['GET'])(servir_cob_listar_pagos_pendientes)    
    
    app.route( ruta_base + '/usuarios/organizacion/<id_organizacion>/cuentasbco/crear' , method = ['GET', 'POST'])(servir_usr_crear_cuenta)
    app.route( ruta_base + '/usuarios/organizacion/<id_organizacion>/cuentasbco/<id_cta_bco>' , method = ['GET', 'POST'])(servir_usr_editar_cuenta)
    
    app.route( ruta_base + '/usuarios/organizacion/<id_organizacion>/cliente/crear' , method = ['GET', 'POST'])(servir_usr_crear_pagador)
    app.route( ruta_base + '/usuarios/organizacion/<id_organizacion>/cliente/<id_pagador>' , method = ['GET', 'POST'])(servir_usr_editar_pagador)

    app.route( ruta_base + '/usuarios/organizacion/<id_organizacion>' , method = ['GET', 'POST'])(servir_usr_editar_organizacion)

    app.route( ruta_base + '/usuarios/organizacion' , method = ['GET'])(servir_api_main)

    app.route( ruta_base + '/imagenes/<id_imagen>' , method = ['GET', 'POST'])(servir_imagen)

    app.route( ruta_base + '/admin/config' , method = ['GET','POST'])(servir_admin_lista_config)

    app.route( ruta_base + '/ordenes_pago/<id_orden_pago>' , method = ['GET','POST'])(servir_orden_pago)
    
    # app.route( ruta_base + '/admin/cobradores' , method = ['GET'])(servir_admin_listar_cobradores)
    # app.route( ruta_base + '/admin/organizacion/<id_organizacion>' , method = ['GET', 'POST'])(servir_admin_editar_cobrador)
    # app.route( ruta_base + '/admin/cobrador' , method = ['GET','POST'])(servir_admin_nuevo_cobrador)

    # app.route( ruta_base + '/admin/abonos/<id_abono>' , method = ['GET', 'POST'])(servir_gestionar_abono)
    # app.route( ruta_base + '/admin/abonos' , method = ['GET'])(servir_cola_abonos)


    # app.route( ruta_base + '/usuarios/organizacion/<id_organizacion>/cuentasbco' , method = ['GET'])(servir_usr_listar_cuentas)

    # app.route( ruta_base + '/usuario/organizacion/<id_organizacion>/ordenespago' , method = ['GET'])(servir_usr_listar_ordenes_pago)
    # app.route( ruta_base + '/usuario/organizacion/<id_organizacion>/ordenespago/cargar' , method = ['GET','POST'])(servir_usr_cargar_ordenes_pago)
    # app.route( ruta_base + '/usuario/organizacion/<id_organizacion>/ordenespago/crear' , method = ['GET','POST'])(servir_usr_crear_orden_pago)
    # app.route( ruta_base + '/usuario/organizacion/<id_organizacion>/ordenespago/<id_orden_pago>' , method = ['GET','POST'])(servir_usr_editar_orden_pago)

    # app.route( ruta_base + '/usuario/organizacion/<id_organizacion>/pagadores' , method = ['GET'])(servir_usr_listar_pagadores)
    # app.route( ruta_base + '/usuario/organizacion/<id_organizacion>/pagador/<id_pagador>' , method = ['GET', 'POST'])(servir_usr_ver_pagador)


