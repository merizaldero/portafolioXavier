import ModeladorDao
import xpdbdd
import unittest
import config
import os
import json

XPDBASEPATH_back = config.XPDBASEPATH

class DaoTest(unittest.TestCase):
    def setUp(self):
        config.XPDBASEPATH = ( XPDBASEPATH_back + ".test.db" )
        #print("TEST - PATH BASE TEMPORAL EN %s"% config.XPDBASEPATH )
        self.conexion = xpdbdd.Conexion(config.XPDBASEPATH)
        
    def tearDown(self):
        #print ("TEST - CERRANDO CONEXION PRUEBA")
        self.conexion.close()
        self.conexion = None
        config.XPDBASEPATH = XPDBASEPATH_back
        #print("TEST - PATH BASE RESTAURADO A %s"% config.XPDBASEPATH )

class ModeladorDaoTest (unittest.TestCase):
    
    def setUp(self):
        config.XPDBASEPATH = ( XPDBASEPATH_back + ".test.db" )
        #print("TEST - PATH BASE TEMPORAL EN %s"% config.XPDBASEPATH )
        
    def tearDown(self):
        config.XPDBASEPATH = XPDBASEPATH_back
        #print("TEST - PATH BASE RESTAURADO A %s"% config.XPDBASEPATH )

    def testDummy(self):
        print('Prueba dummy exitosa')

    def testInicializarBase (self):
        #os.remove(config.XPDBASEPATH)
        if not (ModeladorDao.inicializarBase() ):
            self.fail ("Error en proceso inicializacion")
    
    def testRegenerarMetamodelo(self):
        if not (ModeladorDao.regenerarMetamodelo() ):
            self.fail ("Error en Regeneracion de metamodelo")
    
    def testAplicarParches (self):
        "Aplica todos los parches presentes y verificar que ninguno este aplicado"
        parches = ModeladorDao.getParches(1)
        preaplicados = []
        parchesFallidos = []
        for parche in parches:
            if ModeladorDao.verificarParche ( parche["archivoParche"] )["aplicado"]:
                preaplicados.append ( parche["archivoParche"] )
            else:
                #el parche "" debe fallar obligatoriamente. los demas NO
                resultado = ModeladorDao.aplicarParche( parche["archivoParche"] )
                if resultado!="1" and parche["archivoParche"] != "parche1.sql" :
                    parchesFallidos.append(parche["archivoParche"])
                elif resultado=="1" and parche["archivoParche"] == "parche1.sql":
                    parchesFallidos.append(parche["archivoParche"])
        if len(preaplicados)>0:
            self.fail("Los parches %s estaban aplicados de antemano"%str(preaplicados))
        if len(parchesFallidos)>0:
            self.fail("Los parches %s fallaron al aplicarse"%str(parchesFallidos))
        
        parches = ModeladorDao.getParches(0)
        # recordar que solo el parche "parche1.sql" no debio aplicarse
        if len(parches)>1:
            self.fail("Los parches %s no fueron aplicados"%str(parches))
    
    def testGetMetamodelos (self):
        lista = ModeladorDao.getMetamodelos()
        if len(lista)==0:
            self.fail("no se pudo recuperar metamodelos")
    
    def testCrearModeloValido (self):
        conteo = len(ModeladorDao.getModelos())
        #if conteo!=0:
        #    self.fail("no se puede recuperar modelos creado por default")
        modeloDao = ModeladorDao.ModeloDao()
        modelo = modeloDao.nuevoDiccionario ()
        modelo["idMetamodelo"] = 1
        modelo["nombre"] = ("ModeloDePrueba")
        modelo = ModeladorDao.crearModelo(modelo)
        if modelo["idModelo"] is None or modelo["idModelo"] == 0:
            self.fail("no se pudo obtener id de Modelo")
        #print ("MODELO CREADO %s"%str (modelo))
        conteo1 = len(ModeladorDao.getModelos())
        if conteo1 !=(conteo + 1):
            self.fail("creación  de modelo no ha alterado contador")
        raizModelo = ModeladorDao.getRaizModelo(modelo["idModelo"])
        if raizModelo is None or raizModelo["idObjeto"] != modelo["idObjetoRaiz"]:
            self.fail("no se recuperó objetoRaiz")
        modelos = ModeladorDao.getModelos()
        if len (modelos) <= 0:
            self.fail("No se puede consultar modelos")
        
    def testCrearObjetoHijoValido (self):
        modelos = ModeladorDao.getModelos()
        modelo = modelos [len (modelos) -1]
        raizModelo = ModeladorDao.getRaizModelo(modelo["idModelo"])
        #print ("BUSCANDO JERARQUIAS PARA METAMODELO %s, tipo %s"%( modelo["idMetamodelo"], raizModelo["idTipoMetamodelo"] ))
        jerarquias = ModeladorDao.getJerarquiasByTipo( modelo["idMetamodelo"] , raizModelo["idTipoMetamodelo"], "1" )
        if len(jerarquias) == 0:
            self.fail("no existen jerarquias para tipo raiz")
        conteoAntes = len( ModeladorDao.getObjetosModeloByPadre(raizModelo["idObjeto"], jerarquias[0]["idJerarquia"]) )
        objetosAnadir = 5
        while objetosAnadir > 0:
            objetosAnadir = objetosAnadir - 1
            objetoModelo = ModeladorDao.ModeloDao().nuevoDiccionario()
            objetoModelo ["idModelo"] = modelo ["idModelo"]
            objetoModelo ["idTipoMetamodelo"] = jerarquias[0] ["idTipoMetamodeloHijo"]
            objetoModelo ["idObjetoPadre"] = raizModelo["idObjeto"]
            objetoModelo ["idJerarquia"] = jerarquias[0] ["idJerarquia"]
            objetoModelo ["nombre"] = ("nuevo%s"% objetoModelo ["idTipoMetamodelo"] )
            objetoModelo ["orden"] = 0
            objetoModelo ["descripcion"] = ("")
            objetoModelo = ModeladorDao.crearObjetoHijo(objetoModelo)
            if objetoModelo is None or not ("idObjeto" in objetoModelo ) or objetoModelo["idObjeto"] == 0:
                self.fail("objeto modelo creado incorrectamente")
            objetoModelo = ModeladorDao.getAtributosByObjetoModelo( objetoModelo["idObjeto"] )
            if objetoModelo is None or not ("idObjeto" in objetoModelo ) or not ("_atributos" in objetoModelo) or objetoModelo["idObjeto"] == 0:
                self.fail("objeto no puede recuperar atributos")
            diccionarioAtributos = ModeladorDao.getDiccionarioAtributosByObjetoModelo( objetoModelo["idObjeto"] )
            if diccionarioAtributos is None or not ("nombreTabla" in diccionarioAtributos ):
                self.fail("objeto no puede recuperar atributos(1)")
            #print(str( diccionarioAtributos))
        listaAntesCambio = ModeladorDao.getObjetosModeloByPadre(raizModelo["idObjeto"], jerarquias[0]["idJerarquia"])
        conteoDespues = len ( listaAntesCambio)
        if conteoDespues != (conteoAntes + 5):
            self.fail("creacion de hijos no consistente")
        if "1" != ModeladorDao.moverObjeto ( listaAntesCambio[2]["idObjeto"] ,1):
            self.fail("falla Cambio Orden")
        listaDespuesCambio = ModeladorDao.getObjetosModeloByPadre(raizModelo["idObjeto"], jerarquias[0]["idJerarquia"])
        if listaAntesCambio [2]["idObjeto"] != listaDespuesCambio [1]["idObjeto"] :
            self.fail("moverArriba no fue efectivo")
        if "1" != ModeladorDao.moverObjeto ( listaAntesCambio[2]["idObjeto"] ,0):
            self.fail("falla Cambio Orden 1")
        listaDespuesCambio = ModeladorDao.getObjetosModeloByPadre(raizModelo["idObjeto"], jerarquias[0]["idJerarquia"])
        if listaAntesCambio [2]["idObjeto"] != listaDespuesCambio [2]["idObjeto"] :
            self.fail("moverAbajo no fue efectivo")
        # verifica items del tipo creado
        listaDespuesCambio = ModeladorDao.getObjetosModeloByModeloTipo( modelo['idModelo'] , jerarquias[0] ["idTipoMetamodeloHijo"] )
        if len(listaDespuesCambio) == 0:
            self.fail("fallo al obtener elementos por modelo y tipo")
        
    def testActualizarAtributosObjeto (self):
        modelos = ModeladorDao.getModelos()
        modelo = modelos [len (modelos) -1]
        raizModelo = ModeladorDao.getRaizModelo(modelo["idModelo"])
        objetoModelo = ModeladorDao.getObjetosModeloByPadre(raizModelo["idObjeto"],"Entidades")[0]
        objetoModelo = ModeladorDao.getAtributosByObjetoModelo( objetoModelo["idObjeto"] )
        #print (str (objetoModelo))
        objetoModelo["nombre"] = ("ABC")
        objetoModelo["descripcion"] = ("CDE")
        objetoModelo["__atributos"] = objetoModelo["_atributos"]
        objetoModelo["__atributos"] [0]["valor"] = ("ABC")
        objetoModelo1 = ModeladorDao.actualizarAtributosObjeto(objetoModelo,None)
        if objetoModelo1["__errorCode"] != 0:
            self.fail("error act atributos")
        objetoModelo1 = ModeladorDao.getAtributosByObjetoModelo( objetoModelo["idObjeto"] )
        if objetoModelo["nombre"] != objetoModelo1["nombre"]:
            self.fail("error al actualizar nombre")
        if objetoModelo["descripcion"] != objetoModelo1["descripcion"]:
            self.fail("error al actualizar descripcion")
        if objetoModelo["_atributos"][0]["valor"] != objetoModelo1["_atributos"][0]["valor"] :
            self.fail("error al actualizar atributo")
    
    def testGeneradoresEntidad (self):
        modelos = ModeladorDao.getModelos()
        modelo = modelos [len (modelos) -1]
        generadores = ModeladorDao.getGeneradoresByModelo(modelo["idModelo"])
        if generadores is None or len(generadores) == 0:
            self.fail("error recuperando Generadores para Entidades")
        for generador in generadores:
            self.testGenerador(generador,modelo)
        generador = ModeladorDao.getModeloGenerador(modelo ["idModelo"],generadores[0]["idGenerador"])
        if generador is None:
            self.fail("error recuperando generador individual")
        self.testGenerador(generador,modelo)
            
    def testGenerador (self, generador, modelo):
        pass
        
    def testExportarImportar (self):
        "exporta el primer modelo para importarlo"
        nombreArchivo = ("Documents/export.txt")
        modelos = ModeladorDao.getModelos()
        modelo = modelos [len (modelos) -1]
        jsonModelo = ModeladorDao.exportarModelo( modelo["idModelo"] , nombreArchivo )
        #print ("Modelo inicial\n%s\n" % str(jsonModelo))
        objetosExportados = len (ModeladorDao.getObjetosByModelo ( modelo["idModelo"] ))
        idModeloImportado = ModeladorDao.importarModelo (jsonModelo)
        jsonModelo = ModeladorDao.exportarModelo( idModeloImportado )
        #print ("Modelo importado\n%s\n" % str(jsonModelo))
        objetosImportados = len (ModeladorDao.getObjetosByModelo ( idModeloImportado ))
        if objetosImportados != objetosExportados:
            self.fail ("Importacion o exportacion fallaron")
    
    def testGenerarScriptSql (self):
        "generacion script"
        archivo = open(config.APP_ROOT + '/test/Seguridad.txt','r')
        strImport = archivo.read()
        #print("JSON "+ strImport[:150])
        jsonModelo = json.loads(strImport)
        idModeloImportado = ModeladorDao.importarModelo (jsonModelo)
        generado = ModeladorDao.generarModelo( idModeloImportado , 'SCRIPT_SQL' )
        #print("TESTGENERARSCRIPTSQL " + repr(generado))
        if generado is None:
            self.fail("respuesta None " )
        if 'error' in generado:
            self.fail("respuesta con error " + generado['error'])
        if not ('archivos' in generado):
            self.fail("respuesta no contiene lista de archivos")
        if len(generado['archivos']) == 0:
            self.fail("no se generaron archivos")
        if not ('create table' in generado['archivos'][0]['contenido']) :
            self.fail("contenido de archivo no esperado")
            
    def testValidarModelo(self):
        modelos = ModeladorDao.getModelos()
        #primer modelo estara incompleto
        modelo = modelos [0]
        
        validaciones = ModeladorDao.validarModelo( modelo['idModelo'] )
        
        if len(validaciones ) == 0:
            self.fail("se esperaba validaciones")


    
