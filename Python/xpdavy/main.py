#qpy:webapp:Xpd Avies
#qpy:fullscreen
#qpy://127.0.0.1:8080/

import os.path
import xpd_orm as orm
import avy

from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, request, response, redirect, TEMPLATE_PATH, abort
from os.path import abspath, dirname
import uuid
import json

# import claves
from random import randint

TEMPLATE_PATH.append( dirname(abspath( __file__ )) + "/views" )

######### QPYTHON WEB SERVER ###############
class MyWSGIRefServer(ServerAdapter):
    server = None
    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        import threading
        threading.Thread(target=self.server.shutdown).start()
        self.server.server_close()

app = Bottle()

######### BUILT-IN ROUTERS ###############
@app.route('/__exit', method=['GET','HEAD'])
def __exit():
    global server
    server.stop()

@app.route('/static/<filepath:path>')
def server_static(filepath):
    if filepath == 'ingreso.html':
        response.set_cookie('ssn', '')
    return static_file(filepath, root = dirname(abspath(__file__)) + '/static')


######### WEBAPP ROUTERS WRITE YOUR CODE BELOW###############
@app.route('/')
def home():
    #return template('<h1>Hello {{name}} !</h1><a href="/assets/qpython/projects/WebAppSample/main.py">View code</a><br /><br /> <a href="http://edu.qpython.org/qpython-webapp/index.html">>> About QPython Web App</a>',name='QPython')
    redirect("/static/ingreso.html")

@app.route('/inicializar')
def inicializar():
    avy.inicializar()
    return 'Inicializacion ok'

@app.route('/aleatorio/<id_genero:int>.svg')
def aleatorio_png(id_genero):
    conexion =  orm.Conexion(avy.PATH_BDD)
    avatar = avy.generarPrendasByGenero(conexion, id_genero)
    conexion.close()
    salida_svg = avy.generarSvgAvatar(avatar)
    response.add_header('Content-Type','image/svg+xml')
    return salida_svg

def servir_listado(entidad, query, parametros):
    conexion =  orm.Conexion(avy.PATH_BDD)
    lista= entidad.getNamedQuery(conexion,query,parametros)
    conexion.close()
    return {'lista':lista}

@app.route('/api/partes')
def servir_partes():
    return servir_listado(avy.Partes, 'findall', {})

@app.route('/api/generos')
def servir_generos():
    return servir_listado(avy.Generos, 'findall', {})

@app.route('/api/usuarios')
def servir_usuarios():
    return servir_listado(avy.Usuarios, 'findall', {'activo':'1', 'es_admin':'0'})

@app.route('/api/genero/<id_genero:int>/parte/<id_parte:int>/prendas')
def servir_prendasByGenero(id_genero, id_parte):
    conexion =  orm.Conexion(avy.PATH_BDD)
    lista = avy.findPrendasByGeneroParte(conexion, id_genero, id_parte)
    conexion.close()
    return {'lista':lista}

SESIONES = {}

@app.route('/login', method='POST')
def servir_login():
    nombre = request.forms.get('nombre', default='')
    clave = request.forms.get('clave', default='')
    conexion =  orm.Conexion(avy.PATH_BDD)    
    usuarios = avy.Usuarios.getNamedQuery(conexion, 'findLogin',{'nombre':nombre, 'clave':clave })
    if len(usuarios) == 0:
        abort(401, "Sorry, access denied. {0},{1}".format(nombre,clave))
    keys_existentes = [ clave for clave in SESIONES.keys() if SESIONES[clave] == usuarios[0] ]
    for clave in keys_existentes:
        del SESIONES[clave]
    clave = str(uuid.uuid4())
    SESIONES[clave] = usuarios[0]
    return clave

@app.route('/user/info', method='POST')
def servir_userinfo():
    ses = request.forms.get('ses', default='')
    if ses not in SESIONES.keys():
        abort(401, "Sorry, invalid session")
    return SESIONES[ses]

@app.route('/api/user/<id_usuario:int>/avatares')
def servir_AvataresByUsuario(id_usuario):
    conexion =  orm.Conexion(avy.PATH_BDD)
    lista = avy.findAvataresByUsuario(conexion, id_usuario)
    conexion.close()
    return {'lista':lista}

@app.route('/crearavatar', method="POST")
def servir_crearAvatar():
    avatar = None
    sesion = request.forms.get("id_usuario",None)
    if sesion not in SESIONES.keys():
        abort(401, "Sorry, invalid session {0}".format(sesion))
    id_usuario = SESIONES[sesion]['id']
    try:
        id_genero = int(request.forms.get("id_genero","3"))
        avatar = { "id_genero":id_genero, "id_usuario":id_usuario }
        avy.transaccionar(avy.trxCrearAvatar, avatar )        
    except Exception as ex:
        print(repr(ex))
        abort(500, "Se produjo un error en la transaccion")
    redirect("/avatar/{0}".format(avatar['id']))

@app.route('/api/avatar/<id_avatar:int>')
def servir_avatar_json(id_avatar):    
    avatar = avy.findAvatarById(id_avatar)
    if avatar is None:
        abort(404, "Imagen no existe")
    return avatar

@app.route('/imagen/avatar/<id_avatar:int>.svg')
def servir_avatar_svg(id_avatar):    
    avatar = avy.findAvatarById(id_avatar)
    if avatar is None:
        abort(404, "Imagen no existe")
    salida_svg = avy.generarSvgAvatar(avatar)
    response.add_header('Content-Type','image/svg+xml')
    return salida_svg

@app.route('/imagen/avatartemporal', method="POST")
def servir_avatar_temporal_svg():
    archivo = request.files.get('archivo').file
    avatar = json.loads(archivo.read().decode())
    if avatar is None:
        abort(404, "Imagen no existe")
    salida_svg = avy.generarSvgAvatar(avatar)
    response.add_header('Content-Type','image/svg+xml')
    return salida_svg

@app.route('/avatar/<id_avatar:int>')
def servir_crearAvatar(id_avatar):

    return template('avatar')

######### WEBAPP ROUTERS ###############

# app.route('/', method='GET')(home)
# app.route('/__exit', method=['GET','HEAD'])(__exit)
# app.route('/assets/<filepath:path>', method='GET')(server_static)

try:
    server = MyWSGIRefServer(host="127.0.0.1", port="8080")
    app.run(server=server,reloader=False)
except Exception as ex:
    errs = "Exception: %s" % repr(ex)
    print(errs)
