import sqlite3 as lite 
import sys
import os
import os.path
import datetime

DEBUG_MODE = False

class XpdException (Exception):
    "Excepcion lanzada por programas XPD"
    def __init__(self,valor):
        self.__valor = valor
        
    def __str__(self):
        return "XpdException: " + str (self.__valor)

class Conexion:
    "Encapsula transacciones y conexiones de Base de Datos"
    
    def __init__(self, pathBase):
        "Establece conexion de base de datos e inicia un cursor de transaccion"
        paso = 0
        try:
            paso = 1
            self.__conexion = lite.connect(pathBase)
            paso = 2
            self.__cursor = self.__conexion.cursor()
            
        except (Exception) as ex:
            print("Error al establecer conexion " + paso + ":" + repr(ex))
            if not( self.__conexion is None):
                self.__conexion.close ()
            self.__conexion = None
            self.__cursor = None
            
    def conectado (self):
        "Devuelve True si la conexion esta abierta"
        __conectado = not(self.__conexion is None)
        if not __conectado:
            print("Error conexion cerrada")
        return __conectado
        
    def cursor (self):
        "Devuelve cursor de Transaccion actual"
        if not (self.conectado ()):
            raise XpdException("conexion cerrada")
        return self.__cursor
    
    def consultar(self,sqlSelect,parametros,vectorColumnas) :
        """Ejecuta una consulta SQL con los parametros dados.
        El resultado es una lista de Diccionarios cuyas claves son el vector de columnas"""
        #print("inicia consulta " + str(sqlSelect))
        if not (self.conectado ()):
            raise XpdException("conexion cerrada")
        try:
            
            self.__cursor.execute(sqlSelect, parametros)
        except (Exception) as ex:
            #self.__ultimoError = ('error en sql')
            print("error en consulta" + repr(ex))
            raise XpdException("error de consulta")
        resultado = []
        rows = self.__cursor.fetchall()
        #print(str(rows))
        #resultado = rows
        for row in rows:
            if len(vectorColumnas) != len(row):
                print(" número de columnas no es el esperado")
                raise XpdException("número de columnas no es el esperado")
            fila = {}
            #print("lee fila")
            for i in range(0,len(vectorColumnas)):
                #print("asigna " + str(vectorColumnas[i]))
                fila[ vectorColumnas[i] ] = row [ i ]
            resultado.append(fila)
        #self.__ultimoError = None
        return resultado
        
    def consultarEscalar(self,sqlSelect, parametros):
        """Ejecuta una consulta SQL con los parametros provistos.
        El resultado debe ser una fila y una columna."""
        if not (self.conectado()):
            raise XpdException("Conexion cerrada")
        try:
            self.__cursor.execute(sqlSelect, parametros)
            valor = self.__cursor.fetchone()
            #self.__ultimoError = None
            return valor
        except (Exception) as ex:
            raise XpdException("Error en consulta escalar " + repr(ex))
            
    def ejecutarFileScript(self, filePath):
        "Ejecuta los scripts SQL dentro de un archivo"
        if not (self.conectado()):
            raise XpdException("Conexion cerrada")
        archivo = None
        paso = 0
        try:
            archivo = open(filePath,'r')
            paso=paso+1
            contenido = archivo.read()
            if DEBUG_MODE:
                print(str(contenido))
            paso=paso+1
            self.__cursor.executescript(contenido)
            #self.__ultimoError = None
        except (Exception) as ex:
            print("error script %d : %s"%(paso,repr(ex)))
            raise XpdException("Error al ejectutar script")
        finally:
            if not(archivo is None):
                archivo.close()
    
    def nuevoCursor(self):
        """Inicia un nuevo cursor de Transaccion.
        Si existe un cursor previo, lo cierra"""
        if not (self.conectado ()):
            raise XpdException("conexion cerrada")
        self.__cursor = None
        self.__cursor = self.__conexion.cursor()
        #self.__cursor.row_factory=lite.Row
        return self.__cursor
    
    def commit (self):
        "Asienta los cambios sobre el cursor actual lo cierra e inicia un nuevo cursor"
        if not (self.conectado()):
            raise XpdException("Conexion cerrada")
        try:
            self.__conexion.commit()
            self.nuevoCursor()
        except (Exception) as ex:
            raise XpdException ("Error commit "+repr(ex))
            
    def rollback (self):
        "Reversa los cambios sobre el cursor actual, lo cierra e inicia un nuevo cursor"
        if not (self.conectado()):
            raise XpdException("Conexion cerrada")
        try:
            self.__conexion.rollback()
            self.nuevoCursor()
        except (Exception) as ex:
            raise XpdException ("Error rollback "+repr(ex))
    
    def close (self):
        "Cierra cursor de transaccion y la conexion de base de datos, tal y como esta"
        if not (self.conectado()):
            raise XpdException("Conexion cerrada")
        try:
            self.__conexion.close()
            self.__conexion = None
            self.__cursor = None
        except (Exception) as ex:
            raise XpdException ("Error close "+repr(ex))