class TipoPrimitivoDaoTest (DaoTest):
    
    def testInit(self):
        dao=ModeladorDao.TipoPrimitivoDao()
        #print(dao.getNamedQuerySql("getAll")+"\n")
            
    def testGetAll (self):
        dao=ModeladorDao.TipoPrimitivoDao()
        lista = dao.getAll( self.conexion )
        if len(lista)==0:
            self.fail ("el listado de Tipos primitivos esta vacio")

class AtributoTipoMetamodeloDaoTest (DaoTest):
    def testInit(self):
        dao=ModeladorDao.AtributoTipoMetamodeloDao()
        #print(dao.getNamedQuerySql("getByTipoMetamodelo")+"\n")
            
    def testGetByTipoMetamodelo (self):
        dao=ModeladorDao.AtributoTipoMetamodeloDao()
        lista = dao.getByTipoMetamodelo( self.conexion , 1, "ENTIDAD")
        if len(lista)==0:
            self.fail ("el listado de Atributos  de metamodelo esta vacio")

class AtributoObjetoDaoTest (DaoTest):
    
    def testInit(self):
        dao=ModeladorDao.AtributoObjetoDao()
        #print(dao.getNamedQuerySql("getByObjeto")+"\n")
            
    def testGetByObjeto (self):
        dao=ModeladorDao.AtributoObjetoDao()
        lista = dao.getByObjeto( self.conexion , 3)
        if len(lista)==0:
            self.fail ("el listado de Atributos  de metamodelo esta vacio")

