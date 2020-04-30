import sqlite3 as lite 
import sys
import os
import os.path



DEBUG_MODE = False

droid = None

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
            raise xpdException ("Error commit "+repr(ex))
            
    def rollback (self):
        "Reversa los cambios sobre el cursor actual, lo cierra e inicia un nuevo cursor"
        if not (self.conectado()):
            raise XpdException("Conexion cerrada")
        try:
            self.__conexion.rollback()
            self.nuevoCursor()
        except (Exception) as ex:
            raise xpdException ("Error rollback "+repr(ex))
    
    def close (self):
        "Cierra cursor de transaccion y la conexion de base de datos, tal y como esta"
        if not (self.conectado()):
            raise XpdException("Conexion cerrada")
        try:
            self.__conexion.close()
            self.__conexion = None
            self.__cursor = None
        except (Exception) as ex:
            raise xpdException ("Error close "+repr(ex))

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
    #elif tipo == XPDDATE :
    #    return
    elif tipo == XPDBOOLEAN :
        return bool (valor)
    else:
        raise XpdException ("Tipo no soportado")
        
def validarEntrada(valor,tipo):
    "Valida devolviendo True en caso que el valor dado pueda ser convertido al tipo indicado"
    try:
        parseTexto(valor,tipo)
        return True
    except:
        return False

def preguntarSiNo(titulo,texto,valorSi,valorNo,valorCancelar):
    "Retorna True o false de la respuesta de una pregunta con SL4a"
    droid.dialogCreateAlert(titulo, texto )
    droid.dialogSetPositiveButtonText('Si')
    droid.dialogSetNegativeButtonText('No')
    droid.dialogShow()
    response = droid.dialogGetResponse().result
    if DEBUG_MODE:
        print(str (response))
    if 'canceled' in response :
        return valorCancelar
    if ('which' in response) and (response['which'] == 'positive'):
        return valorSi
    return valorNo

def obtenerTexto(titulo,subtitulo,tipo,valorDefecto):
    "Devuelve la entrada de texto obtenida de un prompt usando Sl4a"
    entradaValida = True
    cancelado = False
    valor = str(valorDefecto)
    while True:
        valor = droid.dialogGetInput(titulo,subtitulo,valor).result
        #print (str (valor))
        cancelado = (valor is None)
        entradaValida = validarEntrada(valor,tipo)
        if entradaValida or cancelado:
            break
    resultado = valorDefecto
    if not cancelado:
        resultado = parseTexto(valor,tipo)
    return resultado

def capturarBarCode(dummy):
    "Captura codigo de barras con la camara"
    scan = droid.scanBarcode().result
    if scan is None:
        return None    
    result = str(scan['extras']['SCAN_RESULT'])
    print(result)    
    return result

class EditorDiccionario():
    """Editor de diccionarios utilizando SL4A
    """
    
    def __init__(self, titulo, dicPropiedades):
        "Inicializa editor recibiendo un titulo y un diccionario con el tipo de dato de cada propiedad"
        self.__dicPropiedades = dicPropiedades
        self.__titulo = titulo
        
    def editar(self, diccionario ):
        "Despliega el dialogo SL4A"
        atributos = self.__dicPropiedades.keys()
        atributos2 = []
        for atributo in atributos:
            atributos2 .append (atributo)
        while True:
            labels = []
            for atributo in atributos:
                if type(self.__dicPropiedades[atributo]) == XPDFUNCTION:
                    labels.append (atributo)
                else:
                    #print (str ( self.__dicPropiedades[atributo]))
                    labels.append ( atributo + " : " + diccionario[atributo] )
            droid.dialogCreateAlert( self.__titulo )
            droid.dialogSetItems( labels )
            droid.dialogShow()
            response = droid.dialogGetResponse().result
            resultado = None
            if "item" in response:
                atributoEditar = atributos2[response["item"]]
                if XPDFUNCTION == type(self.__dicPropiedades[atributoEditar]):
                    try:
                        self.__dicPropiedades[atributoEditar](diccionario)
                    except (Exception) as ex:
                        print ("Error al ejecutar llamado a " + str ( self.__dicPropiedades[atributoEditar] ) +":"+ repr(ex) )
                elif XPDBARCODE == self.__dicPropiedades[atributoEditar] :
                    valor = capturarBarCode(None)
                    if not (valor is None):
                        print('barcode ' + valor)
                        diccionario[atributoEditar] = valor
                else:
                    valor = obtenerTexto( atributoEditar , "Ingrese Nuevo valor"  , self.__dicPropiedades[atributoEditar] , diccionario [ atributoEditar ] )
                    diccionario[atributoEditar] = valor
                    print('valor cambiado '+ str( diccionario ))
            else:
                return diccionario

