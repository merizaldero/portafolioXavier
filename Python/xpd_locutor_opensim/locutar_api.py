from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH, response
from os.path import dirname, abspath, join, exists
from os import remove as remove_file
import datetime
import xpd_orm as orm
import xpd_usr
from uuid import uuid4
import pyttsx4
import ffmpeg

PATH_BDD = join(dirname(abspath(__file__)) , "data", "base.db")

# entidades
Locuciones = orm.Entidad()
Locuciones.setMetamodelo({
    "nombreTabla":"XL_LOCUCION",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"texto", "nombreCampo":"TEXTO", "tipo":orm.XPDSTRING, "tamano":1028, },
        { "nombre":"mime_type", "nombreCampo":"MIME_TYPE", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"contenido", "nombreCampo":"CONTENIDO", "tipo":orm.XPDLONGBINARY, },
        { "nombre":"duracion", "nombreCampo":"DURACION", "tipo":orm.XPDREAL, 'tamano':3, 'precision':2, },
        { "nombre":"fecha_creacion", "nombreCampo":"FECHA_CREACION", "tipo":orm.XPDDATE },
        { "nombre":"fecha_lectura", "nombreCampo":"FECHA_LECTURA", "tipo":orm.XPDDATE },
        ],
    "namedQueries":[
        { "nombre":"findById", "whereClause":["id",], },
        { "nombre":"findByTexto", "whereClause":["texto",], },
        { "nombre":"findAll", "orderBy":["fecha_lectura",],  },        
        ]
    })

def inicializar():
    entidades = [Locuciones]
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

def servir_locucion(id_locucion):
    fecha_lectura = datetime.datetime.now().isoformat()
    con = orm.Conexion(PATH_BDD)
    locucion = Locuciones.getNamedQuery(con, 'findById',{'id':id_locucion})
    con.close()
    if len(locucion) == 0:
        error(404)
    locucion = locucion[0]
    contenido = locucion['contenido']
    actualizar_flag = bool(request.query.get('actualizar_flag','True'))
    if actualizar_flag:
        locucion['fecha_lectura'] = fecha_lectura
        transaccionar(Locuciones.actualizar, locucion)
    response.add_header('Content-Type',locucion['mime_type'])
    return contenido

def servir_pagina_locucion(id_locucion):
    con = orm.Conexion(PATH_BDD)
    locucion = Locuciones.getNamedQuery(con, 'findById',{'id':id_locucion})
    con.close()
    if len(locucion) == 0:
        error(404)
    locucion = locucion[0]
    return template('xpd_locutor_opensim/locucion', locucion=locucion)

def servir_locuciones():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    con = orm.Conexion(PATH_BDD)
    locuciones = Locuciones.getNamedQuery(con, 'findAll',{})
    con.close()
    if request.method == "GET":
        return template('xpd_locutor_opensim/locuciones', usuario = usuario, locuciones = locuciones, lvl="", mensaje="")

    # Se procesa posteados desde aqui
    accion = request.forms.get("accion","")

    if accion == "Eliminar":        
        ids_locucion = request.forms.getlist("id_locucion")
        if len(ids_locucion) == 0:
            return template('xpd_locutor_opensim/locuciones', usuario = usuario, locuciones = locuciones, lvl="warning", mensaje="No se ha seleccionado items para eliminar.")
        locuciones_eliminar = [ x for x in locuciones if str(x['id']) in ids_locucion ]
        con = orm.Conexion(PATH_BDD)
        try:
            for locucion_eliminar in locuciones_eliminar:
                Locuciones.eliminar(con, locucion_eliminar)
            con.commit()
            locuciones = [x for x in locuciones if x not in locuciones_eliminar]
        except Exception as ex:
            con.rollback()
            return template('xpd_locutor_opensim/locuciones', usuario = usuario, locuciones = locuciones, lvl="danger", mensaje="Se presentó un error al eliminar items")
        finally:
            con.close()
        return template('xpd_locutor_opensim/locuciones', usuario = usuario, locuciones = locuciones, lvl="success", mensaje="{0} Locuciones eliminadas exitosamente.".format(len(locuciones_eliminar)))        

