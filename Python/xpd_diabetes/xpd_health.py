import xpd_orm as orm
from os.path import abspath , dirname, join, exists, basename
from os import makedirs
from os import remove as remove_file

import matplotlib.pyplot as plt

from bottle import run, debug, route, abort, static_file, template, request, response, redirect
from bottle import Bottle
import datetime

import xpd_usr

PATH_BDD = dirname(abspath(__file__)) + "/data/xpd_health.db"
CONFIG = {'rutas': []}

import datetime

CONVERSION_ACENTOS = {'á': '&aacute;', 'é': '&eacute;', 'í': '&iacute;', 'ó': '&oacute;', 'ú': '&uacute;', 'ñ': '&nacute;', 'Ñ': '&Nacute;'}

def convertir_acentos(texto):
    if texto is None:
        return None
    for clave in CONVERSION_ACENTOS.keys():
        texto = texto.replace(clave, CONVERSION_ACENTOS[clave])
    return texto

def des_convertir_acentos(texto):
    if texto is None:
        return None
    for clave in CONVERSION_ACENTOS.keys():
        texto = texto.replace(CONVERSION_ACENTOS[clave] , clave)
    return texto
    
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


Sujetos = orm.Entidad()
Sujetos.setMetamodelo({
    'nombreTabla' : 'SUJETO',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'nombre', 'nombreCampo':'NOMBRE', 'tipo':orm.XPDSTRING, 'tamano':128, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'umbral_maximo', 'nombreCampo':'UMBRAL_MAXIMO', 'tipo':orm.XPDREAL, 'tamano': 6, 'precision': 2, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'umbral_minimo', 'nombreCampo':'UMBRAL_MINIMO', 'tipo':orm.XPDREAL, 'tamano': 6, 'precision': 2, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'fecha_update', 'nombreCampo':'FECHA_UPDATE', 'tipo':orm.XPDDATE, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_user', 'nombreCampo':'ID_USER', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findByUser', 'whereClause':['id_user'], },
        ]
    })

LecturaGlucosas = orm.Entidad()
LecturaGlucosas.setMetamodelo({
    'nombreTabla' : 'LECTURA_GLUCOSA',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'fecha_hora', 'nombreCampo':'FECHA_HORA', 'tipo':orm.XPDDATE, 'pk': False, 'incremental': False, 'insert': True, 'update': False, },
        { 'nombre':'valor', 'nombreCampo':'VALOR', 'tipo':orm.XPDREAL, 'tamano': 6, 'precision': 2, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'observacion', 'nombreCampo':'OBSERVACION', 'tipo':orm.XPDSTRING, 'tamano':256, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_sujeto', 'nombreCampo':'ID_SUJETO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findBySujeto', 'whereClause':['id_sujeto'], },
        ]
    })

DosisInsulinas = orm.Entidad()
DosisInsulinas.setMetamodelo({
    'nombreTabla' : 'DOSIS_INSULINA',
    'propiedades' : [
        { 'nombre':'id', 'nombreCampo':'ID', 'tipo':orm.XPDINTEGER, 'pk': True, 'incremental': True, 'insert': False, 'update': False, },
        { 'nombre':'fecha_hora', 'nombreCampo':'FECHA_HORA', 'tipo':orm.XPDDATE, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'unidades_aplicadas', 'nombreCampo':'UNIDADES_APLICADAS', 'tipo':orm.XPDINTEGER, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'observacion', 'nombreCampo':'OBSERVACION', 'tipo':orm.XPDSTRING, 'tamano':128, 'pk': False, 'incremental': False, 'insert': True, 'update': True, },
        { 'nombre':'id_sujeto', 'nombreCampo':'ID_SUJETO', 'tipo':orm.XPDINTEGER, 'incremental': False, },
        ],
    'namedQueries' : [
        { 'nombre':'findById', 'whereClause':['id'], },
        { 'nombre':'findBySujeto', 'whereClause':['id_sujeto'], },
        ]
    })


def inicializar():
    entidades = [Sujetos, LecturaGlucosas, DosisInsulinas]
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
    

def sujeto_getowner(conexion, id_sujeto):
    objeto = Sujetos.getNamedQuery(conexion, 'findById', {'id': id_sujeto})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, objeto['id_user'])

