#qpy:webapp:XPD Modelador
#qpy:fullscreen
#qpy://127.0.0.1:8080/?73

"""
Copyright 2015 Marcelo Xavier Merizalde

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""
Aplicacion Web XPD MODELADOR
"""

from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, request, response
import config
#import GeneradorModelo
import ModeladorDao
import xpdbdd
import os
import os.path
import ModeladorDaoTest
import unittest
import json

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
        #sys.stderr.close()
        import threading 
        threading.Thread(target=self.server.shutdown).start() 
        #self.server.shutdown()
        self.server.server_close() #<--- alternative but causes bad fd exception
        print("# qpyhttpd stop")


######### BUILT-IN ROUTERS ###############
@route('/__exit', method=['GET','HEAD'])
def __exit():
    global server
    server.stop()

@route('/__ping')
def __ping():
    return "ok"

@route ('/__test')
def __test():
    try:
        testRunner = unittest.TextTestRunner()
        testRunner.run( ModeladorDaoTest.ModeladorDaoTestSuite() )
        return "Pruebas Unitarias realizadas\n verificar log"
    except (Exception) as ex:
        return repr(ex)

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=config.WEB_ROOT)

@route('/js/<filepath:path>')
def server_static_js(filepath):
    response.set_header("Cache-control","no-cache")
    response.set_header("Expires","0")
    return static_file(filepath, root=config.WEB_ROOT+"/js")

@route('/css/<filepath:path>')
def server_static_css(filepath):
    if filepath.endswith('.css'):
        return static_file(filepath, root=config.WEB_ROOT+"/css", mimetype="text/css")
    else:
        return static_file(filepath, root=config.WEB_ROOT+"/css")

@route ('/fonts/<filepath:path>')
def server_static_fonts(filepath):
    return static_file(filepath, root=config.WEB_ROOT+"/fonts")
    
@route('/img/<filepath:path>')
def server_static_img(filepath):
    return static_file(filepath, root=config.WEB_ROOT+"/img")

@route ('/getLocalConfig.html',method="POST")
def server_get_localConfig_html ():
    return config.LOCAL_CONFIG

@route('/metamodelos.html')
def server_metamodelos_html ():
    salida = {}
    try:
        lista = ModeladorDao.getMetamodelos()
        salida = {'registros': lista }
    except (Exception) as ex:
        salida = {'error':repr(ex)}
        print(repr(ex))
    return salida

@route('/listaModelos.html')
def server_lista_modelos_html ():
    salida = ("")
    try:
        lista = ModeladorDao.getModelos()
        salida = { 'registros' : lista }
    except (Exception) as ex:
        salida = {'error':repr(ex)}
        print(repr(ex))
    return salida
    
@route('/crearModelo.html', method = "POST")
def server_crear_modelo_html ():
    salida = ("")
    try:
        nombreModelo = request.forms.get("nombreModelo")
        idMetamodelo = int(request.forms.get("idMetamodelo"))
        modelo = ModeladorDao.crearModelo({"idMetamodelo":idMetamodelo,"nombre":nombreModelo})
        salida = modelo
    except (Exception) as ex:
        salida = ("")
        print(repr(ex))
    return salida
    
@route ('/crearObjetoHijo.html',method="POST")
def server_crear_objeto_hijo_html ():
    salida = {}
    try:
        nombre = request.forms.get("nombre")
        idJerarquia = request.forms.get("idJerarquia")
        idObjetoPadre = int(request.forms.get("idObjetoPadre"))
        objetoModelo = ModeladorDao.ObjetoModeloDao().nuevoDiccionario()
        objetoModelo["idObjetoPadre"] = idObjetoPadre
        objetoModelo["nombre"] = nombre
        objetoModelo["idJerarquia"] = idJerarquia
        salida = ModeladorDao.crearObjetoHijo( objetoModelo )
        
    except (Exception) as ex:
        salida = {}
        print(repr(ex))
    return salida
    
@route ('/getAtributosObjeto.html',method="POST")
def server_get_atributos_objeto_html ():
    salida = {}
    try:
        idObjeto = int(request.forms.get("idObjeto"))
        salida = ModeladorDao.getAtributosByObjetoModelo( idObjeto )
        
    except (Exception) as ex:
        salida = {}
        print(repr(ex))
    return salida

