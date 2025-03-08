import xpd_orm as orm
from os.path import abspath , dirname, join, exists
from os import makedirs
from os import remove as remove_file

from bottle import run, debug, route, abort, static_file, template, request, response, redirect
from bottle import Bottle
import datetime

import xpd_usr

PATH_BDD = dirname(abspath(__file__)) + "/data/xpd_alicuotas.db"
CONFIG = {'rutas': []}

import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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


Condominios = orm.Entidad()
Condominios.setMetamodelo({
    'nombreTabla' : 'CONDOMINIO',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'nombre', 'nombreCampo':'NOMBRE', 'tipo':orm.XPDSTRING, 'tamano':64, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'saldo', 'nombreCampo':'SALDO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_user', 'nombreCampo':'ID_USER', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByUser', 'whereClause':['id_user'], },
        ]
    })

Departamentos = orm.Entidad()
Departamentos.setMetamodelo({
    'nombreTabla' : 'DEPARTAMENTO',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'numero_dep', 'nombreCampo':'NUMERO_DEP', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'propietario', 'nombreCampo':'PROPIETARIO', 'tipo':orm.XPDSTRING, 'tamano':64, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'arrendatario', 'nombreCampo':'ARRENDATARIO', 'tipo':orm.XPDSTRING, 'tamano':64, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'saldo', 'nombreCampo':'SALDO', 'tipo':orm.XPDREAL, 'tamano': 5, 'precision': 2, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_condominio', 'nombreCampo':'ID_CONDOMINIO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByCondominio', 'whereClause':['id_condominio'], },
        ]
    })

Transaccions = orm.Entidad()
Transaccions.setMetamodelo({
    'nombreTabla' : 'TRANSACCION',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'fecha', 'nombreCampo':'FECHA', 'tipo':orm.XPDDATE, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'concepto', 'nombreCampo':'CONCEPTO', 'tipo':orm.XPDSTRING, 'tamano':256, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'monto', 'nombreCampo':'MONTO', 'tipo':orm.XPDREAL, 'tamano': 7, 'precision': 2, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'saldo_antes', 'nombreCampo':'SALDO_ANTES', 'tipo':orm.XPDREAL, 'tamano': 6, 'precision': 2, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'saldo_despues', 'nombreCampo':'SALDO_DESPUES', 'tipo':orm.XPDREAL, 'tamano': 6, 'precision': 2, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'anulado', 'nombreCampo':'ANULADO', 'tipo':orm.XPDBOOLEAN, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_abono', 'nombreCampo':'ID_ABONO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'id_egreso', 'nombreCampo':'ID_EGRESO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'id_condominio', 'nombreCampo':'ID_CONDOMINIO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByCondominio', 'whereClause':['id_condominio'], },
        ]
    })

Egresos = orm.Entidad()
Egresos.setMetamodelo({
    'nombreTabla' : 'EGRESO',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'fecha', 'nombreCampo':'FECHA', 'tipo':orm.XPDDATE, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'destino', 'nombreCampo':'DESTINO', 'tipo':orm.XPDSTRING, 'tamano':128, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'monto', 'nombreCampo':'MONTO', 'tipo':orm.XPDREAL, 'tamano': 6, 'precision': 2, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'observaciones', 'nombreCampo':'OBSERVACIONES', 'tipo':orm.XPDSTRING, 'tamano':256, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'anulado', 'nombreCampo':'ANULADO', 'tipo':orm.XPDBOOLEAN, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_condominio', 'nombreCampo':'ID_CONDOMINIO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByCondominio', 'whereClause':['id_condominio'], 'orderBy':['fecha']},
        ]
    })

Alicuotas = orm.Entidad()
Alicuotas.setMetamodelo({
    'nombreTabla' : 'ALICUOTA',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'anio', 'nombreCampo':'ANIO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'mes', 'nombreCampo':'MES', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'monto', 'nombreCampo':'MONTO', 'tipo':orm.XPDREAL, 'tamano': 5, 'precision': 2, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'monto_pendiente', 'nombreCampo':'MONTO_PENDIENTE', 'tipo':orm.XPDREAL, 'tamano': 5, 'precision': 2, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'pagado', 'nombreCampo':'PAGADO', 'tipo':orm.XPDBOOLEAN, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'observaciones', 'nombreCampo':'OBSERVACIONES', 'tipo':orm.XPDSTRING, 'tamano':256, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_departamento', 'nombreCampo':'ID_DEPARTAMENTO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByDepartamento', 'whereClause':['id_departamento'], 'orderBy':['anio', 'mes']},
        ]
    })

Abonos = orm.Entidad()
Abonos.setMetamodelo({
    'nombreTabla' : 'ABONO',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'fecha', 'nombreCampo':'FECHA', 'tipo':orm.XPDDATE, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'monto', 'nombreCampo':'MONTO', 'tipo':orm.XPDREAL, 'tamano': 5, 'precision': 2, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'monto_aprobado', 'nombreCampo':'MONTO_APROBADO', 'tipo':orm.XPDREAL, 'tamano': 5, 'precision': 2, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'monto_por_aplicar', 'nombreCampo':'MONTO_POR_APLICAR', 'tipo':orm.XPDREAL, 'tamano': 5, 'precision': 2, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'observacion', 'nombreCampo':'OBSERVACION', 'tipo':orm.XPDSTRING, 'tamano':256, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'genera_egreso', 'nombreCampo':'GENERA_EGRESO', 'tipo':orm.XPDBOOLEAN, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'aplicado', 'nombreCampo':'APLICADO', 'tipo':orm.XPDBOOLEAN, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'aplicado_saldo', 'nombreCampo':'APLICADO_SALDO', 'tipo':orm.XPDBOOLEAN, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_egreso', 'nombreCampo':'ID_EGRESO', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_departamento', 'nombreCampo':'ID_DEPARTAMENTO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByDepartamento', 'whereClause':['id_departamento'], 'orderBy':['fecha'] },
        ]
    })

EventoLimpezaAlicuotas = orm.Entidad()
EventoLimpezaAlicuotas.setMetamodelo({
    'nombreTabla' : 'ABONO_ALICUOTA',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'id_alicuota', 'nombreCampo':'ID_ALICUOTA', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'monto', 'nombreCampo':'MONTO', 'tipo':orm.XPDREAL, 'tamano': 5, 'precision': 2, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'id_abono', 'nombreCampo':'ID_ABONO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'fkAlicuota', 'whereClause':['id_alicuota'], },
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByAbono', 'whereClause':['id_abono'], },
        ]
    })


def inicializar():
    entidades = [Condominios, Departamentos, Transaccions, Egresos, Alicuotas, Abonos, EventoLimpezaAlicuotas]
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
    

def condominio_getowner(conexion, id_condominio):
    objeto = Condominios.getNamedQuery(conexion, 'findById', {'id': id_condominio})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, objeto['id_user'])

def departamento_getowner(conexion, id_departamento):
    objeto = Departamentos.getNamedQuery(conexion, 'findById', {'id': id_departamento})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, condominio_getowner(conexion, objeto['id_condominio'])[1] )

def transaccion_getowner(conexion, id_transaccion):
    objeto = Transaccions.getNamedQuery(conexion, 'findById', {'id': id_transaccion})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, condominio_getowner(conexion, objeto['id_condominio'])[1] )

