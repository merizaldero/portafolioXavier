#qpy:webapp:Xpd Avies
#qpy:fullscreen
#qpy://127.0.0.1:8080/

from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, request, response, redirect, TEMPLATE_PATH, abort
from os.path import abspath, dirname, exists
from os.path import join as join_dir
from os import listdir
from os import remove as remove_file
from shutil import move as move_file
import uuid
import json

# import claves
from random import randint

EXTENSION = '.png'

PATHS_CHARACTER = {
    'skinsdb' :  { 'path' : "C:\\Users\\XAVIER\\Documents\\minetest\\mods\\skinsdb\\textures",  'prefijo' : 'character' },
    'mobs_npc' : { 'path' : "C:\\Users\\XAVIER\\Documents\\minetest\\mods\\mobs_npc\\textures", 'prefijo' : 'mobs' },    
}

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
    return template("main", tipo_mensaje ="", mensaje="");

@app.route('/js/<path>')
def servir_js(path):
    redirect("/static/js/" + path)

@app.route('/css/<path>')
def servir_css(path):
    redirect("/static/css/" + path)

@app.route('/grupos')
def listar_grupos():
    return {'lista' : list(PATHS_CHARACTER.keys())}

@app.route('/grupo/<grupo>')
def listar_grupo(grupo):
    if grupo not in PATHS_CHARACTER.keys():
        abort(404, "Grupo no existe")
    grupo_dic = PATHS_CHARACTER[grupo]    
    archivos = [x for x in listdir( grupo_dic['path'] ) if x.startswith(grupo_dic['prefijo']) and x.endswith(EXTENSION) ]
    resultado = []
    for archivo in archivos:
        nombre = ' '.join(archivo[ len(grupo_dic['prefijo']) + 1 : - len(EXTENSION) ].split('-'))
        resultado.append( {'nombre' : nombre, 'path': '/imagen/{0}/{1}'.format(grupo, archivo)} )
    return {'lista': resultado}

@app.route('/imagen/<grupo>/<archivo>')
def obtener_imagen( grupo, archivo):
    if grupo not in PATHS_CHARACTER.keys():
        abort(404, "Grupo no existe")
    grupo_dic = PATHS_CHARACTER[grupo]
    if not exists(join_dir(grupo_dic['path'],archivo)):
        abort(404, "Imagen no existe")
    return static_file(archivo, root = grupo_dic['path'])

@app.route('/nuevo_skin/<grupo>', method = 'GET')
def form_nuevo_skin ( grupo ):
    if grupo not in PATHS_CHARACTER.keys():
        abort(404, "Grupo no existe")
    grupo_dic = PATHS_CHARACTER[grupo]
    
    return template ("nuevo_skin", grupo = grupo, nombre ="", tipo_mensaje="", mensaje="")

@app.route('/nuevo_skin', method = 'POST')
def cargar_nuevo_skin():
    grupo   = request.forms.get('txt_grupo')
    nombre  = request.forms.get('txt_nombre').strip()
    archivo = request.files.get('archivo')

    #guarda archivo temporal
    archivo_temporal = join_dir(dirname(abspath( __file__ )), "upload", str(uuid.uuid4()) + ".png" )
    archivo.save(archivo_temporal);

    if not archivo.filename.endswith(EXTENSION):
        remove_file(archivo_temporal)
        return template ("nuevo_skin", grupo = grupo, nombre = nombre, tipo_mensaje="danger", mensaje="Solo se permite archivos .png")

    if grupo not in PATHS_CHARACTER.keys():
        remove_file(archivo_temporal)
        return template ("nuevo_skin", grupo = grupo, nombre = nombre, tipo_mensaje="danger", mensaje="Grupo no es v&aacute;lido")

    if nombre == "":
        remove_file(archivo_temporal)
        return template ("nuevo_skin", grupo = grupo, nombre = nombre, tipo_mensaje="danger", mensaje="Se requiere Nombre")

    grupo_dic = PATHS_CHARACTER[grupo]
    nombre_archivo = join_dir( grupo_dic['path'], grupo_dic['prefijo'] + '_' + '-'.join( nombre.split() ) + EXTENSION )
    
    move_file(archivo_temporal, nombre_archivo)
    print('Archivo copiado a {0}'.format(nombre_archivo))

    return template("main", tipo_mensaje ="success", mensaje="Se ha cargado el skin {0}".format(nombre));


######### WEBAPP ROUTERS ###############

try:
    server = MyWSGIRefServer(host="127.0.0.1", port="8080")
    app.run(server=server,reloader=False)
except Exception as ex:
    errs = "Exception: %s" % repr(ex)
    print(errs)