@route ('/actualizarAtributos.html',method="POST")
def server_actualizar_atributos_html ():
    salida = {}
    try:
        objetoModelo = { "idObjeto": int( request.forms.get("__idObjeto")) , "nombre":request.forms.get("__nombre") , "descripcion":request.forms.get("__descripcion") , "__atributos":[]}
        for item in request.forms.items():
            if item[0].find("__") != 0:
                objetoModelo["__atributos"].append({"idAtributoMetamodelo":item[0],"valor":item[1]})
        print(str(objetoModelo))
        salida = ModeladorDao. actualizarAtributosObjeto( objetoModelo , None)
    except (Exception) as ex:
        salida = {"__errorCode":3,"__mensajes":[{"idAtributoMetamodelo":"__nombre","mensaje":repr(ex)}]}
        print(repr(ex))
    return salida

@route('/inicializarBase.html', method = "POST")
def server_inicializar_base_html ():
    salida = ("")
    try:
        idMetamodelo = int(request.forms.get("idMetamodelo"))
        if idMetamodelo is None:
            raise Exception ("Ingreso no autorizado")
        if not ModeladorDao.inicializarBase():
            raise Exception ("Error en Inicializacion")
        salida = str("Inicializacion Exitosa")
    except (Exception) as ex:
        salida = ( repr(ex) )
    return salida
    
@route('/regenerarMetamodelo.html', method = "POST")
def server_regenerar_metamodelo_html ():
    salida = ("")
    try:
        idMetamodelo = int(request.forms.get("idMetamodelo"))
        if idMetamodelo is None:
            raise Exception ("Ingreso no autorizado")
        if not ModeladorDao.regenerarMetamodelo():
            raise Exception ("Error en Inicializacion")
        salida = str("Inicializacion Exitosa")
    except (Exception) as ex:
        salida = ( repr(ex) )
    return salida

@route('/getRaizModelo.html',method="POST")
def server_get_raiz_modelo_html ():
    salida = {}
    try:
        idModelo = int(request.forms.get("idModelo"))
        salida = ModeladorDao.getRaizModelo( idModelo )
        print(str(salida))
    except (Exception) as ex:
        salida = {}
        print(repr(ex))
    return salida
    
@route ('/getObjetosByPadre.html',method="POST")
def server_get_objetos_by_padre_html ():
    salida = {}
    try:
        idObjeto = int(request.forms.get("idObjeto"))
        idJerarquia = request.forms.get("idJerarquia")
        salida = {"lista":ModeladorDao.getObjetosModeloByPadre( idObjeto ,idJerarquia ) }
        print(str(salida))
    except (Exception) as ex:
        salida = {}
        print(repr(ex))
    return salida

@route ('/getObjetosByModeloTipo.html',method="POST")
def server_get_objetos_by_modelo_tipo_html ():
    salida = {}
    try:
        idModelo = int(request.forms.get("idModelo"))
        idTipoMetamodelo = request.forms.get("idTipoMetamodelo")
        salida = {"lista":ModeladorDao.getObjetosModeloByModeloTipo( idModelo ,idTipoMetamodelo ) }
        print(str(salida))
    except (Exception) as ex:
        salida = {}
        print(repr(ex))
    return salida
    
@route ('/getGeneradores.html',method="POST")
def server_get_generadores_html ():
    salida = {}
    try:
        idModelo = int(request.forms.get("idModelo"))
        salida = {"lista":ModeladorDao.getGeneradoresByModelo( idModelo ) }
        print(str(salida))
    except (Exception) as ex:
        salida = {}
        print(repr(ex))
    return salida
    
@route ('/generarModelo.html',method="POST")
def server_generar_modelo_html ():
    archivoSalida = {}
    try:
        print("inicia generarModelo")
        if config.DEBUG_MODE:
            print (request.forms.get("idModelo"))
        
        idModelo = int(request.forms.get("idModelo"))
        idGenerador = request.forms.get("idGenerador")
        
        archivoSalida = ModeladorDao.generarModelo(idModelo, idGenerador)

        #archivoSalida = GeneradorModelo.generarModelo(idModelo,idGenerador)
        #print (str(archivoSalida))
        return archivoSalida
        # return static_file( archivoSalida["fileName"] , root=config.TEMP_ROOT, mimetype= archivoSalida["mimeType"] )
        
    except (Exception) as ex:
        print(repr(ex))
        return {"error":"Error al recuperar modelo"}
                