def egreso_getowner(conexion, id_egreso):
    objeto = Egresos.getNamedQuery(conexion, 'findById', {'id': id_egreso})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, condominio_getowner(conexion, objeto['id_condominio'])[1] )

def alicuota_getowner(conexion, id_alicuota):
    objeto = Alicuotas.getNamedQuery(conexion, 'findById', {'id': id_alicuota})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, departamento_getowner(conexion, objeto['id_departamento'])[1] )

def abono_getowner(conexion, id_abono):
    objeto = Abonos.getNamedQuery(conexion, 'findById', {'id': id_abono})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, departamento_getowner(conexion, objeto['id_departamento'])[1] )

def eventolimpezaalicuota_getowner(conexion, id_eventolimpezaalicuota):
    objeto = EventoLimpezaAlicuotas.getNamedQuery(conexion, 'findById', {'id': id_eventolimpezaalicuota})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, abono_getowner(conexion, objeto['id_abono'])[1] )

def servir_page_editar_condominio(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    condominio, id_usuario_owner = condominio_getowner( conexion , id)
    conexion.close()
    if condominio is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_Condominio", objeto = condominio, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/condominios/" + str(condominio['id']), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    condominio["nombre"] = request.forms.get( "nombre", "").strip()
        
    if len(condominio["nombre"]) == 0:
        mensajes_error.append("nombre es requerido")

    if len(condominio["nombre"]) > 64:
        mensajes_error.append("El tamaño de nombre excede el permitido")

    condominio["saldo"] = request.forms.get( "saldo", "").strip()
        
    if len(condominio["saldo"]) == 0:
        mensajes_error.append("saldo es requerido")

    try:
        condominio["saldo"] = int( condominio["saldo"] )
    except:
        mensajes_error.append("El valor de saldo no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_Condominio", objeto = condominio, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/condominios/" + str(condominio['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Condominios.actualizar, condominio)
    except:
        return template("xpd_alicuotas/editar_Condominio", objeto = condominio, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/condominios/" + str(condominio['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_alicuotas/editar_Condominio", objeto = condominio, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_alicuotas/condominios/" + str(condominio['id']), fecha_iso_to_js = fecha_iso_to_js )

CONFIG['rutas'].append({'ruta':'/condominios/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_condominio })

def servir_page_insertar_condominio():

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    condominio = Condominios.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_Condominio", objeto = condominio, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/condominios", fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    condominio['id_user'] = usuario['id']

    condominio["nombre"] = request.forms.get( "nombre", "").strip()
        
    if len(condominio["nombre"]) == 0:
        mensajes_error.append("nombre es requerido")

    if len(condominio["nombre"]) > 64:
        mensajes_error.append("El tamaño de nombre excede el permitido")

    condominio["saldo"] = request.forms.get( "saldo", "").strip()
        
    if len(condominio["saldo"]) == 0:
        mensajes_error.append("saldo es requerido")

    try:
        condominio["saldo"] = int( condominio["saldo"] )
    except:
        mensajes_error.append("El valor de saldo no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_Condominio", objeto = condominio, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/condominios", fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Condominios.insertar, condominio)
    except:
        return template("xpd_alicuotas/editar_Condominio", objeto = condominio, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/condominios", fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/condominios/" + str(condominio['id']) )

CONFIG['rutas'].append({'ruta':'/condominios/nuevo', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_condominio })

def servir_page_eliminar_condominio(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    condominio, id_usuario_owner = condominio_getowner( conexion , id)
    conexion.close()
    if condominio is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method != "GET":
        abort( 404, "Metodo no Valido" )
    try:
        transaccionar(Condominios.eliminar, condominio)
    except:
    
        return template("xpd_usr/mensaje", lvl = "danger", mensaje = "Error al eliminar objeto.", href ="/xpd_alicuotas/condominios" )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/condominios" )
    
CONFIG['rutas'].append({'ruta':'/condominios/<id>/eliminar', 'metodos':['GET','POST'], 'funcion': servir_page_eliminar_condominio })

def servir_page_get_condominio_lista():
    conexion = orm.Conexion(PATH_BDD)

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    
    conexion = orm.Conexion(PATH_BDD)

    lista = Condominios.getNamedQuery(conexion, 'findByUser', {'id_user':usuario['id']})

    conexion.close()

    return template("xpd_alicuotas/listar_Condominio", lista = lista, usuario = usuario)
    
CONFIG['rutas'].append({'ruta':'/condominios', 'metodos':['GET'], 'funcion': servir_page_get_condominio_lista })

def servir_page_get_condominio_byid(id_condominio):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    

    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = condominio_getowner(conexion, id_condominio)
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    
    departamentos = Departamentos.getNamedQuery( conexion, "findByCondominio", {'id_condominio':objeto['id']} )

    transaccions = Transaccions.getNamedQuery( conexion, "findByCondominio", {'id_condominio':objeto['id']} )

    egresos = Egresos.getNamedQuery( conexion, "findByCondominio", {'id_condominio':objeto['id']} )

    conexion.close()
    return template("xpd_alicuotas/show_condominio", objeto = objeto, usuario = usuario , departamentos = departamentos, transaccions = transaccions, egresos = egresos)

CONFIG['rutas'].append({'ruta':'/condominios/<id_condominio>', 'metodos':['GET'], 'funcion': servir_page_get_condominio_byid })

def servir_page_graficar_condominio(id_condominio):

    con = orm.Conexion(PATH_BDD)
    
    # Obtiene datos de Departamentos 
    departamentos = Departamentos.getNamedQuery(con, 'findByCondominio', {'id_condominio':id_condominio}) 
    df_departamentos = pd.DataFrame(departamentos)
    
    # Obtiene datos de Alicuotas
    sql = """SELECT a.id as id, a.anio as anio, a.mes as mes, a.monto as monto, a.monto_pendiente as monto_pendiente, a.pagado as pagado, a.observaciones as observaciones, a.id_departamento as id_departamento 
, ( SELECT count(1) from ABONO_ALICUOTA b, ABONO c, EGRESO d where b.id_alicuota = a.id and c.id = b.id_abono and d.id = c.id_egreso ) as conteo_egresos
FROM ALICUOTA a , DEPARTAMENTO b 
WHERE b.id_condominio = :id_condominio and a.id_departamento = b.id"""
    alicuotas = con.consultar(sql,{"id_condominio":id_condominio},["id", "anio", "mes", "monto", "monto_pendiente", "pagado", "observaciones", "id_departamento", "conteo_egresos"])
    df_alicuotas = pd.DataFrame(alicuotas)

    # Obtiene datos de Egresos
    sql = """SELECT a.id as id, a.fecha as fecha, a.destino as destino, a.monto as monto, a.observaciones as observaciones, a.anulado as anulado, a.id_condominio as id_condominio 
, b.monto_por_aplicar as monto_por_aplicar
, c.id as id_departamento, c.numero_dep as numero_dep
FROM EGRESO a, ABONO b, DEPARTAMENTO c
WHERE a.id_condominio = :id_condominio and a.anulado = '0' and b.id_egreso = a.id and b.id_departamento = c.id """
    egresos = con.consultar(sql,{'id_condominio':id_condominio},[ "id", "fecha", "destino", "monto", "observaciones", "anulado", "id_condominio", "monto_por_aplicar", "id_departamento", "numero_dep" ])
    df_egresos = pd.DataFrame(egresos)

    con.close()

    # Define Rango de Meses y define data para despliegue
    meses = set()
    for indice in df_alicuotas.index:
        df_alicuotas.loc[indice,'aniomes'] = f"{df_alicuotas.loc[indice,'anio']}-{df_alicuotas.loc[indice,'mes']:02d}"
        if df_alicuotas.loc[indice, 'aniomes'] not in meses:
            meses.add(df_alicuotas.loc[indice,'aniomes'])
            
        df_alicuotas.loc[indice,'color'] = 'green' 
        if df_alicuotas.loc[indice,'pagado'] == '0':
            df_alicuotas.loc[indice,'color'] = 'red' 
        elif df_alicuotas.loc[indice,'conteo_egresos'] > 0:
            df_alicuotas.loc[indice,'color'] = 'orange' 
        
    for indice in df_egresos.index:
        df_egresos.loc[indice, 'aniomes'] = df_egresos.loc[indice, 'fecha'][:7]
        if df_egresos.loc[indice, 'aniomes'] not in meses:
            meses.add(df_egresos.loc[indice, 'aniomes'])
        
        df_egresos.loc[indice, 'color'] = "#44FF44"
        if df_egresos.loc[indice, 'monto_por_aplicar'] > 0:
                df_egresos.loc[indice, 'color'] = "#FFFF00"
                
    meses = list(meses)
    meses.sort()

    for indice in df_alicuotas.index:    
        df_alicuotas.loc[indice,'aniomes_x'] = meses.index(df_alicuotas.loc[indice,'aniomes'])
    for indice in df_egresos.index:    
        df_egresos.loc[indice,'aniomes_x'] = meses.index(df_egresos.loc[indice,'aniomes'])

    # Genera Gráfica y la guarda en archivo
    ancho_pulgadas = 10
    alto_pulgadas = 5
    dpi = 100

    fig, ax = plt.subplots(figsize=(ancho_pulgadas, alto_pulgadas), dpi=dpi)

    ax.set_title(f"Pago Alicuotas ({datetime.datetime.now().isoformat()})")
    ax.set_label("Mes")

    yticks = [x for x in range(-1,-7,-1)]
    ylabels = [f"Dep. {-x}" for x in yticks]
    xlabels = [meses[0]] + [ x for x in meses if x.endswith('-01') ] + [meses[-1]]
    xticks = [ meses.index(x) for x in xlabels]
    ax.set_xticks(xticks, xlabels, rotation=90)
    ax.set_yticks(yticks, ylabels)

    ax.scatter( df_alicuotas['aniomes_x'], df_alicuotas['id_departamento'] * -1, c = df_alicuotas['color'], s = df_alicuotas['monto'] * 3.0 )
    ax.scatter( df_egresos['aniomes_x'], df_egresos['id_departamento'] * -1 - 0.2, c = df_egresos['color'], s = df_egresos['monto'] * 3.0 )

    plt.savefig(dirname(abspath(__file__)) + f"/static/graficas/alicuotas_{id_condominio}.png")

    # retorno
    return "OK"

CONFIG['rutas'].append({'ruta':'/condominios/<id_condominio>/graficar', 'metodos':['GET'], 'funcion': servir_page_graficar_condominio })

def servir_page_editar_departamento(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    departamento, id_usuario_owner = departamento_getowner( conexion , id)
    conexion.close()
    if departamento is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_Departamento", objeto = departamento, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/departamentos/" + str(departamento['id']), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    departamento["numero_dep"] = request.forms.get( "numero_dep", "").strip()
        
    if len(departamento["numero_dep"]) == 0:
        mensajes_error.append("numero_dep es requerido")

    try:
        departamento["numero_dep"] = int( departamento["numero_dep"] )
    except:
        mensajes_error.append("El valor de numero_dep no es válido")

    departamento["propietario"] = request.forms.get( "propietario", "").strip()
        
    if len(departamento["propietario"]) == 0:
        mensajes_error.append("propietario es requerido")

    if len(departamento["propietario"]) > 64:
        mensajes_error.append("El tamaño de propietario excede el permitido")

    departamento["arrendatario"] = request.forms.get( "arrendatario", "").strip()
        
    if len(departamento["arrendatario"]) > 64:
        mensajes_error.append("El tamaño de arrendatario excede el permitido")

    departamento["saldo"] = request.forms.get( "saldo", "").strip()
        
    if len(departamento["saldo"]) == 0:
        mensajes_error.append("saldo es requerido")

    try:
        departamento["saldo"] = float( departamento["saldo"] )
    except:
        mensajes_error.append("El valor de saldo no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_Departamento", objeto = departamento, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/departamentos/" + str(departamento['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Departamentos.actualizar, departamento)
    except:
        return template("xpd_alicuotas/editar_Departamento", objeto = departamento, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/departamentos/" + str(departamento['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_alicuotas/editar_Departamento", objeto = departamento, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_alicuotas/departamentos/" + str(departamento['id']), fecha_iso_to_js = fecha_iso_to_js )

CONFIG['rutas'].append({'ruta':'/departamentos/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_departamento })

def servir_page_insertar_departamento(id_condominio):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    condominio, id_usuario_owner = condominio_getowner( conexion , id_condominio)
    conexion.close()
    if condominio is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )

    departamento = Departamentos.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_Departamento", objeto = departamento, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/condominios/" + str(id_condominio), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    departamento['id_condominio'] = id_condominio

    departamento["numero_dep"] = request.forms.get( "numero_dep", "").strip()
        
    if len(departamento["numero_dep"]) == 0:
        mensajes_error.append("numero_dep es requerido")

    try:
        departamento["numero_dep"] = int( departamento["numero_dep"] )
    except:
        mensajes_error.append("El valor de numero_dep no es válido")

    departamento["propietario"] = request.forms.get( "propietario", "").strip()
        
    if len(departamento["propietario"]) == 0:
        mensajes_error.append("propietario es requerido")

    if len(departamento["propietario"]) > 64:
        mensajes_error.append("El tamaño de propietario excede el permitido")

    departamento["arrendatario"] = request.forms.get( "arrendatario", "").strip()
        
    if len(departamento["arrendatario"]) > 64:
        mensajes_error.append("El tamaño de arrendatario excede el permitido")

    departamento["saldo"] = request.forms.get( "saldo", "").strip()
        
    if len(departamento["saldo"]) == 0:
        mensajes_error.append("saldo es requerido")

    try:
        departamento["saldo"] = float( departamento["saldo"] )
    except:
        mensajes_error.append("El valor de saldo no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_Departamento", objeto = departamento, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/condominios/" + str(id_condominio), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Departamentos.insertar, departamento)
    except:
        return template("xpd_alicuotas/editar_Departamento", objeto = departamento, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/condominios/" + str(id_condominio), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/departamentos/" + str(departamento['id']) )

CONFIG['rutas'].append({'ruta':'/condominios/<id_condominio>/nuevodepartamento', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_departamento })

def servir_page_eliminar_departamento(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    departamento, id_usuario_owner = departamento_getowner( conexion , id)
    conexion.close()
    if departamento is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method != "GET":
        abort( 404, "Metodo no Valido" )
    try:
        transaccionar(Departamentos.eliminar, departamento)
    except:
    
        return template("xpd_usr/mensaje", lvl = "danger", mensaje = "Error al eliminar objeto.", href ="/xpd_alicuotas/Condominios/" + str(departamento['id_Condominio']) )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/Condominios/" + str(departamento['id_Condominio']) )
    
CONFIG['rutas'].append({'ruta':'/departamentos/<id>/eliminar', 'metodos':['GET','POST'], 'funcion': servir_page_eliminar_departamento })

def servir_page_get_departamento_byid(id_departamento):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    

    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = departamento_getowner(conexion, id_departamento)
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    
    alicuotas = Alicuotas.getNamedQuery( conexion, "findByDepartamento", {'id_departamento':objeto['id']} )
    alicuotas.reverse()
    abonos = Abonos.getNamedQuery( conexion, "findByDepartamento", {'id_departamento':objeto['id']} )

    conexion.close()
    return template("xpd_alicuotas/show_departamento", objeto = objeto, usuario = usuario , alicuotas = alicuotas, abonos = abonos)

CONFIG['rutas'].append({'ruta':'/departamentos/<id_departamento>', 'metodos':['GET'], 'funcion': servir_page_get_departamento_byid })

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
        return template("xpd_alicuotas/editar_Transaccion", objeto = transaccion, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/transaccions/" + str(transaccion['id']), fecha_iso_to_js = fecha_iso_to_js)
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

    transaccion["concepto"] = request.forms.get( "concepto", "").strip()
        
    if len(transaccion["concepto"]) == 0:
        mensajes_error.append("concepto es requerido")

    if len(transaccion["concepto"]) > 256:
        mensajes_error.append("El tamaño de concepto excede el permitido")

    transaccion["monto"] = request.forms.get( "monto", "").strip()
        
    if len(transaccion["monto"]) == 0:
        mensajes_error.append("monto es requerido")

    try:
        transaccion["monto"] = float( transaccion["monto"] )
    except:
        mensajes_error.append("El valor de monto no es válido")

    transaccion["saldo_antes"] = request.forms.get( "saldo_antes", "").strip()
        
    if len(transaccion["saldo_antes"]) == 0:
        mensajes_error.append("saldo_antes es requerido")

    try:
        transaccion["saldo_antes"] = float( transaccion["saldo_antes"] )
    except:
        mensajes_error.append("El valor de saldo_antes no es válido")

    transaccion["saldo_despues"] = request.forms.get( "saldo_despues", "").strip()
        
    if len(transaccion["saldo_despues"]) == 0:
        mensajes_error.append("saldo_despues es requerido")

    try:
        transaccion["saldo_despues"] = float( transaccion["saldo_despues"] )
    except:
        mensajes_error.append("El valor de saldo_despues no es válido")

    transaccion["anulado"] = request.forms.get( "anulado", "").strip()
        
    transaccion["anulado"] = transaccion["anulado"] == "1"

    transaccion["id_abono"] = request.forms.get( "id_abono", "").strip()
        
    try:
        transaccion["id_abono"] = int( transaccion["id_abono"] )
    except:
        mensajes_error.append("El valor de id_abono no es válido")

    transaccion["id_egreso"] = request.forms.get( "id_egreso", "").strip()
        
    try:
        transaccion["id_egreso"] = int( transaccion["id_egreso"] )
    except:
        mensajes_error.append("El valor de id_egreso no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_Transaccion", objeto = transaccion, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/transaccions/" + str(transaccion['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Transaccions.actualizar, transaccion)
    except:
        return template("xpd_alicuotas/editar_Transaccion", objeto = transaccion, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/transaccions/" + str(transaccion['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_alicuotas/editar_Transaccion", objeto = transaccion, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_alicuotas/transaccions/" + str(transaccion['id']), fecha_iso_to_js = fecha_iso_to_js )

CONFIG['rutas'].append({'ruta':'/transaccions/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_transaccion })

def servir_page_insertar_transaccion(id_condominio):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    condominio, id_usuario_owner = condominio_getowner( conexion , id_condominio)
    conexion.close()
    if condominio is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )

    transaccion = Transaccions.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_Transaccion", objeto = transaccion, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/condominios/" + str(id_condominio), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    transaccion['id_condominio'] = id_condominio

    transaccion["fecha"] = request.forms.get( "fecha", "").strip()
        
    if len(transaccion["fecha"]) == 0:
        mensajes_error.append("fecha es requerido")

    transaccion["concepto"] = request.forms.get( "concepto", "").strip()
        
    if len(transaccion["concepto"]) == 0:
        mensajes_error.append("concepto es requerido")

    if len(transaccion["concepto"]) > 256:
        mensajes_error.append("El tamaño de concepto excede el permitido")

    transaccion["monto"] = request.forms.get( "monto", "").strip()
        
    if len(transaccion["monto"]) == 0:
        mensajes_error.append("monto es requerido")

    try:
        transaccion["monto"] = float( transaccion["monto"] )
    except:
        mensajes_error.append("El valor de monto no es válido")

    transaccion["saldo_antes"] = request.forms.get( "saldo_antes", "").strip()
        
    if len(transaccion["saldo_antes"]) == 0:
        mensajes_error.append("saldo_antes es requerido")

    try:
        transaccion["saldo_antes"] = float( transaccion["saldo_antes"] )
    except:
        mensajes_error.append("El valor de saldo_antes no es válido")

    transaccion["saldo_despues"] = request.forms.get( "saldo_despues", "").strip()
        
    if len(transaccion["saldo_despues"]) == 0:
        mensajes_error.append("saldo_despues es requerido")

    try:
        transaccion["saldo_despues"] = float( transaccion["saldo_despues"] )
    except:
        mensajes_error.append("El valor de saldo_despues no es válido")

    transaccion["anulado"] = request.forms.get( "anulado", "").strip()
        
    transaccion["anulado"] = transaccion["anulado"] == "1"

    transaccion["id_abono"] = request.forms.get( "id_abono", "").strip()
        
    try:
        transaccion["id_abono"] = int( transaccion["id_abono"] )
    except:
        mensajes_error.append("El valor de id_abono no es válido")

    transaccion["id_egreso"] = request.forms.get( "id_egreso", "").strip()
        
    try:
        transaccion["id_egreso"] = int( transaccion["id_egreso"] )
    except:
        mensajes_error.append("El valor de id_egreso no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_Transaccion", objeto = transaccion, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/condominios/" + str(id_condominio), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Transaccions.insertar, transaccion)
    except:
        return template("xpd_alicuotas/editar_Transaccion", objeto = transaccion, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/condominios/" + str(id_condominio), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/transaccions/" + str(transaccion['id']) )

CONFIG['rutas'].append({'ruta':'/condominios/<id_condominio>/nuevotransaccion', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_transaccion })

def servir_page_eliminar_transaccion(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    transaccion, id_usuario_owner = transaccion_getowner( conexion , id)
    conexion.close()
    if transaccion is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method != "GET":
        abort( 404, "Metodo no Valido" )
    try:
        transaccionar(Transaccions.eliminar, transaccion)
    except:
    
        return template("xpd_usr/mensaje", lvl = "danger", mensaje = "Error al eliminar objeto.", href ="/xpd_alicuotas/Condominios/" + str(transaccion['id_Condominio']) )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/Condominios/" + str(transaccion['id_Condominio']) )
    
CONFIG['rutas'].append({'ruta':'/transaccions/<id>/eliminar', 'metodos':['GET','POST'], 'funcion': servir_page_eliminar_transaccion })

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
    return template("xpd_alicuotas/show_transaccion", objeto = objeto, usuario = usuario )

CONFIG['rutas'].append({'ruta':'/transaccions/<id_transaccion>', 'metodos':['GET'], 'funcion': servir_page_get_transaccion_byid })

def servir_page_editar_egreso(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    egreso, id_usuario_owner = egreso_getowner( conexion , id)
    conexion.close()
    if egreso is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_Egreso", objeto = egreso, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/egresos/" + str(egreso['id']), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    egreso["fecha"] = request.forms.get( "fecha", "").strip()
        
    if len(egreso["fecha"]) == 0:
        mensajes_error.append("fecha es requerido")

    try:
        if len(egreso["fecha"]) > 0:
            egreso["fecha"] = fecha_js_to_iso(egreso["fecha"])
    except:
        mensajes_error.append("fecha no es una fecha válida")

    egreso["destino"] = request.forms.get( "destino", "").strip()
        
    if len(egreso["destino"]) == 0:
        mensajes_error.append("destino es requerido")

    if len(egreso["destino"]) > 128:
        mensajes_error.append("El tamaño de destino excede el permitido")

    egreso["monto"] = request.forms.get( "monto", "").strip()
        
    if len(egreso["monto"]) == 0:
        mensajes_error.append("monto es requerido")

    try:
        egreso["monto"] = float( egreso["monto"] )
    except:
        mensajes_error.append("El valor de monto no es válido")

    egreso["observaciones"] = request.forms.get( "observaciones", "").strip()
        
    if len(egreso["observaciones"]) == 0:
        mensajes_error.append("observaciones es requerido")

    if len(egreso["observaciones"]) > 256:
        mensajes_error.append("El tamaño de observaciones excede el permitido")

    egreso["anulado"] = request.forms.get( "anulado", "").strip()
        
    egreso["anulado"] = egreso["anulado"] == "1"

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_Egreso", objeto = egreso, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/egresos/" + str(egreso['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Egresos.actualizar, egreso)
    except:
        return template("xpd_alicuotas/editar_Egreso", objeto = egreso, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/egresos/" + str(egreso['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_alicuotas/editar_Egreso", objeto = egreso, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_alicuotas/egresos/" + str(egreso['id']), fecha_iso_to_js = fecha_iso_to_js )

CONFIG['rutas'].append({'ruta':'/egresos/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_egreso })

def servir_page_insertar_egreso(id_condominio):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    condominio, id_usuario_owner = condominio_getowner( conexion , id_condominio)
    conexion.close()
    if condominio is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )

    egreso = Egresos.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_Egreso", objeto = egreso, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/condominios/" + str(id_condominio), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    egreso['id_condominio'] = id_condominio

    egreso["fecha"] = request.forms.get( "fecha", "").strip()
        
    if len(egreso["fecha"]) == 0:
        mensajes_error.append("fecha es requerido")

    egreso["destino"] = request.forms.get( "destino", "").strip()
        
    if len(egreso["destino"]) == 0:
        mensajes_error.append("destino es requerido")

    if len(egreso["destino"]) > 128:
        mensajes_error.append("El tamaño de destino excede el permitido")

    egreso["monto"] = request.forms.get( "monto", "").strip()
        
    if len(egreso["monto"]) == 0:
        mensajes_error.append("monto es requerido")

    try:
        egreso["monto"] = float( egreso["monto"] )
    except:
        mensajes_error.append("El valor de monto no es válido")

    egreso["observaciones"] = request.forms.get( "observaciones", "").strip()
        
    if len(egreso["observaciones"]) == 0:
        mensajes_error.append("observaciones es requerido")

    if len(egreso["observaciones"]) > 256:
        mensajes_error.append("El tamaño de observaciones excede el permitido")

    egreso["anulado"] = request.forms.get( "anulado", "").strip()
        
    egreso["anulado"] = egreso["anulado"] == "1"

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_Egreso", objeto = egreso, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/condominios/" + str(id_condominio), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Egresos.insertar, egreso)
    except:
        return template("xpd_alicuotas/editar_Egreso", objeto = egreso, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/condominios/" + str(id_condominio), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/egresos/" + str(egreso['id']) )

CONFIG['rutas'].append({'ruta':'/condominios/<id_condominio>/nuevoegreso', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_egreso })

def servir_page_eliminar_egreso(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    egreso, id_usuario_owner = egreso_getowner( conexion , id)
    conexion.close()
    if egreso is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method != "GET":
        abort( 404, "Metodo no Valido" )
    try:
        transaccionar(Egresos.eliminar, egreso)
    except:
    
        return template("xpd_usr/mensaje", lvl = "danger", mensaje = "Error al eliminar objeto.", href ="/xpd_alicuotas/Condominios/" + str(egreso['id_Condominio']) )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/Condominios/" + str(egreso['id_Condominio']) )
    
CONFIG['rutas'].append({'ruta':'/egresos/<id>/eliminar', 'metodos':['GET','POST'], 'funcion': servir_page_eliminar_egreso })

def servir_page_get_egreso_byid(id_egreso):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    

    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = egreso_getowner(conexion, id_egreso)
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    
    conexion.close()
    return template("xpd_alicuotas/show_egreso", objeto = objeto, usuario = usuario )

CONFIG['rutas'].append({'ruta':'/egresos/<id_egreso>', 'metodos':['GET'], 'funcion': servir_page_get_egreso_byid })

def servir_page_editar_alicuota(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    alicuota, id_usuario_owner = alicuota_getowner( conexion , id)
    conexion.close()
    if alicuota is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_Alicuota", objeto = alicuota, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/alicuotas/" + str(alicuota['id']), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    alicuota["anio"] = request.forms.get( "anio", "").strip()
        
    if len(alicuota["anio"]) == 0:
        mensajes_error.append("anio es requerido")

    try:
        alicuota["anio"] = int( alicuota["anio"] )
    except:
        mensajes_error.append("El valor de anio no es válido")

    alicuota["mes"] = request.forms.get( "mes", "").strip()
        
    if len(alicuota["mes"]) == 0:
        mensajes_error.append("mes es requerido")

    try:
        alicuota["mes"] = int( alicuota["mes"] )
    except:
        mensajes_error.append("El valor de mes no es válido")

    alicuota["monto"] = request.forms.get( "monto", "").strip()
        
    if len(alicuota["monto"]) == 0:
        mensajes_error.append("monto es requerido")

    try:
        alicuota["monto"] = float( alicuota["monto"] )
    except:
        mensajes_error.append("El valor de monto no es válido")

    alicuota["monto_pendiente"] = request.forms.get( "monto_pendiente", "").strip()
        
    if len(alicuota["monto_pendiente"]) == 0:
        mensajes_error.append("monto_pendiente es requerido")

    try:
        alicuota["monto_pendiente"] = float( alicuota["monto_pendiente"] )
    except:
        mensajes_error.append("El valor de monto_pendiente no es válido")

    alicuota["pagado"] = request.forms.get( "pagado", "").strip()
        
    alicuota["pagado"] = alicuota["pagado"] == "1"

    alicuota["observaciones"] = request.forms.get( "observaciones", "").strip()
        
    if len(alicuota["observaciones"]) == 0:
        mensajes_error.append("observaciones es requerido")

    if len(alicuota["observaciones"]) > 256:
        mensajes_error.append("El tamaño de observaciones excede el permitido")

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_Alicuota", objeto = alicuota, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/alicuotas/" + str(alicuota['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Alicuotas.actualizar, alicuota)
    except:
        return template("xpd_alicuotas/editar_Alicuota", objeto = alicuota, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/alicuotas/" + str(alicuota['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_alicuotas/editar_Alicuota", objeto = alicuota, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_alicuotas/alicuotas/" + str(alicuota['id']), fecha_iso_to_js = fecha_iso_to_js )

CONFIG['rutas'].append({'ruta':'/alicuotas/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_alicuota })

def servir_page_insertar_alicuota(id_departamento):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    departamento, id_usuario_owner = departamento_getowner( conexion , id_departamento)
    conexion.close()
    if departamento is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )

    alicuota = Alicuotas.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_Alicuota", objeto = alicuota, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/departamentos/" + str(id_departamento), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    alicuota['id_departamento'] = id_departamento

    alicuota["anio"] = request.forms.get( "anio", "").strip()
        
    if len(alicuota["anio"]) == 0:
        mensajes_error.append("anio es requerido")

    try:
        alicuota["anio"] = int( alicuota["anio"] )
    except:
        mensajes_error.append("El valor de anio no es válido")

    alicuota["mes"] = request.forms.get( "mes", "").strip()
        
    if len(alicuota["mes"]) == 0:
        mensajes_error.append("mes es requerido")

    try:
        alicuota["mes"] = int( alicuota["mes"] )
    except:
        mensajes_error.append("El valor de mes no es válido")

    alicuota["monto"] = request.forms.get( "monto", "").strip()
        
    if len(alicuota["monto"]) == 0:
        mensajes_error.append("monto es requerido")

    try:
        alicuota["monto"] = float( alicuota["monto"] )
    except:
        mensajes_error.append("El valor de monto no es válido")

    alicuota["monto_pendiente"] = request.forms.get( "monto_pendiente", "").strip()
        
    if len(alicuota["monto_pendiente"]) == 0:
        mensajes_error.append("monto_pendiente es requerido")

    try:
        alicuota["monto_pendiente"] = float( alicuota["monto_pendiente"] )
    except:
        mensajes_error.append("El valor de monto_pendiente no es válido")

    alicuota["pagado"] = request.forms.get( "pagado", "").strip()
        
    alicuota["pagado"] = alicuota["pagado"] == "1"

    alicuota["observaciones"] = request.forms.get( "observaciones", "").strip()
        
    if len(alicuota["observaciones"]) == 0:
        mensajes_error.append("observaciones es requerido")

    if len(alicuota["observaciones"]) > 256:
        mensajes_error.append("El tamaño de observaciones excede el permitido")

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_Alicuota", objeto = alicuota, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/departamentos/" + str(id_departamento), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Alicuotas.insertar, alicuota)
    except:
        return template("xpd_alicuotas/editar_Alicuota", objeto = alicuota, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/departamentos/" + str(id_departamento), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/alicuotas/" + str(alicuota['id']) )

CONFIG['rutas'].append({'ruta':'/departamentos/<id_departamento>/nuevoalicuota', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_alicuota })

def servir_page_eliminar_alicuota(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    alicuota, id_usuario_owner = alicuota_getowner( conexion , id)
    conexion.close()
    if alicuota is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method != "GET":
        abort( 404, "Metodo no Valido" )
    try:
        transaccionar(Alicuotas.eliminar, alicuota)
    except:
    
        return template("xpd_usr/mensaje", lvl = "danger", mensaje = "Error al eliminar objeto.", href ="/xpd_alicuotas/Departamentos/" + str(alicuota['id_Departamento']) )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/Departamentos/" + str(alicuota['id_Departamento']) )
    
CONFIG['rutas'].append({'ruta':'/alicuotas/<id>/eliminar', 'metodos':['GET','POST'], 'funcion': servir_page_eliminar_alicuota })

def servir_page_get_alicuota_byid(id_alicuota):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    

    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = alicuota_getowner(conexion, id_alicuota)
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    
    conexion.close()
    return template("xpd_alicuotas/show_alicuota", objeto = objeto, usuario = usuario )

CONFIG['rutas'].append({'ruta':'/alicuotas/<id_alicuota>', 'metodos':['GET'], 'funcion': servir_page_get_alicuota_byid })

def servir_page_editar_abono(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    abono, id_usuario_owner = abono_getowner( conexion , id)
    conexion.close()
    if abono is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_Abono", objeto = abono, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/abonos/" + str(abono['id']), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    abono["fecha"] = request.forms.get( "fecha", "").strip()
        
    if len(abono["fecha"]) == 0:
        mensajes_error.append("fecha es requerido")

    try:
        if len(abono["fecha"]) > 0:
            abono["fecha"] = fecha_js_to_iso(abono["fecha"])
    except:
        mensajes_error.append("fecha no es una fecha válida")

    abono["monto"] = request.forms.get( "monto", "").strip()
        
    if len(abono["monto"]) == 0:
        mensajes_error.append("monto es requerido")

    try:
        abono["monto"] = float( abono["monto"] )
    except:
        mensajes_error.append("El valor de monto no es válido")

    abono["monto_aprobado"] = request.forms.get( "monto_aprobado", "").strip()
        
    if len(abono["monto_aprobado"]) == 0:
        mensajes_error.append("monto_aprobado es requerido")

    try:
        abono["monto_aprobado"] = float( abono["monto_aprobado"] )
    except:
        mensajes_error.append("El valor de monto_aprobado no es válido")

    abono["monto_por_aplicar"] = request.forms.get( "monto_por_aplicar", "").strip()
        
    if len(abono["monto_por_aplicar"]) == 0:
        mensajes_error.append("monto_por_aplicar es requerido")

    try:
        abono["monto_por_aplicar"] = float( abono["monto_por_aplicar"] )
    except:
        mensajes_error.append("El valor de monto_por_aplicar no es válido")

    abono["observacion"] = request.forms.get( "observacion", "").strip()
        
    if len(abono["observacion"]) > 256:
        mensajes_error.append("El tamaño de observacion excede el permitido")

    abono["genera_egreso"] = request.forms.get( "genera_egreso", "").strip()
        
    abono["genera_egreso"] = abono["genera_egreso"] == "1"

    abono["aplicado"] = request.forms.get( "aplicado", "").strip()
        
    abono["aplicado"] = abono["aplicado"] == "1"

    abono["aplicado_saldo"] = request.forms.get( "aplicado_saldo", "").strip()
        
    abono["aplicado_saldo"] = abono["aplicado_saldo"] == "1"

    abono["id_egreso"] = request.forms.get( "id_egreso", "").strip()
        
    try:
        abono["id_egreso"] = int( abono["id_egreso"] )
    except:
        mensajes_error.append("El valor de id_egreso no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_Abono", objeto = abono, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/abonos/" + str(abono['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Abonos.actualizar, abono)
    except:
        return template("xpd_alicuotas/editar_Abono", objeto = abono, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/abonos/" + str(abono['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_alicuotas/editar_Abono", objeto = abono, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_alicuotas/abonos/" + str(abono['id']), fecha_iso_to_js = fecha_iso_to_js )

CONFIG['rutas'].append({'ruta':'/abonos/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_abono })

def servir_page_insertar_abono(id_departamento):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    departamento, id_usuario_owner = departamento_getowner( conexion , id_departamento)
    conexion.close()
    if departamento is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )

    abono = Abonos.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_Abono", objeto = abono, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/departamentos/" + str(id_departamento), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    abono['id_departamento'] = id_departamento

    abono["fecha"] = request.forms.get( "fecha", "").strip()
        
    if len(abono["fecha"]) == 0:
        mensajes_error.append("fecha es requerido")

    abono["monto"] = request.forms.get( "monto", "").strip()
        
    if len(abono["monto"]) == 0:
        mensajes_error.append("monto es requerido")

    try:
        abono["monto"] = float( abono["monto"] )
    except:
        mensajes_error.append("El valor de monto no es válido")

    abono["monto_aprobado"] = request.forms.get( "monto_aprobado", "").strip()
        
    if len(abono["monto_aprobado"]) == 0:
        mensajes_error.append("monto_aprobado es requerido")

    try:
        abono["monto_aprobado"] = float( abono["monto_aprobado"] )
    except:
        mensajes_error.append("El valor de monto_aprobado no es válido")

    abono["monto_por_aplicar"] = request.forms.get( "monto_por_aplicar", "").strip()
        
    if len(abono["monto_por_aplicar"]) == 0:
        mensajes_error.append("monto_por_aplicar es requerido")

    try:
        abono["monto_por_aplicar"] = float( abono["monto_por_aplicar"] )
    except:
        mensajes_error.append("El valor de monto_por_aplicar no es válido")

    abono["observacion"] = request.forms.get( "observacion", "").strip()
        
    if len(abono["observacion"]) > 256:
        mensajes_error.append("El tamaño de observacion excede el permitido")

    abono["genera_egreso"] = request.forms.get( "genera_egreso", "").strip()
        
    abono["genera_egreso"] = abono["genera_egreso"] == "1"

    abono["aplicado"] = request.forms.get( "aplicado", "").strip()
        
    abono["aplicado"] = abono["aplicado"] == "1"

    abono["aplicado_saldo"] = request.forms.get( "aplicado_saldo", "").strip()
        
    abono["aplicado_saldo"] = abono["aplicado_saldo"] == "1"

    abono["id_egreso"] = request.forms.get( "id_egreso", "").strip()
        
    try:
        abono["id_egreso"] = int( abono["id_egreso"] )
    except:
        mensajes_error.append("El valor de id_egreso no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_Abono", objeto = abono, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/departamentos/" + str(id_departamento), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Abonos.insertar, abono)
    except:
        return template("xpd_alicuotas/editar_Abono", objeto = abono, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/departamentos/" + str(id_departamento), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/abonos/" + str(abono['id']) )

CONFIG['rutas'].append({'ruta':'/departamentos/<id_departamento>/nuevoabono', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_abono })

def servir_page_eliminar_abono(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    abono, id_usuario_owner = abono_getowner( conexion , id)
    conexion.close()
    if abono is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method != "GET":
        abort( 404, "Metodo no Valido" )
    try:
        transaccionar(Abonos.eliminar, abono)
    except:
    
        return template("xpd_usr/mensaje", lvl = "danger", mensaje = "Error al eliminar objeto.", href ="/xpd_alicuotas/Departamentos/" + str(abono['id_Departamento']) )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/Departamentos/" + str(abono['id_Departamento']) )
    
CONFIG['rutas'].append({'ruta':'/abonos/<id>/eliminar', 'metodos':['GET','POST'], 'funcion': servir_page_eliminar_abono })

def servir_page_get_abono_byid(id_abono):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    

    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = abono_getowner(conexion, id_abono)
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    
    eventolimpezaalicuotas = EventoLimpezaAlicuotas.getNamedQuery( conexion, "findByAbono", {'id_abono':objeto['id']} )

    conexion.close()
    return template("xpd_alicuotas/show_abono", objeto = objeto, usuario = usuario , eventolimpezaalicuotas = eventolimpezaalicuotas)

CONFIG['rutas'].append({'ruta':'/abonos/<id_abono>', 'metodos':['GET'], 'funcion': servir_page_get_abono_byid })

def servir_page_editar_eventolimpezaalicuota(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    eventolimpezaalicuota, id_usuario_owner = eventolimpezaalicuota_getowner( conexion , id)
    conexion.close()
    if eventolimpezaalicuota is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_EventoLimpezaAlicuota", objeto = eventolimpezaalicuota, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/eventolimpezaalicuotas/" + str(eventolimpezaalicuota['id']), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    eventolimpezaalicuota["id_alicuota"] = request.forms.get( "id_alicuota", "").strip()
        
    if len(eventolimpezaalicuota["id_alicuota"]) == 0:
        mensajes_error.append("id_alicuota es requerido")

    try:
        eventolimpezaalicuota["id_alicuota"] = int( eventolimpezaalicuota["id_alicuota"] )
    except:
        mensajes_error.append("El valor de id_alicuota no es válido")

    eventolimpezaalicuota["monto"] = request.forms.get( "monto", "").strip()
        
    if len(eventolimpezaalicuota["monto"]) == 0:
        mensajes_error.append("monto es requerido")

    try:
        eventolimpezaalicuota["monto"] = float( eventolimpezaalicuota["monto"] )
    except:
        mensajes_error.append("El valor de monto no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_EventoLimpezaAlicuota", objeto = eventolimpezaalicuota, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/eventolimpezaalicuotas/" + str(eventolimpezaalicuota['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(EventoLimpezaAlicuotas.actualizar, eventolimpezaalicuota)
    except:
        return template("xpd_alicuotas/editar_EventoLimpezaAlicuota", objeto = eventolimpezaalicuota, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/eventolimpezaalicuotas/" + str(eventolimpezaalicuota['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_alicuotas/editar_EventoLimpezaAlicuota", objeto = eventolimpezaalicuota, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_alicuotas/eventolimpezaalicuotas/" + str(eventolimpezaalicuota['id']), fecha_iso_to_js = fecha_iso_to_js )

CONFIG['rutas'].append({'ruta':'/eventolimpezaalicuotas/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_eventolimpezaalicuota })

def servir_page_insertar_eventolimpezaalicuota(id_abono):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    abono, id_usuario_owner = abono_getowner( conexion , id_abono)
    conexion.close()
    if abono is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )

    eventolimpezaalicuota = EventoLimpezaAlicuotas.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_EventoLimpezaAlicuota", objeto = eventolimpezaalicuota, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/abonos/" + str(id_abono), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    eventolimpezaalicuota['id_abono'] = id_abono

    eventolimpezaalicuota["id_alicuota"] = request.forms.get( "id_alicuota", "").strip()
        
    if len(eventolimpezaalicuota["id_alicuota"]) == 0:
        mensajes_error.append("id_alicuota es requerido")

    try:
        eventolimpezaalicuota["id_alicuota"] = int( eventolimpezaalicuota["id_alicuota"] )
    except:
        mensajes_error.append("El valor de id_alicuota no es válido")

    eventolimpezaalicuota["monto"] = request.forms.get( "monto", "").strip()
        
    if len(eventolimpezaalicuota["monto"]) == 0:
        mensajes_error.append("monto es requerido")

    try:
        eventolimpezaalicuota["monto"] = float( eventolimpezaalicuota["monto"] )
    except:
        mensajes_error.append("El valor de monto no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_EventoLimpezaAlicuota", objeto = eventolimpezaalicuota, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/abonos/" + str(id_abono), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(EventoLimpezaAlicuotas.insertar, eventolimpezaalicuota)
    except:
        return template("xpd_alicuotas/editar_EventoLimpezaAlicuota", objeto = eventolimpezaalicuota, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/abonos/" + str(id_abono), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/eventolimpezaalicuotas/" + str(eventolimpezaalicuota['id']) )

CONFIG['rutas'].append({'ruta':'/abonos/<id_abono>/nuevoeventolimpezaalicuota', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_eventolimpezaalicuota })

def servir_page_eliminar_eventolimpezaalicuota(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    eventolimpezaalicuota, id_usuario_owner = eventolimpezaalicuota_getowner( conexion , id)
    conexion.close()
    if eventolimpezaalicuota is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method != "GET":
        abort( 404, "Metodo no Valido" )
    try:
        transaccionar(EventoLimpezaAlicuotas.eliminar, eventolimpezaalicuota)
    except:
    
        return template("xpd_usr/mensaje", lvl = "danger", mensaje = "Error al eliminar objeto.", href ="/xpd_alicuotas/Abonos/" + str(eventolimpezaalicuota['id_Abono']) )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/Abonos/" + str(eventolimpezaalicuota['id_Abono']) )
    
CONFIG['rutas'].append({'ruta':'/eventolimpezaalicuotas/<id>/eliminar', 'metodos':['GET','POST'], 'funcion': servir_page_eliminar_eventolimpezaalicuota })

def servir_page_get_eventolimpezaalicuota_byid(id_eventolimpezaalicuota):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    

    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = eventolimpezaalicuota_getowner(conexion, id_eventolimpezaalicuota)
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    
    conexion.close()
    return template("xpd_alicuotas/show_eventolimpezaalicuota", objeto = objeto, usuario = usuario )

CONFIG['rutas'].append({'ruta':'/eventolimpezaalicuotas/<id_eventolimpezaalicuota>', 'metodos':['GET'], 'funcion': servir_page_get_eventolimpezaalicuota_byid })

def servir_page_main():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    redirect('/xpd_alicuotas/condominios')    

CONFIG['rutas'].append({'ruta':'/main', 'metodos':['GET'], 'funcion': servir_page_main })

def servir_page_admin_main():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    if 'Administrador' not in usuario['roles']:
        abort(403,"Acceso Denegado")  

    entidades = [

    ]
    return template("xpd_alicuotas/main", usuario = usuario, titulo = "Administración", entidades = entidades)

CONFIG['rutas'].append({'ruta':'/admin', 'metodos':['GET'], 'funcion': servir_page_admin_main })

def rutearModulo( app : Bottle, ruta_base : str ):
    CONFIG['RUTA_BASE'] = ruta_base
    for item in CONFIG['rutas']:
        app.route( ruta_base + item['ruta'], method = item['metodos'] )( item['funcion'])

def aplicarAbonos(con, id_departamento):

    departamento = Departamentos.getNamedQuery(con, "findById", {"id":id_departamento})
    assert len(departamento) == 1 , "Referencia de Departamento no válida"
    departamento = departamento[0]

    condominio = Condominios.getNamedQuery(con, "findById", {"id":departamento['id_condominio']})
    assert len(condominio) == 1 , "Referencia de Condominio no válida"
    condominio = condominio[0]

    alicuotas = Alicuotas.getNamedQuery(con, "findByDepartamento",{"id_departamento":id_departamento})
    alicuotas = [ x for x in alicuotas if x['pagado'] == '0']
    abonos = Abonos.getNamedQuery(con, "findByDepartamento",{"id_departamento":id_departamento})
    abonos = [ x for x in abonos if x['aplicado'] == '1' and x['monto_por_aplicar'] > 0.0 ]

    it_alicuotas = iter(alicuotas)
    alicuota = None
    try:
        alicuota = next(it_alicuotas)
    except StopIteration:
        pass

    for abono in abonos:

        if abono['aplicado_saldo'] == "0" :            
            departamento['saldo'] += abono['monto_aprobado']
            Departamentos.actualizar(con, departamento)
            condominio['saldo'] += abono['monto_aprobado']
            Condominios.actualizar(con, condominio)            
            abono['aplicado_saldo'] = "1"
            
            if abono['genera_egreso'] == '1':
                egreso = {'fecha':abono['fecha'], 'destino':departamento['propietario'] , 'monto':abono['monto_aprobado'], 'observaciones': abono['observacion'], 'anulado':'0', 'id_condominio':condominio['id'] }
                Egresos.insertar(con, egreso)
                aplicarEgreso(con, egreso)
                abono['id_egreso'] = egreso['id']

            Abonos.actualizar(con, abono)

        while abono['monto_por_aplicar'] > 0.0:
            if alicuota is None:
                break
            
            delta = abono['monto_por_aplicar'] if abono['monto_por_aplicar'] < alicuota['monto_pendiente'] else alicuota['monto_pendiente']
            abono['monto_por_aplicar'] -= delta
            alicuota['monto_pendiente'] -= delta

            if alicuota['monto_pendiente'] <= 0.0 :
                 alicuota['monto_pendiente'] = 0.0
                 alicuota['pagado'] = '1'
            if abono['monto_por_aplicar'] < 0.0:
                abono['monto_por_aplicar'] = 0.0

            abono_alicuota = {"id_abono":abono['id'], "id_alicuota":alicuota['id'], "monto": delta}
            
            Abonos.actualizar(con, abono)
            Alicuotas.actualizar(con, alicuota)
            EventoLimpezaAlicuotas.insertar(con, abono_alicuota)

            if alicuota['pagado'] == '1' :
                try:
                    alicuota = next(it_alicuotas)
                except StopIteration:
                    alicuota = None

def aplicarEgreso(con, egreso):
    egreso_persistente = Egresos.getNamedQuery(con, "findById", {'id':egreso['id']})
    assert len(egreso_persistente) == 1 and egreso_persistente[0]['anulado'] == '0', "Registro de egreso no es valido"
    egreso_persistente = egreso_persistente[0]
    
    condominio = Condominios.getNamedQuery(con, "findById", {"id":egreso_persistente['id_condominio']})
    assert len(condominio) == 1 , "Referencia de Condominio no válida"
    condominio = condominio[0]

    condominio['saldo'] -= egreso['monto']
    Condominios.actualizar(con, condominio)



