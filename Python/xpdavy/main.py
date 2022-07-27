#qpy:webapp:Xpd Avies
#qpy:fullscreen
#qpy://127.0.0.1:8080/

from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, request, response
import os.path
import avy

from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH
from os.path import abspath, dirname
import claves
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
    return static_file(filepath, root = dirname(abspath(__file__)) + '/static')


######### WEBAPP ROUTERS WRITE YOUR CODE BELOW###############
@app.route('/')
def home():
    return template('<h1>Hello {{name}} !</h1><a href="/assets/qpython/projects/WebAppSample/main.py">View code</a><br /><br /> <a href="http://edu.qpython.org/qpython-webapp/index.html">>> About QPython Web App</a>',name='QPython')

@app.route('/inicializar')
def inicializar():
    avy.inicializar()
    return 'Inicializacion ok'




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
