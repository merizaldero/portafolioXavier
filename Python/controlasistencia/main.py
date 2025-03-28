#qpy:webapp:Control Ingreso
#qpy:fullscreen
#qpy://127.0.0.1:8080/static/main.html

from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH
from os.path import abspath, dirname
import controlasistencia as ca

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
    return template('main')

@app.route('/datos')
def get_data():
    promociones = ca.findPromociones()
    asistentes = ca.findAsistentes()

    return {'promociones':promociones, 'asistentes':asistentes}

@app.route('/asistente/<id>', method='POST')
def actualizar_check(id):
    asistente = ca.findAsistenteById(id)
    if asistente is None:
        error(404)
    asistente['chequeo'] = request.forms.get('chequeo')
    ca.actualizarAsistente(asistente)
    return {'estado':'ok'}

@app.route('/inicializar')
def inicializar():
    ca.inicializar()
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