def __funcionDummy ():
    pass

XPDINTEGER = type (8)
XPDREAL = type (1.1)
XPDSTRING = type("hola")
XPDLONGSTRING = ("XPDLONGSTRING")
XPDDATE = ("date")
XPDBOOLEAN = type (True)
XPDFUNCTION = type( __funcionDummy )
XPDBARCODE = ("BARCODE")
XPDLONGBINARY = "XPDLONGBINARY"

#print (str ({ XPDINTEGER ,XPDLONG, XPDREAL, XPDSTRING , XPDDATE , XPDBOOLEAN }))
#print(str ( type(consultarEscalar) ))

def parseTexto(valor,tipo):
    "Transforma el valor dado en el tipo de dato solicitado"
    if tipo is None:
        raise XpdException ("Tipo no especificado")
    elif tipo == XPDINTEGER :
        return int (valor)
    elif tipo == XPDREAL :
        return float (valor)
    elif tipo == XPDSTRING :
        return str (valor)
    elif tipo == XPDDATE :
        return datetime.datetime.fromisoformat(valor)
    elif tipo == XPDBOOLEAN :
        return bool (valor)
    elif tipo == XPDLONGBINARY :        
        return bytes (valor, 'utf-8')
    else:
        raise XpdException ("Tipo no soportado")
        
def validarEntrada(valor,tipo):
    "Valida devolviendo True en caso que el valor dado pueda ser convertido al tipo indicado"
    try:
        parseTexto(valor,tipo)
        return True
    except:
        return False

def getTipoSql(propiedad):
    if propiedad["tipo"] is None:
        raise XpdException ("Tipo no especificado")
    elif propiedad["tipo"] == XPDINTEGER :
        return ("INTEGER")
    elif propiedad["tipo"] == XPDREAL :
        return ("FLOAT")
    elif propiedad["tipo"] == XPDSTRING :
        if "tamano" in propiedad:
            return ("VARCHAR(%d)"% propiedad["tamano"] )
        else:
            return ("TEXT")
    elif propiedad["tipo"] == XPDDATE :
        return "DATETIME"
    elif propiedad["tipo"] == XPDBOOLEAN :
        return ("CHAR (1)")
    elif propiedad["tipo"] == XPDLONGBINARY :
        return ("BLOB")
    else:
        raise XpdException ("Tipo no soportado")

