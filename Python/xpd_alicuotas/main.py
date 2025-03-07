#qpy:webapp:Kanji Trainer II
#qpy://127.0.0.1:8080/
"""
This is a sample for qpython webapp
"""
import socket
from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH

from os.path import abspath, dirname

TEMPLATE_PATH.append( dirname(abspath( __file__ )) + "/views" )

from BottleSessions import BottleSessions

import xpd_usr
import xpd_alicuotas


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

# @app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root = dirname(abspath(__file__)) + '/static')
app.route('/static/<filepath:path>')(server_static)

#@app.route('/')
def server_home():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    redirect('/xpd_alicuotas/main')

app.route('/', method='GET')(server_home)

######### WEBAPP ROUTERS WRITE YOUR CODE BELOW###############

xpd_usr.rutearModulo(app, '/security')
xpd_alicuotas.rutearModulo(app, '/xpd_alicuotas')


######### WEBAPP ROUTERS ###############

app.route('/', method='GET')(server_home)
# app.route('/__exit', method=['GET','HEAD'])(__exit)
# app.route('/assets/<filepath:path>', method='GET')(server_static)

try:

    # Get the IP address of the hostname
    direccion_ip = "0.0.0.0"
    puerto = 8080

    backing_params = {
        'cache_type': 'SimpleCache', 
        #'host': direccion_ip,
        #'password': None
    }
    BottleSessions(app, session_backing = backing_params, session_secure = False, session_expire = 600 )
    server = MyWSGIRefServer(host=direccion_ip, port=puerto)
    app.run(server=server,reloader=False)
except Exception as ex:
    errs = "Exception: %s" % repr(ex)
    print(errs)
