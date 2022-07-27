#qpy:webapp:Visualizador Datos
#qpy:fullscreen
#qpy://127.0.0.1:8004/

from bottle import Bottle, ServerAdapter, run, debug, route, error, static_file,template, request, response, abort
import reporte
import os.path

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

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
        #sys.stderr.close()
        import threading
        threading.Thread(target=self.server.shutdown).start()
        #self.server.shutdown()
        self.server.server_close() #<--- alternative but causes bad fd exception
        print("# qpyhttpd stop")


@route('/__exit', method=['GET','HEAD'])
def __exit():
    global server
    server.stop()

@route('/__ping')
def __ping():
    return "ok"

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root = APP_ROOT+'/static')

@route('/')
def home():
    return static_file("index.html", root = APP_ROOT+'/templates')
    #return template('<h1>Hello {{name}} !</h1><a href="/assets/default.html">View source</a><br /> <a href="/js/controles.js">javascript</a> <br /> <a href="javascript:milib.close()">>> Exit</a><br /><a href="http://wiki.qpython.org/doc/program_guide/web_app/">>> About QPython Web App</a>',name='QPython')

@route('/construir_grafico',method = 'POST')
def construir_grafico():
    if request.method=='GET':
        return "Hola Mundo"
    try:
       print("Inicia proceso ")
       entrada = request.json
       print("json ok " + str(entrada))
       salida = reporte.construir_grafico(entrada)
       response.set_header( 'Content-Type' , 'image/png' )
       return salida.getvalue()
    except Exception as ex:
       abort(500, ex.message)

app = Bottle()
app.route('/', method='GET')(home)
app.route('/static/<filepath:path>', method='GET')(server_static)
app.route('/__exit', method=['GET','HEAD'])(__exit)
app.route('/__ping', method=['GET','HEAD'])(__ping)
app.route('/construir_grafico',method = ['GET','POST'])(construir_grafico)

try:
    server = MyWSGIRefServer(host="127.0.0.1", port="8004")
    app.run(server=server,reloader=False)
except (Exception) as ex:
    print("Exception: %s" % repr(ex))
