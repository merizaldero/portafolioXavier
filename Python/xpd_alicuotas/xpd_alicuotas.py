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
        { 'nombre':'id_condominio', 'nombreCampo':'ID_CONDOMINIO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByCondominio', 'whereClause':['id_condominio'], },
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

EventoLimpiezas = orm.Entidad()
EventoLimpiezas.setMetamodelo({
    'nombreTabla' : 'EVENTO_LIMPIEZA',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'fecha', 'nombreCampo':'FECHA', 'tipo':orm.XPDDATE, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'fecha_validacion', 'nombreCampo':'FECHA_VALIDACION', 'tipo':orm.XPDDATE, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'observacion', 'nombreCampo':'OBSERVACION', 'tipo':orm.XPDSTRING, 'tamano':256, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_departamento', 'nombreCampo':'ID_DEPARTAMENTO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByDepartamento', 'whereClause':['id_departamento'], },
        ]
    })

EventoLimpezaAlicuotas = orm.Entidad()
EventoLimpezaAlicuotas.setMetamodelo({
    'nombreTabla' : 'EVLIM_ALICUOTA',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'id_alicuota', 'nombreCampo':'ID_ALICUOTA', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'id_eventolimpieza', 'nombreCampo':'ID_EVENTOLIMPIEZA', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'fkAlicuota', 'whereClause':['id_alicuota'], },
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByEventoLimpieza', 'whereClause':['id_eventolimpieza'], },
        ]
    })


def inicializar():
    entidades = [Condominios, Departamentos, Alicuotas, EventoLimpiezas, EventoLimpezaAlicuotas]
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

def alicuota_getowner(conexion, id_alicuota):
    objeto = Alicuotas.getNamedQuery(conexion, 'findById', {'id': id_alicuota})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, departamento_getowner(conexion, objeto['id_departamento'])[1] )

def eventolimpieza_getowner(conexion, id_eventolimpieza):
    objeto = EventoLimpiezas.getNamedQuery(conexion, 'findById', {'id': id_eventolimpieza})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, departamento_getowner(conexion, objeto['id_departamento'])[1] )

def eventolimpezaalicuota_getowner(conexion, id_eventolimpezaalicuota):
    objeto = EventoLimpezaAlicuotas.getNamedQuery(conexion, 'findById', {'id': id_eventolimpezaalicuota})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, eventolimpieza_getowner(conexion, objeto['id_eventolimpieza'])[1] )

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

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_Condominio", objeto = condominio, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/condominios", fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Condominios.insertar, condominio)
    except:
        return template("xpd_alicuotas/editar_Condominio", objeto = condominio, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/condominios", fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/condominios/" + str(condominio['id']) )

CONFIG['rutas'].append({'ruta':'/condominios/nuevo', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_condominio })

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

    conexion.close()
    return template("xpd_alicuotas/show_condominio", objeto = objeto, usuario = usuario , departamentos = departamentos)

CONFIG['rutas'].append({'ruta':'/condominios/<id_condominio>', 'metodos':['GET'], 'funcion': servir_page_get_condominio_byid })

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

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_Departamento", objeto = departamento, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/condominios/" + str(id_condominio), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Departamentos.insertar, departamento)
    except:
        return template("xpd_alicuotas/editar_Departamento", objeto = departamento, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/condominios/" + str(id_condominio), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/departamentos/" + str(departamento['id']) )

CONFIG['rutas'].append({'ruta':'/condominios/<id_condominio>/nuevodepartamento', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_departamento })

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

    eventolimpiezas = EventoLimpiezas.getNamedQuery( conexion, "findByDepartamento", {'id_departamento':objeto['id']} )

    conexion.close()
    return template("xpd_alicuotas/show_departamento", objeto = objeto, usuario = usuario , alicuotas = alicuotas, eventolimpiezas = eventolimpiezas)

CONFIG['rutas'].append({'ruta':'/departamentos/<id_departamento>', 'metodos':['GET'], 'funcion': servir_page_get_departamento_byid })

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