class SeleccionadorDiccionarios:
    def __init__(self,titulo, propiedadDesplegada ):
        self.__titulo = titulo
        self.__propiedadDesplegada = propiedadDesplegada
        self.__opcionesAntesLista = []
        self.__opcionesDespuesLista = []
    
    def setOpcionesAntesLista (self,lista):
        self.__opcionesAntesLista = lista
    
    def setOpcionesDespuesLista (self,lista):
        self.__opcionesDespuesLista = lista
        
    def seleccionar (self, lista):
        listaMostrar = []
        numeroItems = len (lista)
        numeroOpcionesAntes = len ( self.__opcionesAntesLista )
        numeroOpcionesDespues = len ( self.__opcionesDespuesLista )
        for opcion in self.__opcionesAntesLista:
            listaMostrar.append(opcion [0])
        for item in lista:
            listaMostrar.append (item [ self.__propiedadDesplegada])
        for opcion in self.__opcionesDespuesLista:
            listaMostrar.append(opcion[0])
        droid.dialogCreateAlert( self.__titulo )
        droid.dialogSetItems( listaMostrar )
        droid.dialogShow()
        response = droid.dialogGetResponse().result
        resultado = None
        if "item" in response:
            if response["item"] < numeroOpcionesAntes:
                resultado= self.__opcionesAntesLista [response["item"]][1]
            elif response["item"] < numeroItems + numeroOpcionesAntes:
                resultado=lista[ response["item"] - numeroOpcionesAntes ]
            else:
                resultado= self.__opcionesDespuesLista [ response["item"] - numeroOpcionesAntes - numeroItems ][1]
        return resultado

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
    #elif tipo == XPDDATE :
    #    return
    elif propiedad["tipo"] == XPDBOOLEAN :
        return ("CHAR (1)")
    else:
        raise XpdException ("Tipo no soportado")

class DaoBase:
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
            raise XpdException("Error al realizar insercion")
            
    def actualizar(self, conexion, diccionario):
        "Ejecuta Script Sql de actualizacion con diccionario de parametros"
        try:
            cursor = conexion. cursor()
            #print( self.__actualizar + "\n" +str( diccionario))
            cursor.execute( self.__actualizar , diccionario)
        except (Exception) as ex:
            print("Error al realizar update " + repr(ex))
            raise XpdException("Error al realizar update")
            
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
        campos = {}
        camposHash = {}
        self.__ordenCampos = []
        incrementales = []
        pks = []
        createTable = ("")
        selectCampos = ("")
        whereClause = ("")
        camposInsert1 = ("")
        camposInsert2 = ("")
        camposUpdate = ("")
        if DEBUG_MODE:
           print("metamodelo %s"%metamodelo["nombreTabla"])
        for propiedad in metamodelo["propiedades"]:
            if DEBUG_MODE:
                print("procesa propiedad %s "% str(propiedad))
            if createTable != "":
                createTable = (createTable + ",")
                selectCampos = ( selectCampos + ",")
            createTable = ( "%s %s %s" % ( createTable , propiedad["nombreCampo"] , getTipoSql(propiedad) ) )
            selectCampos = ( "%s %s as %s" % ( selectCampos , propiedad["nombreCampo"] , propiedad["nombre"] ) )
            campos[ propiedad["nombre"] ] = propiedad["tipo"]
            camposHash[ propiedad["nombre"] ] = propiedad
            self.__ordenCampos.append ( propiedad["nombre"] )
            if ("incremental" in propiedad) and propiedad["incremental"]:
                incrementales.append ( propiedad["nombre"] )
                createTable = (createTable + " PRIMARY KEY AUTOINCREMENT ")
            elif not ("insert" in propiedad) or propiedad["insert"]:
                # campos que seran insertados
                if camposInsert1 != "":
                    camposInsert1 = ( camposInsert1 + " , ")
                    camposInsert2 = ( camposInsert2 + " , ")
                camposInsert1 = ( "%s %s " % ( camposInsert1 , propiedad["nombreCampo"] ) )
                camposInsert2 = ( "%s :%s " % ( camposInsert2 , propiedad["nombre"] ) )
            if propiedad["pk"]:
                pks.append ( propiedad )
                # campos utilizados para actualizar y eliminar un registro
                if whereClause != "":
                    whereClause = ( whereClause + " AND ")
                whereClause = ( "%s %s = :%s " % ( whereClause , propiedad["nombreCampo"] , propiedad["nombre"] ) )
            elif not("update" in propiedad) or propiedad["update"]:
                # campos que seran actualizados
                if camposUpdate != "":
                    camposUpdate = ( camposUpdate + " , ")
                camposUpdate = ( "%s %s = :%s " % ( camposUpdate , propiedad["nombreCampo"] , propiedad["nombre"] ) )

        
        
        self.setCampos ( campos )
        self.setIncrementales ( incrementales )
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
                whereClause = ("")
                orderClause = ("")
                if "whereClause" in namedQuery:
                    for campoWhere in namedQuery["whereClause"]:
                        if campoWhere in camposHash:
                            if whereClause != "":
                                whereClause = (whereClause + " AND ")
                            whereClause = ("%s %s = :%s" % ( whereClause , camposHash[campoWhere] ["nombreCampo"] , campoWhere ))
                if whereClause != "":
                    whereClause = (" WHERE "+ whereClause )
                if DEBUG_MODE:
                    print("wc %s" % whereClause )
                if "orderBy" in namedQuery:
                    for campoOrder in namedQuery[ "orderBy" ]:
                        
                        if campoOrder in camposHash:
                            #print("campoOrder esta %s"%str(campoOrder))
                            if orderClause != "":
                                orderClause = (orderClause + " , ")
                            orderClause = ("%s %s" % ( orderClause , camposHash[campoOrder] ["nombreCampo"] ))
                if orderClause != "":
                    orderClause = (" ORDER BY %s" % orderClause )
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