@route ('/getParches.html',method="POST")
def server_get_parches_html ():
    salida = {}
    try:
        incluirAplicados = int(request.forms.get("incluirAplicados"))
        salida = {"__lista":ModeladorDao.getParches( incluirAplicados ) }
        print(str(salida))
    except (Exception) as ex:
        salida = {}
        print(repr(ex))
    return salida

@route ('/verificarParche.html',method="POST")
def server_verificar_parche_html ():
    salida = {}
    try:
        archivoParche = request.forms.get("archivoParche")
        salida = ModeladorDao.verificarParche( archivoParche )
        print(str(salida))
    except (Exception) as ex:
        salida = {}
        print(repr(ex))
    return salida
    
@route ('/aplicarParche.html',method="POST")
def server_aplicar_parche_html ():
    salida = ("")
    try:
        archivoParche = request.forms.get("archivoParche")
        salida = ModeladorDao.aplicarParche( archivoParche )
        if config.DEBUG_MODE:
            print(salida)
    except (Exception) as ex:
        salida = (repr(ex))
        print(repr(ex))
    return salida
    
@route ('/exportarModelo.html',method="POST")
def server_exportar_modelo_html ():
    salida = ("")
    try:
        idModelo = int(request.forms.get("idModelo"))
        bandera_descargar = request.forms.get("descargar")
        nombreArchivo = request.forms.get("path")
        print("exportando modelo %d" % idModelo)
        modelo = ModeladorDao.exportarModelo(idModelo,nombreArchivo)
        salida = json.dumps( modelo, sort_keys = False, indent = 2, separators = (',',':') )
        if config.DOWNLOAD_ENABLED and bandera_descargar == '1':
            response.set_header("Content-Type","text/txt")
            response.add_header("content-disposition","attachment ;filename=%s.txt" % modelo["nombre"] );
        if config.DEBUG_MODE:
            print(salida)
    except (Exception) as ex:
        salida = ("Error al exportar modelo: "+repr(ex))
        print(repr(ex))
    return salida

@route ('/eliminarObjeto.html',method="POST")
def server_eliminar_objeto_html ():
    salida = ("")
    try:
        idObjeto = int(request.forms.get("idObjeto"))
        salida = str(ModeladorDao.eliminarObjeto( idObjeto , None ) )
        if config.DEBUG_MODE:
            print("RESULTADO ELIMINAR: %s"%salida)
    except (Exception) as ex:
        salida = (repr(ex))
        print(repr(ex))
    return salida
    
@route ('/moverObjeto.html',method="POST")
def server_mover_objeto_html ():
    salida = ("")
    try:
        idObjeto = int(request.forms.get("idObjeto"))
        moverArriba = int(request.forms.get("moverArriba"))
        salida = str(ModeladorDao.moverObjeto( idObjeto , moverArriba ) )
        if config.DEBUG_MODE:
            print("RESULTADO Mover: %s"%salida)
    except (Exception) as ex:
        salida = (repr(ex))
        print(repr(ex))
    return salida
    
@route ('/importarModelo.html',method="POST")
def server_importar_modelo_html ():
    salida = ("")
    strImport =("")
    fileImport = None
    try:
        nombreArchivo = request.forms.get("nombreArchivo")
        if nombreArchivo is None:
            fileImport = request.files.get("modeloImportado").file
            strImport = fileImport.read().decode("utf-8")
        else:
            fileImport = open( "%s/%s"%(config.FS_ROOT,nombreArchivo) ,'r')
            strImport = fileImport.read()
        jsonModelo = json.loads(strImport)
        salida = str(ModeladorDao.importarModelo( jsonModelo ) )
    except (Exception) as ex:
        salida = (repr(ex) +  "*" +strImport )
        print(repr(ex))
    finally:
        if not(fileImport is None):
            fileImport.close()
            fileImport = None
    return salida
    
######### DIALOGO ARCHIVOS #########

@route ('/listarFs.html',method="POST")
def server_listar_fs_html ():
    salida = {}
    try:
        folder = request.forms.get("folder")
        if folder is None:
          folder = config.FS_ROOT
        else:
          folder = config.FS_ROOT + "/" + folder
        print("obteniendolistado de %s"%folder)
        archivos = os.listdir( folder )
        salida["lista"] = []
        if folder != config.FS_ROOT :
            salida["lista"].append({"tipo":"padre","archivo":".."})
        
        for archivo in archivos:
            if os.path.isdir( folder+"/"+archivo ):
                salida["lista"].append({"tipo":"dir","archivo":archivo})
            else:
                salida["lista"].append({"tipo":"arch","archivo":archivo})
    except (Exception) as ex:
        salida["error"] = repr(ex)
    print(str(salida))
    return salida

