#qpy:webapp:Almacen de Carve
#qpy://127.0.0.1:8080/
"""
This is a sample for qpython webapp
"""
from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH

from os.path import abspath, dirname

import xpd_usr
import locutar_api

from BottleSessions import BottleSessions


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

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root = dirname(abspath(__file__)) + '/static')

######### WEBAPP ROUTERS WRITE YOUR CODE BELOW###############

@app.route('/')
def home():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        redirect('/login')
    else:
        redirect('/xpd_locutor_opensim/locuciones')

xpd_usr.rutearModulo(app, '/security')
locutar_api.rutearModulo(app, '/xpd_locutor_opensim')

######### WEBAPP ROUTERS ###############

# app.route('/', method='GET')(home)
# app.route('/__exit', method=['GET','HEAD'])(__exit)
# app.route('/assets/<filepath:path>', method='GET')(server_static)

if __name__ == '__main__':
    try:
        # Get the IP address of the hostname
        direccion_ip = "0.0.0.0"
        puerto = 80

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