# Callbacks eventos de TTS
LOG_ENABLED = False
def loguear(texto, forzar = False):
    if LOG_ENABLED or forzar:
        fecha = datetime.datetime.now().isoformat()
        print('{0} {1}'.format(fecha,texto)) 

def onStartUtterance(name):
   loguear('starting {0}'.format(name))

def onStartWord(name, location, length):
    loguear('starting word: {0},{1},{2}'.format(name, location, length))

def onFinishUtterance(name, completed):
    loguear('finishing: {0},{1}'.format(name, completed))

def onError(name, exception):
    loguear('error: {0},{1}'.format(name, repr(exception)), forzar=True)

def generar_locucion(texto):
    # realiza reemplazos de acentos
    reemplazos = {'&aacute;':'á', '&eacute;':'é', '&iacute;':'í', '&oacute;':'ó', '&uacute;':'ú', '&ntilde;':'ñ', '&Ntilde;':'Ñ'}
    for clave in reemplazos.keys():
        texto = texto.replace(clave, reemplazos[clave])
    con = orm.Conexion(PATH_BDD)
    locucion = Locuciones.getNamedQuery(con, 'findByTexto',{'texto': texto})
    con.close()
    if len(locucion) > 0:
        locucion = locucion[0]
    else:
        nombre_archivo = join(dirname(abspath(__file__)) , "temp", "{0}.mp3".format(str(uuid4())) )
        try:
            engine = pyttsx4.init()
            engine.connect("started-utterance", onStartUtterance)
            engine.connect("started-word", onStartWord)
            engine.connect("finished-utterance", onFinishUtterance)
            engine.connect("error", onError)
            #if engine.isBusy():
            #    print('El motor de Voz se encuentra ocupado')
            #else:
            voces = engine.getProperty('voices')
            voz = [x for x in voces if 'spanish' in x.name.lower() ] [0]
            #if arg_voz is not None and arg_voz in [x.name for x in voces]:
            #    voz = [x for x in voces if x.name == arg_voz ] [0]
            engine.setProperty('voice', voz.id)
            engine.save_to_file(texto, nombre_archivo)
            engine.runAndWait()
            loguear("Dicho: {0}".format(texto))
            #obtiene duracion
            probe = ffmpeg.probe(nombre_archivo)
            stream_audio = [x for x in probe['streams'] if x['codec_type'] == 'audio'][0]
            duracion = round( float( stream_audio['duration'] ), 2 )
            #obtiene contenido
            with open(nombre_archivo, 'rb') as stream_binario:
                contenido = stream_binario.read()
            locucion = {'texto':texto, 'mime_type':'audio/mpeg', 'contenido':contenido, 'duracion':duracion, 'fecha_lectura':None, 'fecha_creacion': datetime.datetime.now().isoformat()}
            transaccionar(Locuciones.insertar, locucion)
        except Exception as ex:
            loguear('Error: {0}'.format(repr(ex)), forzar = True)
            raise ex
        finally:
            if exists(nombre_archivo):
                remove_file(nombre_archivo)
    return locucion

def servir_locutar():
    if request.method == "GET":
        redirect('/static/formulario.html')
    texto = request.forms.get("texto","")
    if len(texto) == 0:
        error(500,"No se ha ingresado texto")
    
    locucion = generar_locucion(texto)

    return template('xpd_locutor_opensim/locucion', locucion=locucion)    

def servir_generar_locucion():
    texto = request.forms.get("texto","")
    if len(texto) == 0:
        error(500,"No se ha ingresado texto")    
    locucion = generar_locucion(texto)
    return str(locucion['id'])


def rutearModulo(app:Bottle, path_base):
    app.route(path_base + '/locutar',method=['GET','POST'])(servir_locutar)
    app.route(path_base + '/locucion/<id_locucion>/play',method=['GET'])(servir_locucion)
    app.route(path_base + '/locucion/<id_locucion>',method=['GET'])(servir_pagina_locucion)
    app.route(path_base + '/locuciones',method=['GET','POST'])(servir_locuciones)
    app.route(path_base + '/generar_locucion',method=['POST'])(servir_generar_locucion)