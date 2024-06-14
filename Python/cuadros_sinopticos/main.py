#qpy:webapp:MineArchitech
#qpy://127.0.0.1:8080/static/demo.html
"""
This is a sample for qpython webapp
"""
import socket
from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH
from BottleSessions import BottleSessions

from os.path import abspath, dirname, join
from os import listdir

import sinopticos

direccion_ip = socket.gethostbyname(socket.gethostname()) # "127.0.0.1"

TEMPLATE_PATH.append( join(dirname(abspath( __file__ )) , "views") )

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
    return static_file(filepath, root = dirname(abspath(__file__)) + '/static')

@app.route('/css/<filepath:path>')
def server_css(filepath):
    return static_file(filepath , root = dirname(abspath(__file__)) + '/css' )

@app.route('/js/<filepath:path>')
def server_js(filepath):
    return static_file(filepath , root = dirname(abspath(__file__)) + '/js' )

######### WEBAPP ROUTERS WRITE YOUR CODE BELOW###############

@app.route('/')
def home():
    redirect('/sinopticos/lista')

sinopticos.rutearModulo(app,'/sinopticos')

######### WEBAPP ROUTERS ###############

# app.route('/', method='GET')(home)
# app.route('/__exit', method=['GET','HEAD'])(__exit)
# app.route('/assets/<filepath:path>', method='GET')(server_static)

try:

    # Get the IP address of the hostname
    
    puerto = 8080

    backing_params = {
        'cache_type': 'SimpleCache', 
        #'host': direccion_ip,
        #'password': None
    }

    BottleSessions(app, session_backing = backing_params, session_secure = False, session_expire = 3600 )
    server = MyWSGIRefServer(host='0.0.0.0', port=puerto)
    app.run(server=server,reloader=False)
except Exception as ex:
    errs = "Exception: %s" % repr(ex)
    print(errs)