@route ('/catalogos.html',method="POST")
def server_get_catalogo_valor_html ():
    salida = {}
    try:
        idModelo = int(request.forms.get("idModelo"))
        salida = ModeladorDao.getCatalogoByModelo( idModelo )
        print(str(salida))
    except (Exception) as ex:
        salida = {}
        print(repr(ex))
    return salida

@route ('/validarModelo.html',method="POST")
def server_validar_modelo ():
    salida = {}
    try:
        idModelo = int(request.forms.get("idModelo"))
        salida = {'lista' : ModeladorDao.validarModelo( idModelo ) }
        print(str(salida))
    except (Exception) as ex:
        salida = {'error': repr(ex) }
        print(repr(ex))
    return salida


######### WEBAPP ROUTERS ###############
@route('/')
def home():
    return server_static("modelador.html")
    #return template('<h1>Hello {{name}} !</h1><a href="/assets/default.html">View source</a><br /> <a href="/js/controles.js">javascript</a> <br /> <a href="javascript:milib.close()">>> Exit</a><br /><a href="http://wiki.qpython.org/doc/program_guide/web_app/">>> About QPython Web App</a>',name='QPython')


######### WEBAPP ROUTERS ###############
app = Bottle()
app.route('/', method='GET')(home)
app.route('/__exit', method=['GET','HEAD'])(__exit)
app.route('/__ping', method=['GET','HEAD'])(__ping)
app.route('/__test', method=['GET','HEAD'])(__test)
app.route ('/getLocalConfig.html',method="POST") ( server_get_localConfig_html )
app.route('/static/<filepath:path>', method='GET')(server_static)
app.route('/js/<filepath:path>', method='GET')(server_static_js)
app.route('/css/<filepath:path>', method='GET')(server_static_css)
app.route('/fonts/<filepath:path>', method='GET')(server_static_fonts)
app.route('/img/<filepath:path>', method='GET')(server_static_img)
app.route('/metamodelos.html', method='GET')( server_metamodelos_html )
app.route('/listaModelos.html', method='GET')( server_lista_modelos_html )
app.route('/crearModelo.html', method='POST')( server_crear_modelo_html )
app.route('/inicializarBase.html', method='POST')( server_inicializar_base_html )
app.route('/regenerarMetamodelo.html', method='POST')( server_regenerar_metamodelo_html )
app.route('/getRaizModelo.html',method="POST")( server_get_raiz_modelo_html )
app.route('/getObjetosByPadre.html',method="POST")( server_get_objetos_by_padre_html )
app.route('/getObjetosByModeloTipo.html',method="POST")( server_get_objetos_by_modelo_tipo_html )
app.route('/crearObjetoHijo.html',method="POST")( server_crear_objeto_hijo_html )
app.route('/getAtributosObjeto.html',method="POST") ( server_get_atributos_objeto_html )
app.route('/actualizarAtributos.html',method="POST") ( server_actualizar_atributos_html )
app.route('/getGeneradores.html',method="POST") ( server_get_generadores_html )
app.route('/generarModelo.html',method="POST") ( server_generar_modelo_html )
app.route ('/getParches.html',method="POST") ( server_get_parches_html )
app.route ('/verificarParche.html',method="POST") ( server_verificar_parche_html )
app.route ('/aplicarParche.html',method="POST") ( server_aplicar_parche_html )
app.route ('/exportarModelo.html',method="POST") ( server_exportar_modelo_html )
app.route ('/eliminarObjeto.html',method="POST") ( server_eliminar_objeto_html )
app.route ('/moverObjeto.html',method="POST") ( server_mover_objeto_html )
app.route ('/importarModelo.html',method="POST") ( server_importar_modelo_html )
app.route ('/listarFs.html',method="POST") ( server_listar_fs_html )
app.route ('/catalogos.html',method="POST") ( server_get_catalogo_valor_html )
app.route ('/validarModelo.html',method="POST") ( server_validar_modelo )

try:
    server = MyWSGIRefServer(host="127.0.0.1", port="8081")
    app.run(server=server,reloader=False)
except (Exception) as ex:
    print("Exception: %s" % repr(ex))