def obtenerFileName(modoSave = False):
    baseDir = ("/storage")
    while True:
        archivos = os.listdir(baseDir)
        if baseDir != "/":
            archivos.insert(0,"..")
            if modoSave:
                archivos.insert(1,"<Nuevo Archivo>")
        elif modoSave :
            archivos.insert(0,"<Nuevo Archivo>")
        droid.dialogCreateAlert( baseDir )
        droid.dialogSetItems( archivos )
        droid.dialogShow()
        response = droid.dialogGetResponse().result
        if "canceled" in response:
            return None
        if "item" in response:
            indice = response ["item"]
            archivo = archivos[indice]
            if archivo == "..":
                baseDir = os.path.dirname(baseDir)
            elif modoSave and archivo == "<Nuevo Archivo>":
                archivo = obtenerTexto("Nuevo Archivo","Nombre nuevo Archivo:",XPDSTRING ,"")
                if archivo is None:
                    return None
                archivo = os.path.join(baseDir, archivo)
                return archivo
            else:
                archivo = os.path.join(baseDir, archivo)
                
                if os.path.isdir(archivo):
                    baseDir = archivo
                else:
                    if modoSave:
                        confirma = preguntarSiNo("Sobrescribir Archivo?",archivo,True,False,False)
                        if confirma:
                            return archivo
                    else:
                        return archivo

#print ( str ( obtenerFileName(True) ))

#plantilla dao
#class MetamodelDao(DaoBase):
#    def __init__(self):
#        self.__campos = { "idMetamodelo" : XPDINTEGER , "nombreMetamodelo" : XPDSTRING ,"idObjetoRaiz" : XPDINTEGER }
#        self.__incrementales = [ "idMetamodelo"]
#        self.__createTable = """
#        CREATE TABLE XMMTMD (
#        ID_METAMODELO INTEGER PRIMARY KEY NOT NULL,
#        NOMBRE_METAMODELO VARCHAR(16) NOT NULL,
#        ID_TIPO_RAIZ VARCHAR (16));"""
#        self.__insertar = "INSERT INTO XMMTMD ( NOMBRE_METAMODELO, ID_TIPO_RAIZ ) VALUES ( :nombreMetamodelo , :idObjetoRaiz );"
#        self.__actualizar = "UPDATE XMMTMD SET NOMBRE_METAMODELO = :nombreMetamodelo , ID_TIPO_RAIZ = :idObjetoRaiz WHERE ID_METAMODELO = :idMetamodelo ;"
#        self.__eliminar = "DELETE FROM XMMTMD WHERE ID_METAMODELO = :idMetamodelo ;"

#def mnuCrearModelo(dummy):
#    print("CrearModelo")

#def mnuEditarModelo(dummy):
#    print("EditarModelo")

#def mnuEliminarModelo(dummy):
#    print("EliminarModelo")

#def mnuEditarMetamodelo(dummy):
#    print("EditarMetaModelo")
    
#def mnuCrearMetamodelo(dummy):
#    print("crearMetaModelo")

#def xpdmain():
#    opciones = {"Crear Modelo" : mnuCrearModelo, "Editar Modelo": mnuEditarModelo , "Eliminar modelo": mnuEliminarModelo ,"Editar Metamodelo": mnuEditarMetamodelo , "Crear Metamodelo": mnuCrearMetamodelo , "Capturar cod barra" : capturarBarCode }
#    editor = EditorDiccionario("MENU PRINCIPAL",opciones)
#    editor.editar({})

#xpdmain()