def servir_page_editar_eventolimpieza(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    eventolimpieza, id_usuario_owner = eventolimpieza_getowner( conexion , id)
    conexion.close()
    if eventolimpieza is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_EventoLimpieza", objeto = eventolimpieza, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/eventolimpiezas/" + str(eventolimpieza['id']), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    eventolimpieza["fecha"] = request.forms.get( "fecha", "").strip()
        
    if len(eventolimpieza["fecha"]) == 0:
        mensajes_error.append("fecha es requerido")

    try:
        if len(eventolimpieza["fecha"]) > 0:
            eventolimpieza["fecha"] = fecha_js_to_iso(eventolimpieza["fecha"])
    except:
        mensajes_error.append("fecha no es una fecha válida")

    eventolimpieza["fecha_validacion"] = request.forms.get( "fecha_validacion", "").strip()
        
    try:
        if len(eventolimpieza["fecha_validacion"]) > 0:
            eventolimpieza["fecha_validacion"] = fecha_js_to_iso(eventolimpieza["fecha_validacion"])
    except:
        mensajes_error.append("fecha_validacion no es una fecha válida")

    eventolimpieza["observacion"] = request.forms.get( "observacion", "").strip()
        
    if len(eventolimpieza["observacion"]) > 256:
        mensajes_error.append("El tamaño de observacion excede el permitido")

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_EventoLimpieza", objeto = eventolimpieza, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/eventolimpiezas/" + str(eventolimpieza['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(EventoLimpiezas.actualizar, eventolimpieza)
    except:
        return template("xpd_alicuotas/editar_EventoLimpieza", objeto = eventolimpieza, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/eventolimpiezas/" + str(eventolimpieza['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_alicuotas/editar_EventoLimpieza", objeto = eventolimpieza, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_alicuotas/eventolimpiezas/" + str(eventolimpieza['id']), fecha_iso_to_js = fecha_iso_to_js )

CONFIG['rutas'].append({'ruta':'/eventolimpiezas/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_eventolimpieza })

def servir_page_insertar_eventolimpieza(id_departamento):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    departamento, id_usuario_owner = departamento_getowner( conexion , id_departamento)
    # alicuotas = conexion.consultar("SELECT id as id, anio as anio, mes as mes, monto as monto, monto_pendiente as monto_pendiente, pagado as pagado, observaciones as observaciones, id_departamento as id_departamento FROM ALICUOTA  WHERE ID_DEPARTAMENTO = :id_departamento and PAGADO = '0' order by ANIO, MES", {'id_departamento':id_departamento}, ['id', 'anio', 'mes', 'monto', 'monto_pendiente', 'pagado', 'observaciones', 'id_departamento'])
    conexion.close()
    if departamento is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )

    eventolimpieza = EventoLimpiezas.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_EventoLimpieza", objeto = eventolimpieza, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/departamentos/" + str(id_departamento), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    eventolimpieza['id_departamento'] = id_departamento

    eventolimpieza["fecha"] = request.forms.get( "fecha", "").strip()
        
    if len(eventolimpieza["fecha"]) == 0:
        mensajes_error.append("fecha es requerido")

    eventolimpieza["fecha_validacion"] = request.forms.get( "fecha_validacion", "").strip()
        
    eventolimpieza["observacion"] = request.forms.get( "observacion", "").strip()
        
    if len(eventolimpieza["observacion"]) > 256:
        mensajes_error.append("El tamaño de observacion excede el permitido")

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_EventoLimpieza", objeto = eventolimpieza, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/departamentos/" + str(id_departamento), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(EventoLimpiezas.insertar, eventolimpieza)
    except:
        return template("xpd_alicuotas/editar_EventoLimpieza", objeto = eventolimpieza, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/departamentos/" + str(id_departamento), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/eventolimpiezas/" + str(eventolimpieza['id']) )

CONFIG['rutas'].append({'ruta':'/departamentos/<id_departamento>/nuevoeventolimpieza', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_eventolimpieza })

def servir_page_get_eventolimpieza_byid(id_eventolimpieza):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    

    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = eventolimpieza_getowner(conexion, id_eventolimpieza)
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    
    eventolimpezaalicuotas = EventoLimpezaAlicuotas.getNamedQuery( conexion, "findByEventoLimpieza", {'id_eventolimpieza':objeto['id']} )

    conexion.close()
    return template("xpd_alicuotas/show_eventolimpieza", objeto = objeto, usuario = usuario , eventolimpezaalicuotas = eventolimpezaalicuotas)

CONFIG['rutas'].append({'ruta':'/eventolimpiezas/<id_eventolimpieza>', 'metodos':['GET'], 'funcion': servir_page_get_eventolimpieza_byid })

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

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_EventoLimpezaAlicuota", objeto = eventolimpezaalicuota, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/eventolimpezaalicuotas/" + str(eventolimpezaalicuota['id']), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(EventoLimpezaAlicuotas.actualizar, eventolimpezaalicuota)
    except:
        return template("xpd_alicuotas/editar_EventoLimpezaAlicuota", objeto = eventolimpezaalicuota, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/eventolimpezaalicuotas/" + str(eventolimpezaalicuota['id']), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_alicuotas/editar_EventoLimpezaAlicuota", objeto = eventolimpezaalicuota, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_alicuotas/eventolimpezaalicuotas/" + str(eventolimpezaalicuota['id']), fecha_iso_to_js = fecha_iso_to_js )

# CONFIG['rutas'].append({'ruta':'/eventolimpezaalicuotas/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_eventolimpezaalicuota })

def servir_page_insertar_eventolimpezaalicuota(id_eventolimpieza):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    eventolimpieza, id_usuario_owner = eventolimpieza_getowner( conexion , id_eventolimpieza)
    alicuotas = []
    if eventolimpieza is not None:
        alicuotas = conexion.consultar("SELECT id as id, anio as anio, mes as mes, monto as monto, monto_pendiente as monto_pendiente, pagado as pagado, observaciones as observaciones, id_departamento as id_departamento FROM ALICUOTA  WHERE ID_DEPARTAMENTO = :id_departamento and PAGADO = '0' order by ANIO, MES", {'id_departamento':eventolimpieza['id_departamento']}, ['id', 'anio', 'mes', 'monto', 'monto_pendiente', 'pagado', 'observaciones', 'id_departamento'])
    conexion.close()
    if eventolimpieza is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )

    eventolimpezaalicuota = EventoLimpezaAlicuotas.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_alicuotas/editar_EventoLimpezaAlicuota", alicuotas = alicuotas, objeto = eventolimpezaalicuota, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_alicuotas/eventolimpiezas/" + str(id_eventolimpieza), fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []

    eventolimpezaalicuota['id_eventolimpieza'] = id_eventolimpieza

    eventolimpezaalicuota["id_alicuota"] = request.forms.get( "id_alicuota", "").strip()
        
    if len(eventolimpezaalicuota["id_alicuota"]) == 0:
        mensajes_error.append("id_alicuota es requerido")

    try:
        eventolimpezaalicuota["id_alicuota"] = int( eventolimpezaalicuota["id_alicuota"] )
    except:
        mensajes_error.append("El valor de id_alicuota no es válido")

    if len(mensajes_error) > 0:
        return template("xpd_alicuotas/editar_EventoLimpezaAlicuota", alicuotas = alicuotas, objeto = eventolimpezaalicuota, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_alicuotas/eventolimpiezas/" + str(id_eventolimpieza), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(EventoLimpezaAlicuotas.insertar, eventolimpezaalicuota)
    except:
        return template("xpd_alicuotas/editar_EventoLimpezaAlicuota", alicuotas = alicuotas, objeto = eventolimpezaalicuota, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_alicuotas/eventolimpiezas/" + str(id_eventolimpieza), fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_alicuotas/eventolimpezaalicuotas/" + str(eventolimpezaalicuota['id']) )

CONFIG['rutas'].append({'ruta':'/eventolimpiezas/<id_eventolimpieza>/nuevoeventolimpezaalicuota', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_eventolimpezaalicuota })

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