class Entidad:
    "Manejador Dao Base para una entidad"
    
    def __init__(self):
        "inicializa Dao"
        self.__campos = None
        self.__incrementales = None
        self.__createTable = None
        self.__insertar = None
        self.__actualizar = None
        self.__eliminar = None
    
    def setCampos( self, valor):
        "Asigna listado de campos"
        self.__campos = valor
        
    def getCampos(self):
        "Retorna listado de campos"
        return self.__campos
        
    def setIncrementales ( self, valor):
        "asigna lista de campos incrementales"
        self.__incrementales = valor
    
    def setCreateTable ( self, valor):
        "asigna SQL de creacion/regeneracion de tabla"
        self.__createTable = valor
    
    def setInsertar ( self, valor):
        "Asigna SQL de insercion"
        self.__insertar = valor
        # print(valor)
    
    def setActualizar ( self, valor):
        "Asigna Sql de actualización"
        self.__actualizar = valor
    
    def setEliminar( self, valor):
        "Asigna Sql de eliminacion"
        self.__eliminar = valor
        
    def crearTabla(self, conexion):
        "Ejecuta Sql de creacion/regeneracion de tabla"
        try:
            cursor = conexion.cursor()
            if DEBUG_MODE:
                print("creando tabla")
                print(str(cursor)+"\n"+ self.__createTable )
            cursor.executescript( self.__createTable )
        except (Exception) as ex:
            raise XpdException("Error al crear tabla " + repr(ex))
            
    def nuevoDiccionario(self):
        "Inicializa diccionario con campos especificados"
        resultado = {}
        for clave in self.__campos.keys():
            resultado[clave] = None
        return resultado
        
    def insertar(self, conexion, diccionario):
        "Ejecuta Sql insercion con diccionario de parámetros"
        try:
            cursor = conexion. cursor()
            if DEBUG_MODE:
                print( self.__insertar + "\n" +str( diccionario))
            cursor.execute( self.__insertar , diccionario)
            if DEBUG_MODE:
                print("insercion ok")
            if len (self.__incrementales) == 1:
                diccionario[ self.__incrementales[0]] = cursor.lastrowid
        except (Exception) as ex:
            print("Error al realizar insercion" + repr(ex))
            raise XpdException("Error al realizar insercion " + str(ex) )
            
    def actualizar(self, conexion, diccionario):
        "Ejecuta Script Sql de actualizacion con diccionario de parametros"
        try:
            cursor = conexion. cursor()
            #print( self.__actualizar + "\n" +str( diccionario))
            cursor.execute( self.__actualizar , diccionario)
        except (Exception) as ex:
            print("Error al realizar update " + repr(ex))
            raise XpdException("Error al realizar update " + str(ex) )
            
    def eliminar(self, conexion, diccionario):
        "Ejecuta Sql de eliminación con diccionario  de parámetros"
        try:
            #print("obtiene cursor")
            cursor = conexion. cursor()
            if DEBUG_MODE:
                print( str( diccionario )+"\n"+ self.__eliminar )
            cursor.execute( self.__eliminar , diccionario)
        except (Exception) as ex:
            print("error al eliminar " +repr(ex))
            raise XpdException("Error al realizar delete")
    
    def setMetamodelo(self, metamodelo):
        "setea campos, consultas de creacion, insercion, actualuzacion, eliminacion, y consultas base. a partir de un diccionario de metamodelo"
        
        self.__ordenCampos = [ propiedad["nombre"] 
            for propiedad in metamodelo["propiedades"] 
            ]
        self.setCampos ( { propiedad["nombre"] : propiedad["tipo"] 
            for propiedad in metamodelo["propiedades"] 
            } )
        self.setIncrementales ( [ propiedad["nombre"] 
            for propiedad in metamodelo["propiedades"] 
            if "incremental" in propiedad and propiedad["incremental"] 
            ] )

        camposHash = { propiedad["nombre"] : propiedad for propiedad in metamodelo["propiedades"] }
        pks = [ propiedad 
            for propiedad in metamodelo["propiedades"] 
            if "pk" in propiedad and propiedad["pk"] 
            ]

        selectCampos = ", ".join( [ propiedad["nombre"]+" as "+propiedad["nombre"] 
            for propiedad in metamodelo["propiedades"] 
            ] )
        
        camposInsert1 = ", ".join( [ propiedad["nombreCampo"] 
            for propiedad in metamodelo["propiedades"] 
            if propiedad['nombre'] not in self.__incrementales and (not ("insert" in propiedad) or propiedad["insert"]) 
            ] )
        camposInsert2 = ", ".join( [ ":"+propiedad["nombre"]  
            for propiedad in metamodelo["propiedades"] 
            if propiedad['nombre'] not in self.__incrementales and (not ("insert" in propiedad) or propiedad["insert"]) 
            ] )
        camposUpdate  = ", ".join( [ propiedad["nombreCampo"] + " = :" + propiedad["nombre"]  
            for propiedad in metamodelo["propiedades"] 
            if propiedad not in pks and (not ("update" in propiedad) or propiedad["update"]) 
            ] )
        
        whereClause = " and ".join( [ 
            propiedad["nombreCampo"]+" = :"+propiedad["nombre"] 
            for propiedad in pks 
            ] )
        
        if DEBUG_MODE:
           print("metamodelo %s"%metamodelo["nombreTabla"])
        
        createTable = ""
        
        for propiedad in metamodelo["propiedades"]:
            if DEBUG_MODE:
                print("procesa propiedad %s "% str(propiedad))
            if createTable != "":
                createTable += ","
            createTable += " %s %s" % ( propiedad["nombreCampo"] , getTipoSql(propiedad) ) 
            if propiedad["nombre"] in self.__incrementales :
                createTable = (createTable + " PRIMARY KEY AUTOINCREMENT ")
        
        #xpdbdd.print("marca1CadenaDao")
        self.setCreateTable ("DROP TABLE IF EXISTS %s ;\n CREATE TABLE %s ( %s );" % ( metamodelo["nombreTabla"] , metamodelo["nombreTabla"] , createTable ) )
        
        #xpdbdd.print("marca2CadenaDao")
        self.setInsertar ("INSERT INTO %s ( %s ) VALUES ( %s )" % ( metamodelo["nombreTabla"] , camposInsert1 , camposInsert2 ))
        self.setActualizar ("UPDATE %s SET %s WHERE %s " % ( metamodelo["nombreTabla"] , camposUpdate , whereClause ))
        self.setEliminar ("DELETE FROM %s WHERE %s " % ( metamodelo["nombreTabla"] , whereClause ))
        
        self.__namedQueries = {}
        
        if "namedQueries" in metamodelo:
            for namedQuery in metamodelo ["namedQueries"]:
                if DEBUG_MODE:
                    print("procesa namedQuery %s "% str( namedQuery ))
                whereClause = "" 
                orderClause = ""
                if "whereClause" in namedQuery:
                    whereClause = " and ".join([
                        "{0} = :{1}".format( propiedad["nombreCampo"], propiedad["nombre"] )
                        for campoWhere in namedQuery["whereClause"]
                        for propiedad in metamodelo["propiedades"]
                        if propiedad["nombre"] == campoWhere
                        ])
                if whereClause != "":
                    whereClause = " WHERE " + whereClause
                if DEBUG_MODE:
                    print("wc %s" % whereClause )
                if "orderBy" in namedQuery:
                    orderClause = ", ".join([
                        propiedad["nombreCampo"]
                        for campoOrder in namedQuery[ "orderBy" ]
                        for propiedad in metamodelo["propiedades"]
                        if propiedad["nombre"] == campoOrder
                        ])
                if orderClause != "":
                    orderClause = " ORDER BY " + orderClause
                if DEBUG_MODE:
                    print("ob %s" % orderClause )
                self.__namedQueries[ namedQuery["nombre"] ] = ("SELECT %s FROM %s %s %s" % ( selectCampos , metamodelo["nombreTabla"] , whereClause , orderClause ))
        if DEBUG_MODE:
            print(str(self.__namedQueries))
            print("fin setmetamodelo %s"%metamodelo["nombreTabla"])
    
    def getNamedQuery(self,conexion,namedQuery,parametros):
        "Ejecuta consulta de plantilla"
        #xpdbdd.print("inicia getall \n"+ str(self.__getAll) + "\n" + str(self.getCampos() ))
        return conexion.consultar( self.__namedQueries[namedQuery] , parametros , self.__ordenCampos )
        
    def getNamedQuerySql(self,namedQuery):
        "obtiene sql de plantilla"
        return self.__namedQueries[namedQuery]




#xpdmain()