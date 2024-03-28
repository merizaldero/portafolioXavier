#qpy:webapp:Almacen de Carve
#qpy://127.0.0.1:8080/
"""
This is a sample for qpython webapp
"""
import socket
from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH
from BottleSessions import BottleSessions

from bottle.ext.websocket import GeventWebSocketServer

from os.path import abspath, dirname
import pymvu
import pymvu_websocket
import bvh_viewer

from random import randint

import xpd_usr

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

def distorsionar():
    estilos = [ "text-muted" , "text-primary" , "text-success", "text-info", "text-danger", "text-secondary" ]
    return estilos[ randint(0, len(estilos) -1 ) ]

app = Bottle()

######### BUILT-IN ROUTERS ###############
@app.route('/__exit', method=['GET','HEAD'])
def __exit():
    global server
    server.stop()

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root = dirname(abspath(__file__)) + '/static')

@app.route('/salas/<filepath:path>')
def server_static(filepath):
    return static_file(filepath , root = dirname(abspath(__file__)) + '/salas' )

@app.route('/avatares/<filepath:path>')
def server_static(filepath):
    return static_file(filepath , root = dirname(abspath(__file__)) + '/avatares' )

######### WEBAPP ROUTERS WRITE YOUR CODE BELOW###############

@app.route('/')
def home():
    username = xpd_usr.getCurrentUser(request)
    if username is None:
        redirect('/login')
    else:
        redirect('/pymvu/main')

@app.route('/inicializar')
def inicializar():
    xpd_usr.inicializar()
    return 'Inicializacion ok'

xpd_usr.rutearModulo(app, '/security')

pymvu.rutearModulo(app, '/pymvu')

pymvu_websocket.rutearModulo(app, '/sockets')

bvh_viewer.rutearModulo(app, '/bvh','C:\\Users\\XAVIER\\3D Objects')

######### WEBAPP ROUTERS ###############

# app.route('/', method='GET')(home)
# app.route('/__exit', method=['GET','HEAD'])(__exit)
# app.route('/assets/<filepath:path>', method='GET')(server_static)

try:

    # Get the IP address of the hostname
    direccion_ip = "127.0.0.1"
    puerto = 8080

    backing_params = {
        'cache_type': 'SimpleCache', 
        #'host': direccion_ip,
        #'password': None
    }

    BottleSessions(app, session_backing = backing_params, session_secure = False, session_expire = 600 )
    # server = MyWSGIRefServer(host="0.0.0.0", port="8080")
    # app.run(server=server,reloader=False)
    app.run(host = direccion_ip, port = puerto, reloader=False, server = GeventWebSocketServer)
except Exception as ex:
    errs = "Exception: %s" % repr(ex)
    print(errs)