class CatalogoTest(unittest.TestCase):
    
    def setUp(self):
        config.XPDBASEPATH = ( XPDBASEPATH_back + ".test.db" )
        #print("TEST - PATH BASE TEMPORAL EN %s"% config.XPDBASEPATH )
        
    def tearDown(self):
        config.XPDBASEPATH = XPDBASEPATH_back
        #print("TEST - PATH BASE RESTAURADO A %s"% config.XPDBASEPATH )

    def testGetCatalogos (self):
        lista = ModeladorDao.getCatalogoByModelo(1)
        if len(lista)==0:
            self.fail("no se pudo recuperar catalogo")
        if not ('BOOLEAN' in lista):
            self.fail("falta catslogo boolean")
        if not ('TIPO_PRIM' in lista):
            self.fail("falta catslogo TIPOS PRIMITIVOS")
        if len(lista['BOOLEAN']) < 2:
            self.fail("catslogo boolean incompleto")
        if len(lista['TIPO_PRIM']) < 10:
            self.fail("catslogo tipos primitivos incompleto")


        

def ModeladorDaoTestSuite():
    suite = unittest.TestSuite()
    
    suite.addTest(ModeladorDaoTest("testInicializarBase"))
    suite.addTest(ModeladorDaoTest("testRegenerarMetamodelo"))
    #suite.addTest(ModeladorDaoTest("testAplicarParches"))
    suite.addTest(ModeladorDaoTest("testGetMetamodelos"))
    suite.addTest(ModeladorDaoTest("testCrearModeloValido"))
    suite.addTest(ModeladorDaoTest( "testCrearObjetoHijoValido"))
    suite.addTest(ModeladorDaoTest("testActualizarAtributosObjeto"))
    suite.addTest(ModeladorDaoTest("testGeneradoresEntidad"))
    suite.addTest(ModeladorDaoTest("testExportarImportar"))
    suite.addTest(ModeladorDaoTest("testValidarModelo"))
    suite.addTest(ModeladorDaoTest("testGenerarScriptSql"))
    
    suite.addTest( TipoPrimitivoDaoTest("testInit") )
    
    suite.addTest(TipoPrimitivoDaoTest("testGetAll"))
    suite.addTest( AtributoTipoMetamodeloDaoTest ("testInit") )
    suite.addTest( AtributoTipoMetamodeloDaoTest ("testGetByTipoMetamodelo") )
    suite.addTest( AtributoObjetoDaoTest ("testInit") )
    suite.addTest( AtributoObjetoDaoTest ("testGetByObjeto") )
    
    suite.addTest( CatalogoTest ( 'testGetCatalogos' ) )

    return suite
    

    
#testRunner = unittest.TextTestRunner()
#testRunner.run( ModeladorDaoTestSuite() )


    

    