def lecturaglucosa_getowner(conexion, id_lecturaglucosa):
    objeto = LecturaGlucosas.getNamedQuery(conexion, 'findById', {'id': id_lecturaglucosa})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, sujeto_getowner(conexion, objeto['id_sujeto'])[1] )

def dosisinsulina_getowner(conexion, id_dosisinsulina):
    objeto = DosisInsulinas.getNamedQuery(conexion, 'findById', {'id': id_dosisinsulina})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]

    return (objeto, sujeto_getowner(conexion, objeto['id_sujeto'])[1] )

def servir_page_editar_sujeto(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    sujeto, id_usuario_owner = sujeto_getowner( conexion , id)
    conexion.close()
    if sujeto is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_health/editar_Sujeto", objeto = sujeto, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_health/sujetos/" + str(sujeto['id']), fecha_iso_to_js = fecha_iso_to_js, des_convertir_acentos = des_convertir_acentos)
    # A partir de este punto se asume POST
    mensajes_error = []

    sujeto["nombre"] = request.forms.get( "nombre", "").strip()
        
    if len(sujeto["nombre"]) == 0:
        mensajes_error.append("nombre es requerido")

    if len(sujeto["nombre"]) > 128:
        mensajes_error.append("El tamaño de nombre excede el permitido")

    sujeto["umbral_maximo"] = request.forms.get( "umbral_maximo", "").strip()
        
    if len(sujeto["umbral_maximo"]) == 0:
        mensajes_error.append("umbral_maximo es requerido")

    try:
        sujeto["umbral_maximo"] = float( sujeto["umbral_maximo"] )
    except:
        mensajes_error.append("El valor de umbral_maximo no es válido")

    sujeto["umbral_minimo"] = request.forms.get( "umbral_minimo", "").strip()
        
    if len(sujeto["umbral_minimo"]) == 0:
        mensajes_error.append("umbral_minimo es requerido")

    try:
        sujeto["umbral_minimo"] = float( sujeto["umbral_minimo"] )
    except:
        mensajes_error.append("El valor de umbral_minimo no es válido")

    sujeto["fecha_update"] = request.forms.get( "fecha_update", "").strip()
        
    if len(sujeto["fecha_update"]) == 0:
        mensajes_error.append("fecha_update es requerido")

    try:
        if len(sujeto["fecha_update"]) > 0:
            sujeto["fecha_update"] = fecha_js_to_iso(sujeto["fecha_update"])
    except:
        mensajes_error.append("fecha_update no es una fecha válida")

    if len(mensajes_error) > 0:
        return template("xpd_health/editar_Sujeto", objeto = sujeto, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_health/sujetos/" + str(sujeto['id']), fecha_iso_to_js = fecha_iso_to_js , des_convertir_acentos = des_convertir_acentos)    
    try:
        transaccionar(Sujetos.actualizar, sujeto)
    except:
        return template("xpd_health/editar_Sujeto", objeto = sujeto, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_health/sujetos/" + str(sujeto['id']), fecha_iso_to_js = fecha_iso_to_js , des_convertir_acentos = des_convertir_acentos)
    return template("xpd_health/editar_Sujeto", objeto = sujeto, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_health/sujetos/" + str(sujeto['id']), fecha_iso_to_js = fecha_iso_to_js, des_convertir_acentos = des_convertir_acentos )

CONFIG['rutas'].append({'ruta':'/sujetos/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_sujeto })

def servir_page_insertar_sujeto():

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    sujeto = Sujetos.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_health/editar_Sujeto", objeto = sujeto, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_health/sujetos", fecha_iso_to_js = fecha_iso_to_js, des_convertir_acentos = des_convertir_acentos)
    # A partir de este punto se asume POST
    mensajes_error = []

    sujeto['id_user'] = usuario['id']

    sujeto["nombre"] = request.forms.get( "nombre", "").strip()
        
    if len(sujeto["nombre"]) == 0:
        mensajes_error.append("nombre es requerido")

    sujeto["nombre"] = convertir_acentos( sujeto["nombre"] )
    if len(sujeto["nombre"]) > 128:
        mensajes_error.append("El tamaño de nombre excede el permitido")

    sujeto["umbral_maximo"] = request.forms.get( "umbral_maximo", "").strip()
        
    if len(sujeto["umbral_maximo"]) == 0:
        mensajes_error.append("umbral_maximo es requerido")

    try:
        sujeto["umbral_maximo"] = float( sujeto["umbral_maximo"] )
    except:
        mensajes_error.append("El valor de umbral_maximo no es válido")

    sujeto["umbral_minimo"] = request.forms.get( "umbral_minimo", "").strip()
        
    if len(sujeto["umbral_minimo"]) == 0:
        mensajes_error.append("umbral_minimo es requerido")

    try:
        sujeto["umbral_minimo"] = float( sujeto["umbral_minimo"] )
    except:
        mensajes_error.append("El valor de umbral_minimo no es válido")

    sujeto["fecha_update"] = request.forms.get( "fecha_update", "").strip()
        
    if len(sujeto["fecha_update"]) == 0:
        mensajes_error.append("fecha_update es requerido")

    if len(mensajes_error) > 0:
        return template("xpd_health/editar_Sujeto", objeto = sujeto, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_health/sujetos", fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(Sujetos.insertar, sujeto)
    except:
        return template("xpd_health/editar_Sujeto", objeto = sujeto, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_health/sujetos", fecha_iso_to_js = fecha_iso_to_js, des_convertir_acentos = des_convertir_acentos )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_health/sujetos/" + str(sujeto['id']) )

CONFIG['rutas'].append({'ruta':'/sujetos/nuevo', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_sujeto })

def servir_page_eliminar_sujeto(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    sujeto, id_usuario_owner = sujeto_getowner( conexion , id)
    conexion.close()
    if sujeto is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method != "GET":
        abort( 404, "Metodo no Valido" )
    try:
        transaccionar(Sujetos.eliminar, sujeto)
    except:
    
        return template("xpd_usr/mensaje", lvl = "danger", mensaje = "Error al eliminar objeto.", href ="/xpd_health/sujetos" )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_health/sujetos" )
    
CONFIG['rutas'].append({'ruta':'/sujetos/<id>/eliminar', 'metodos':['GET','POST'], 'funcion': servir_page_eliminar_sujeto })

def servir_page_get_sujeto_lista():
    conexion = orm.Conexion(PATH_BDD)

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    
    conexion = orm.Conexion(PATH_BDD)

    lista = Sujetos.getNamedQuery(conexion, 'findByUser', {'id_user':usuario['id']})

    conexion.close()

    return template("xpd_health/listar_Sujeto", lista = lista, usuario = usuario)
    
CONFIG['rutas'].append({'ruta':'/sujetos', 'metodos':['GET'], 'funcion': servir_page_get_sujeto_lista })

def generar_imagen_sujeto(id_sujeto):
    conexion = orm.Conexion(PATH_BDD)

    objeto = Sujetos.getNamedQuery(conexion, "findById", {"id":id_sujeto})[0]
    lecturaglucosas = LecturaGlucosas.getNamedQuery( conexion, "findBySujeto", {'id_sujeto':objeto['id']} )
    dosisinsulinas = DosisInsulinas.getNamedQuery( conexion, "findBySujeto", {'id_sujeto':objeto['id']} )

    conexion.close()

    for lectura in lecturaglucosas:
        lectura['fecha_hora'] = datetime.datetime.fromisoformat(lectura['fecha_hora'])
        
    for dosis in dosisinsulinas:
        dosis['fecha_hora'] = datetime.datetime.fromisoformat(dosis['fecha_hora'])

    # Genera Gráfica y la guarda en archivo
    ancho_pulgadas = 10
    alto_pulgadas = 5
    dpi = 100

    fig, ax = plt.subplots(figsize=(ancho_pulgadas, alto_pulgadas), dpi=dpi)
    ax.set_title("Control Glucosa")

    fecha_inicio = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days = - 3)

    lecturaglucosas = [ x for x in lecturaglucosas if x['fecha_hora'] >= fecha_inicio ]
    dosisinsulinas = [ x for x in dosisinsulinas if x['fecha_hora'] >= fecha_inicio ]

    ejex = [ x['fecha_hora'] - fecha_inicio for x in lecturaglucosas]
    ejex = [ x.total_seconds() for x in ejex ]
    fecha_fin = max( [x['fecha_hora'] for x in lecturaglucosas] ) - fecha_inicio

    xticks_rango = range(1, int (fecha_fin.total_seconds() ), 60*60*24 )
    xticks = [ fecha_inicio + datetime.timedelta(seconds=x) for x in xticks_rango ]
    xticks = [ x.isoformat()[:10] for x in xticks]

    ax.plot( ejex, [ x['valor'] for x in lecturaglucosas], marker = 'o' )
    ax.plot( ejex, [ objeto['umbral_minimo'] for x in lecturaglucosas] )
    ax.plot( ejex, [ objeto['umbral_maximo'] for x in lecturaglucosas] )

    for indice, lecturaglucosa in enumerate(lecturaglucosas):
        plt.text(
            ejex[indice],
            lecturaglucosa['valor'] + 1,
            str(lecturaglucosa['valor']),
            fontsize = 10,
            ha = 'center'
        )

    ejex1 = [ x['fecha_hora'] - fecha_inicio for x in dosisinsulinas]
    ejex1 = [ x.total_seconds() for x in ejex1 ]
    ax.scatter( ejex1, [ objeto['umbral_minimo'] for x in ejex1], color = 'green', s = [ x ['unidades_aplicadas'] *2 for x in dosisinsulinas ] )

    for indice, dosisinsulina in enumerate(dosisinsulinas):
        plt.text(
            ejex1[indice] ,
            objeto['umbral_minimo'] + 1,
            str(dosisinsulina['observacion']),
            fontsize = 15,
            ha = 'center'
        )

    plt.xticks(xticks_rango, xticks)
    ax.grid()

    path_salida = dirname(abspath(__file__)) + f"/static/img/resumen_{id_sujeto}.png"
    plt.savefig(path_salida)

    return path_salida

def servir_img_get_sujeto_byid(id_sujeto):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    

    conexion = orm.Conexion(PATH_BDD)

    objeto, id_user_owner = sujeto_getowner(conexion, id_sujeto)

    conexion.close()

    if objeto is None:
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        abort( 403, "Acceso no autorizado") 

    path_salida = generar_imagen_sujeto(id_sujeto)

    return static_file( basename(path_salida), root = dirname(path_salida) )
    

CONFIG['rutas'].append({'ruta':'/sujetos/<id_sujeto>/resumen.png', 'metodos':['GET'], 'funcion': servir_img_get_sujeto_byid })

def servir_page_get_sujeto_byid(id_sujeto):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    

    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = sujeto_getowner(conexion, id_sujeto)
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    
    lecturaglucosas = LecturaGlucosas.getNamedQuery( conexion, "findBySujeto", {'id_sujeto':objeto['id']} )
    lecturaglucosas.reverse()
    dosisinsulinas = DosisInsulinas.getNamedQuery( conexion, "findBySujeto", {'id_sujeto':objeto['id']} )
    dosisinsulinas.reverse()

    conexion.close()
    return template("xpd_health/show_sujeto", objeto = objeto, usuario = usuario , lecturaglucosas = lecturaglucosas, dosisinsulinas = dosisinsulinas)

CONFIG['rutas'].append({'ruta':'/sujetos/<id_sujeto>', 'metodos':['GET'], 'funcion': servir_page_get_sujeto_byid })

def servir_page_editar_lecturaglucosa(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    lecturaglucosa, id_usuario_owner = lecturaglucosa_getowner( conexion , id)
    conexion.close()
    if lecturaglucosa is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_health/editar_LecturaGlucosa", objeto = lecturaglucosa, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_health/lecturaglucosas/" + str(lecturaglucosa['id']), fecha_iso_to_js = fecha_iso_to_js, des_convertir_acentos = des_convertir_acentos)
    # A partir de este punto se asume POST
    mensajes_error = []

    lecturaglucosa["fecha_hora"] = request.forms.get( "fecha_hora", "").strip()
        
    if len(lecturaglucosa["fecha_hora"]) == 0:
        mensajes_error.append("fecha_hora es requerido")

    try:
        if len(lecturaglucosa["fecha_hora"]) > 0:
            lecturaglucosa["fecha_hora"] = fecha_js_to_iso(lecturaglucosa["fecha_hora"])
    except:
        mensajes_error.append("fecha_hora no es una fecha válida")

    lecturaglucosa["valor"] = request.forms.get( "valor", "").strip()
        
    if len(lecturaglucosa["valor"]) == 0:
        mensajes_error.append("valor es requerido")

    try:
        lecturaglucosa["valor"] = float( lecturaglucosa["valor"] )
    except:
        mensajes_error.append("El valor de valor no es válido")

    lecturaglucosa["observacion"] = request.forms.get( "observacion", "").strip()
        
    if len(lecturaglucosa["observacion"]) > 256:
        mensajes_error.append("El tamaño de observacion excede el permitido")

    if len(mensajes_error) > 0:
        return template("xpd_health/editar_LecturaGlucosa", objeto = lecturaglucosa, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_health/lecturaglucosas/" + str(lecturaglucosa['id']), fecha_iso_to_js = fecha_iso_to_js , des_convertir_acentos = des_convertir_acentos)    
    try:
        transaccionar(LecturaGlucosas.actualizar, lecturaglucosa)
    except:
        return template("xpd_health/editar_LecturaGlucosa", objeto = lecturaglucosa, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_health/lecturaglucosas/" + str(lecturaglucosa['id']), fecha_iso_to_js = fecha_iso_to_js , des_convertir_acentos = des_convertir_acentos)
    return template("xpd_health/editar_LecturaGlucosa", objeto = lecturaglucosa, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_health/lecturaglucosas/" + str(lecturaglucosa['id']), fecha_iso_to_js = fecha_iso_to_js, des_convertir_acentos = des_convertir_acentos )

CONFIG['rutas'].append({'ruta':'/lecturaglucosas/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_lecturaglucosa })

def servir_page_insertar_lecturaglucosa(id_sujeto):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    sujeto, id_usuario_owner = sujeto_getowner( conexion , id_sujeto)
    conexion.close()
    if sujeto is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )

    lecturaglucosa = LecturaGlucosas.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_health/editar_LecturaGlucosa", objeto = lecturaglucosa, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_health/sujetos/" + str(id_sujeto), fecha_iso_to_js = fecha_iso_to_js, des_convertir_acentos = des_convertir_acentos)
    # A partir de este punto se asume POST
    mensajes_error = []

    lecturaglucosa['id_sujeto'] = id_sujeto

    lecturaglucosa["fecha_hora"] = request.forms.get( "fecha_hora", "").strip()
        
    if len(lecturaglucosa["fecha_hora"]) == 0:
        mensajes_error.append("fecha_hora es requerido")

    lecturaglucosa["valor"] = request.forms.get( "valor", "").strip()
        
    if len(lecturaglucosa["valor"]) == 0:
        mensajes_error.append("valor es requerido")

    try:
        lecturaglucosa["valor"] = float( lecturaglucosa["valor"] )
    except:
        mensajes_error.append("El valor de valor no es válido")

    lecturaglucosa["observacion"] = request.forms.get( "observacion", "").strip()
        
    lecturaglucosa["observacion"] = convertir_acentos( lecturaglucosa["observacion"] )
    if len(lecturaglucosa["observacion"]) > 256:
        mensajes_error.append("El tamaño de observacion excede el permitido")

    if len(mensajes_error) > 0:
        return template("xpd_health/editar_LecturaGlucosa", objeto = lecturaglucosa, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_health/sujetos/" + str(id_sujeto), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(LecturaGlucosas.insertar, lecturaglucosa)
    except:
        return template("xpd_health/editar_LecturaGlucosa", objeto = lecturaglucosa, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_health/sujetos/" + str(id_sujeto), fecha_iso_to_js = fecha_iso_to_js, des_convertir_acentos = des_convertir_acentos )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_health/lecturaglucosas/" + str(lecturaglucosa['id']) )

CONFIG['rutas'].append({'ruta':'/sujetos/<id_sujeto>/nuevolecturaglucosa', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_lecturaglucosa })

def servir_page_eliminar_lecturaglucosa(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    lecturaglucosa, id_usuario_owner = lecturaglucosa_getowner( conexion , id)
    conexion.close()
    if lecturaglucosa is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method != "GET":
        abort( 404, "Metodo no Valido" )
    try:
        transaccionar(LecturaGlucosas.eliminar, lecturaglucosa)
    except:
    
        return template("xpd_usr/mensaje", lvl = "danger", mensaje = "Error al eliminar objeto.", href ="/xpd_health/Sujetos/" + str(lecturaglucosa['id_Sujeto']) )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_health/Sujetos/" + str(lecturaglucosa['id_Sujeto']) )
    
CONFIG['rutas'].append({'ruta':'/lecturaglucosas/<id>/eliminar', 'metodos':['GET','POST'], 'funcion': servir_page_eliminar_lecturaglucosa })

def servir_page_get_lecturaglucosa_byid(id_lecturaglucosa):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    

    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = lecturaglucosa_getowner(conexion, id_lecturaglucosa)
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    
    conexion.close()
    return template("xpd_health/show_lecturaglucosa", objeto = objeto, usuario = usuario )

CONFIG['rutas'].append({'ruta':'/lecturaglucosas/<id_lecturaglucosa>', 'metodos':['GET'], 'funcion': servir_page_get_lecturaglucosa_byid })

def servir_page_editar_dosisinsulina(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    dosisinsulina, id_usuario_owner = dosisinsulina_getowner( conexion , id)
    conexion.close()
    if dosisinsulina is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method == "GET":        
        return template("xpd_health/editar_DosisInsulina", objeto = dosisinsulina, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_health/dosisinsulinas/" + str(dosisinsulina['id']), fecha_iso_to_js = fecha_iso_to_js, des_convertir_acentos = des_convertir_acentos)
    # A partir de este punto se asume POST
    mensajes_error = []

    dosisinsulina["fecha_hora"] = request.forms.get( "fecha_hora", "").strip()
        
    if len(dosisinsulina["fecha_hora"]) == 0:
        mensajes_error.append("fecha_hora es requerido")

    try:
        if len(dosisinsulina["fecha_hora"]) > 0:
            dosisinsulina["fecha_hora"] = fecha_js_to_iso(dosisinsulina["fecha_hora"])
    except:
        mensajes_error.append("fecha_hora no es una fecha válida")

    dosisinsulina["unidades_aplicadas"] = request.forms.get( "unidades_aplicadas", "").strip()
        
    if len(dosisinsulina["unidades_aplicadas"]) == 0:
        mensajes_error.append("unidades_aplicadas es requerido")

    try:
        dosisinsulina["unidades_aplicadas"] = int( dosisinsulina["unidades_aplicadas"] )
    except:
        mensajes_error.append("El valor de unidades_aplicadas no es válido")

    dosisinsulina["observacion"] = request.forms.get( "observacion", "").strip()
        
    if len(dosisinsulina["observacion"]) == 0:
        mensajes_error.append("observacion es requerido")

    if len(dosisinsulina["observacion"]) > 128:
        mensajes_error.append("El tamaño de observacion excede el permitido")

    if len(mensajes_error) > 0:
        return template("xpd_health/editar_DosisInsulina", objeto = dosisinsulina, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_health/dosisinsulinas/" + str(dosisinsulina['id']), fecha_iso_to_js = fecha_iso_to_js , des_convertir_acentos = des_convertir_acentos)    
    try:
        transaccionar(DosisInsulinas.actualizar, dosisinsulina)
    except:
        return template("xpd_health/editar_DosisInsulina", objeto = dosisinsulina, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_health/dosisinsulinas/" + str(dosisinsulina['id']), fecha_iso_to_js = fecha_iso_to_js , des_convertir_acentos = des_convertir_acentos)
    return template("xpd_health/editar_DosisInsulina", objeto = dosisinsulina, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = "/xpd_health/dosisinsulinas/" + str(dosisinsulina['id']), fecha_iso_to_js = fecha_iso_to_js, des_convertir_acentos = des_convertir_acentos )

CONFIG['rutas'].append({'ruta':'/dosisinsulinas/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_dosisinsulina })

def servir_page_insertar_dosisinsulina(id_sujeto):

    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    sujeto, id_usuario_owner = sujeto_getowner( conexion , id_sujeto)
    conexion.close()
    if sujeto is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )

    dosisinsulina = DosisInsulinas.nuevoDiccionario()
    if request.method == "GET":        
        return template("xpd_health/editar_DosisInsulina", objeto = dosisinsulina, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = "/xpd_health/sujetos/" + str(id_sujeto), fecha_iso_to_js = fecha_iso_to_js, des_convertir_acentos = des_convertir_acentos)
    # A partir de este punto se asume POST
    mensajes_error = []

    dosisinsulina['id_sujeto'] = id_sujeto

    dosisinsulina["fecha_hora"] = request.forms.get( "fecha_hora", "").strip()
        
    if len(dosisinsulina["fecha_hora"]) == 0:
        mensajes_error.append("fecha_hora es requerido")

    dosisinsulina["unidades_aplicadas"] = request.forms.get( "unidades_aplicadas", "").strip()
        
    if len(dosisinsulina["unidades_aplicadas"]) == 0:
        mensajes_error.append("unidades_aplicadas es requerido")

    try:
        dosisinsulina["unidades_aplicadas"] = int( dosisinsulina["unidades_aplicadas"] )
    except:
        mensajes_error.append("El valor de unidades_aplicadas no es válido")

    dosisinsulina["observacion"] = request.forms.get( "observacion", "").strip()
        
    if len(dosisinsulina["observacion"]) == 0:
        mensajes_error.append("observacion es requerido")

    dosisinsulina["observacion"] = convertir_acentos( dosisinsulina["observacion"] )
    if len(dosisinsulina["observacion"]) > 128:
        mensajes_error.append("El tamaño de observacion excede el permitido")

    if len(mensajes_error) > 0:
        return template("xpd_health/editar_DosisInsulina", objeto = dosisinsulina, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = "/xpd_health/sujetos/" + str(id_sujeto), fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar(DosisInsulinas.insertar, dosisinsulina)
    except:
        return template("xpd_health/editar_DosisInsulina", objeto = dosisinsulina, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = "/xpd_health/sujetos/" + str(id_sujeto), fecha_iso_to_js = fecha_iso_to_js, des_convertir_acentos = des_convertir_acentos )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_health/dosisinsulinas/" + str(dosisinsulina['id']) )

CONFIG['rutas'].append({'ruta':'/sujetos/<id_sujeto>/nuevodosisinsulina', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_dosisinsulina })

def servir_page_eliminar_dosisinsulina(id):
    usuario = xpd_usr.getCurrentUser(request)

    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    conexion = orm.Conexion(PATH_BDD)
    dosisinsulina, id_usuario_owner = dosisinsulina_getowner( conexion , id)
    conexion.close()
    if dosisinsulina is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
    
    if request.method != "GET":
        abort( 404, "Metodo no Valido" )
    try:
        transaccionar(DosisInsulinas.eliminar, dosisinsulina)
    except:
    
        return template("xpd_usr/mensaje", lvl = "danger", mensaje = "Error al eliminar objeto.", href ="/xpd_health/Sujetos/" + str(dosisinsulina['id_Sujeto']) )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/xpd_health/Sujetos/" + str(dosisinsulina['id_Sujeto']) )
    
CONFIG['rutas'].append({'ruta':'/dosisinsulinas/<id>/eliminar', 'metodos':['GET','POST'], 'funcion': servir_page_eliminar_dosisinsulina })

def servir_page_get_dosisinsulina_byid(id_dosisinsulina):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    

    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = dosisinsulina_getowner(conexion, id_dosisinsulina)
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    
    conexion.close()
    return template("xpd_health/show_dosisinsulina", objeto = objeto, usuario = usuario )

CONFIG['rutas'].append({'ruta':'/dosisinsulinas/<id_dosisinsulina>', 'metodos':['GET'], 'funcion': servir_page_get_dosisinsulina_byid })

def servir_page_main():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )

    redirect('/xpd_health/sujetos')    

CONFIG['rutas'].append({'ruta':'/main', 'metodos':['GET'], 'funcion': servir_page_main })

def servir_page_admin_main():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    if 'Administrador' not in usuario['roles']:
        abort(403,"Acceso Denegado")  

    entidades = [

    ]
    return template("xpd_health/main", usuario = usuario, titulo = "Administración", entidades = entidades)

CONFIG['rutas'].append({'ruta':'/admin', 'metodos':['GET'], 'funcion': servir_page_admin_main })

def rutearModulo( app : Bottle, ruta_base : str ):
    CONFIG['RUTA_BASE'] = ruta_base
    for item in CONFIG['rutas']:
        app.route( ruta_base + item['ruta'], method = item['metodos'] )( item['funcion'])
