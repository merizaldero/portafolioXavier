import xpdbdd
import config
from random import randint
import re
import os
import json
import GeneradorModelo

class MetamodeloDao(xpdbdd.DaoBase):
    def __init__(self):
        # Incluido en pruebas
        metamodelo={"nombreTabla":"XMMTMDL","propiedades":[],"namedQueries":[]}
        metamodelo["propiedades"].append({"nombre":"idMetamodelo","nombreCampo":"ID_METAMODELO","incremental":False,"pk":True,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":False,"update":False ,"opcional":True })
        metamodelo["propiedades"].append({"nombre":"nombreMetamodelo","nombreCampo":"NOMBRE_METAMODELO","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":16,"insert": False ,"update": False ,"opcional":False })
        metamodelo["propiedades"].append({"nombre":"idTipoRaiz","nombreCampo":"ID_TIPO_RAIZ","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":32,"insert":False,"update": False ,"opcional":True })
        metamodelo["namedQueries"].append({"nombre":"getAll","whereClause":[],"orderBy":["nombreMetamodelo"]})
        metamodelo["namedQueries"].append({"nombre":"getById","whereClause":["idMetamodelo"],"orderBy":[ ]})

        self.setMetamodelo (metamodelo)
        
    def getAll (self, conexion):
        # Incluido en pruebas
        return self.getNamedQuery(conexion,"getAll",{})

    def getById (self, conexion, idMetamodelo ):
        return self.getNamedQuery(conexion,"getById",{ "idMetamodelo": idMetamodelo }) [0]

class TipoPrimitivoDao(xpdbdd.DaoBase):
    def __init__(self):
        # Incluido en pruebas
        metamodelo={"nombreTabla":"XMTPPRMTV","propiedades":[],"namedQueries":[]}
        metamodelo["propiedades"].append({"nombre":"idTipoPrimitivo","nombreCampo":"ID_TIPO_PRIMITIVO","incremental":False,"pk":True,"tipo":xpdbdd.XPDSTRING,"tamano":12,"insert":False,"update":False,"opcional":False })
        metamodelo["propiedades"].append({"nombre":"requiereLongitud","nombreCampo":"REQUIERE_LONGITUD","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":1,"insert":False,"update":False,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"requierePrecision","nombreCampo":"REQUIERE_PRECISION","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":1,"insert":False,"update":False,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"soportaExpresionRegular","nombreCampo":"SOPORTA_EXPRESION_REGULAR","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":1,"insert":False,"update":False,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"expRegularDefault","nombreCampo":"EXP_REGULAR_DEFAULT","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":1,"insert":False,"update":False,"opcional":True})
        metamodelo["namedQueries"].append({"nombre":"getAll","whereClause":[],"orderBy":["idTipoPrimitivo"]})

        self.setMetamodelo (metamodelo)
    
    def getAll (self, conexion):
        # Incluido en pruebas
        return self.getNamedQuery(conexion,"getAll",{})

class TipoMetamodeloDao(xpdbdd.DaoBase):
    def __init__(self):
        metamodelo={"nombreTabla":"XMTPMTMDL","propiedades":[],"namedQueries":[]}
        metamodelo["propiedades"].append({"nombre":"idMetamodelo","nombreCampo":"ID_METAMODELO","incremental":False,"pk":True,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert": False ,"update":False ,"opcional":False })
        metamodelo["propiedades"].append({"nombre":"idTipoMetamodelo","nombreCampo":"ID_TIPO_METAMODELO","incremental":False,"pk":True,"tipo":xpdbdd.XPDSTRING,"tamano":32,"insert": False ,"update":False,"opcional":False })
        metamodelo["propiedades"].append({"nombre":"nombreTipoMetamodelo","nombreCampo":"NOMBRE_TIPO_METAMODELO","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":32,"insert": False ,"update": False ,"opcional":False})
        metamodelo["namedQueries"].append({"nombre":"getByMetamodelo","whereClause":["idMetamodelo"],"orderBy":["nombreMetamodelo"]})
        
        metamodelo["namedQueries"].append({"nombre":"getById","whereClause":["idMetamodelo","idTipoMetamodelo"],"orderBy":[ ]})

        self.setMetamodelo (metamodelo)
            
    def getByMetamodelo (self, conexion, idMetamodelo ):
        return self.getNamedQuery(conexion,"getByMetamodelo",{"idMetamodelo":idMetamodelo})
    
    def getById (self, conexion, idMetamodelo , idTipoMetamodelo ):
        return self.getNamedQuery(conexion,"getById",{"idMetamodelo":idMetamodelo, "idTipoMetamodelo": idTipoMetamodelo })[0]
    
    
class AtributoTipoMetamodeloDao(xpdbdd.DaoBase):
    def __init__(self):
        # Incluido en pruebas
        metamodelo={"nombreTabla":"XMATRBTMTMDL","propiedades":[],"namedQueries":[]}
        metamodelo["propiedades"].append({"nombre":"idMetamodelo","nombreCampo":"ID_METAMODELO","incremental":False,"pk":True,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":True,"update":False ,"opcional":False })
        metamodelo["propiedades"].append({"nombre":"idTipoMetamodelo","nombreCampo":"ID_TIPO_METAMODELO","incremental":False,"pk":True,"tipo":xpdbdd.XPDSTRING,"tamano":32,"insert":True,"update":False,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"idAtributoMetamodelo","nombreCampo":"ID_ATRIBUTO_METAMODELO","incremental":False,"pk":True,"tipo":xpdbdd.XPDSTRING,"tamano":32,"insert":True,"update":False,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"idTipoPrimitivo","nombreCampo":"ID_TIPO_PRIMITIVO","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":12,"insert":True,"update":True,"opcional":True})
        metamodelo["propiedades"].append({"nombre":"idTipoMetamodeloRef","nombreCampo":"ID_TIPO_METAMODELO_REF","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":32,"insert":True,"update":True,"opcional":True})
        metamodelo["propiedades"].append({"nombre":"esObligatorio","nombreCampo":"ES_OBLIGATORIO","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":1,"insert":True,"update":True,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"longitudAtributo","nombreCampo":"LONGITUD_ATRIBUTO","incremental":False,"pk":False,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":True,"update":True,"opcional":True})
        metamodelo["propiedades"].append({"nombre":"precisionAtributo","nombreCampo":"PRECISION_ATRIBUTO","incremental":False,"pk":False,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":True,"update":True,"opcional":True})
        metamodelo["propiedades"].append({"nombre":"orden","nombreCampo":"ORDEN","incremental":False,"pk":False,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":True,"update":True,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"expRegularValidacion","nombreCampo":"EXP_REGULAR_VALIDACION","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":32,"insert":True,"update":True,"opcional":True})
        metamodelo["propiedades"].append({"nombre":"valorDefecto","nombreCampo":"VALOR_DEFECTO","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":32,"insert":True,"update":True,"opcional":True})
        metamodelo["propiedades"].append( {"nombre" : "idCatalogo",		"nombreCampo" : "ID_CATALOGO",		"incremental" : False,	"pk" : False,	"tipo" : xpdbdd.XPDSTRING,	"tamano" : 16,		"insert" : True,	"update" : True,	"opcional" : True } )
        
        metamodelo["namedQueries"].append({"nombre":"getByTipoMetamodelo","whereClause":["idMetamodelo","idTipoMetamodelo"],"orderBy":["orden"]})

        self.setMetamodelo (metamodelo)
        
        self.__getByTipoMetamodelo = ("""SELECT  
        a.ID_METAMODELO as idMetamodelo, a.ID_TIPO_METAMODELO as idTipoMetamodelo, a.ID_ATRIBUTO_METAMODELO as idAtributoMetamodelo, a.ID_TIPO_PRIMITIVO as idTipoPrimitivo, a.ID_TIPO_METAMODELO_REF as idTipoMetamodeloRef, a.ES_OBLIGATORIO as esObligatorio, a.LONGITUD_ATRIBUTO as longitudAtributo, a.PRECISION_ATRIBUTO as precisionAtributo, a.ORDEN as orden, a.EXP_REGULAR_VALIDACION as expRegularValidacion, a.VALOR_DEFECTO as valorDefecto 
        ,EXP_REGULAR_DEFAULT as expRegularDefault
        , a.ID_CATALOGO as idCatalogo
        FROM XMATRBTMTMDL a
        LEFT JOIN XMTPPRMTV b on b.ID_TIPO_PRIMITIVO = a.ID_TIPO_PRIMITIVO
        WHERE  a.ID_METAMODELO = :idMetamodelo AND  a.ID_TIPO_METAMODELO = :idTipoMetamodelo  ORDER BY  a.ORDEN
        """)
    
    def getByTipoMetamodelo (self, conexion, idMetamodelo , idTipoMetamodelo ):
        # Incluido en pruebas
        #return self.getNamedQuery(conexion,"getByTipoMetamodelo", {"idMetamodelo":idMetamodelo,"idTipoMetamodelo":idTipoMetamodelo} )
        return conexion.consultar( self.__getByTipoMetamodelo , {"idMetamodelo":idMetamodelo,"idTipoMetamodelo":idTipoMetamodelo} , ( "idMetamodelo", "idTipoMetamodelo", "idAtributoMetamodelo", "idTipoPrimitivo", "idTipoMetamodeloRef", "esObligatorio", "longitudAtributo", "precisionAtributo", "orden", "expRegularValidacion", "valorDefecto", "expRegularDefault", "idCatalogo" ) )

        
class JerarquiaTipoMetamodeloDao(xpdbdd.DaoBase):
    def __init__(self):
        metamodelo={"nombreTabla":"XMJRRQTP","propiedades":[],"namedQueries":[]}
        metamodelo["propiedades"].append({"nombre":"idMetamodelo","nombreCampo":"ID_METAMODELO","incremental":False,"pk":True,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":True,"update":False ,"opcional":False })
        metamodelo["propiedades"].append({"nombre":"idTipoMetamodeloPadre","nombreCampo":"ID_TIPO_METAMODELO_PADRE","incremental":False,"pk":True,"tipo":xpdbdd.XPDSTRING,"tamano":32,"insert": False ,"update":False,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"idJerarquia","nombreCampo":"ID_JERARQUIA","incremental":False,"pk":True,"tipo":xpdbdd.XPDSTRING,"tamano":32,"insert": False ,"update":False,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"idTipoMetamodeloHijo","nombreCampo":"ID_TIPO_METAMODELO_HIJO","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":32,"insert": False ,"update": False ,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"esMultiple","nombreCampo":"ES_MULTIPLE","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":1,"insert":False,"update": False ,"opcional":True})
        metamodelo["namedQueries"].append({"nombre":"getByTipoMetamodelo","whereClause":["idMetamodelo","idTipoMetamodeloPadre","esMultiple"],"orderBy":["idJerarquia"]})
        metamodelo["namedQueries"].append({"nombre":"getById","whereClause":["idMetamodelo","idTipoMetamodeloPadre","idJerarquia"],"orderBy":[]})

        self.setMetamodelo (metamodelo)
                
    def getByTipoMetamodelo (self, conexion, idMetamodelo , idTipoMetamodelo, esMultiple ):
        return self.getNamedQuery(conexion,"getByTipoMetamodelo", {"idMetamodelo":idMetamodelo,"idTipoMetamodeloPadre":idTipoMetamodelo, "esMultiple":esMultiple} )
    
    def getById (self, conexion, idMetamodelo , idTipoMetamodelo, idJerarquia ):
        return self.getNamedQuery(conexion,"getById", {"idMetamodelo":idMetamodelo,"idTipoMetamodeloPadre":idTipoMetamodelo,"idJerarquia":idJerarquia} )[0]
        
class ModeloDao(xpdbdd.DaoBase):
    def __init__(self):
        # incluido en pruebas
        metamodelo={"nombreTabla":"XMMDL","propiedades":[],"namedQueries":[]}
        metamodelo["propiedades"].append({"nombre":"idModelo","nombreCampo":"ID_MODELO" ,"incremental":True,"pk":True,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":False,"update":False,"opcional":True})
        metamodelo["propiedades"].append({"nombre":"idMetamodelo","nombreCampo":"ID_METAMODELO" ,"incremental":False,"pk":False,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":True,"update":False,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"nombre","nombreCampo":"NOMBRE_MODELO","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":16,"insert":True,"update":True,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"idObjetoRaiz","nombreCampo":"ID_OBJETO_RAIZ","incremental":False,"pk":False,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":False,"update":True,"opcional":True})
        metamodelo["namedQueries"].append({"nombre":"getAll","whereClause":[],"orderBy":["nombre"]})
        metamodelo["namedQueries"].append({ "nombre":"getByMetamodelo","whereClause":["idMetamodelo" ],"orderBy":["nombre"]})
        metamodelo["namedQueries"].append({ "nombre":"getById","whereClause":["idModelo" ],"orderBy":[]})

        self.setMetamodelo (metamodelo)
        
        self.__getAll = ("""SELECT a.ID_MODELO as idModelo,
        a.ID_METAMODELO as idMetamodelo,
        a.NOMBRE_MODELO as nombre,
        a.ID_OBJETO_RAIZ as idObjetoRaiz,
        b.NOMBRE_METAMODELO as nombreMetamodelo
        from XMMDL a
        left join XMMTMDL b on b.ID_METAMODELO = a.ID_METAMODELO
        """)
        self.__eliminarPorMetamodelo = ("delete from %s where ID_METAMODELO = :idMetamodelo " % metamodelo["nombreTabla"])
        
    def getById(self, conexion, idModelo ):
        # incluido en pruebas
        return self.getNamedQuery(conexion,"getById", {"idModelo": idModelo } )[0]
    
    def getByMetamodelo (self, conexion, idMetamodelo ):
        return self.getNamedQuery(conexion,"getByMetamodelo", {"idMetamodelo":idMetamodelo } )
    
    def getAll (self, conexion ):
        #return self.getNamedQuery(conexion,"getAll", {} )
        return conexion.consultar( self.__getAll , {} , ( "idModelo", "idMetamodelo", "nombre", "idObjetoRaiz", "nombreMetamodelo" ) )

    def eliminarPorMetamodelo(self, conexion, idMetamodelo ):
        cursor = conexion.cursor()
        cursor.execute ( self.__eliminarPorMetamodelo , {"idMetamodelo":idMetamodelo} )
        if config.DEBUG_MODE:
            print("jerarquias x metamodelo borrados")

class ObjetoModeloDao(xpdbdd.DaoBase):
    def __init__(self):
        # incluido en pruebas
        metamodelo={"nombreTabla": "XMOBJTMDL" ,"propiedades":[],"namedQueries":[]}
        metamodelo["propiedades"].append({"nombre":"idObjeto","nombreCampo":"ID_OBJETO" ,"incremental":True,"pk":True,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":False,"update":False,"opcional":True})
        metamodelo["propiedades"].append({"nombre":"idModelo","nombreCampo":"ID_MODELO" ,"incremental":False,"pk":False,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":True,"update":False,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"idTipoMetamodelo","nombreCampo":"ID_TIPO_METAMODELO","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":32,"insert":True,"update":False,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"idJerarquia","nombreCampo":"ID_JERARQUIA","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":32,"insert":True,"update":True,"opcional":True})

        metamodelo["propiedades"].append({"nombre":"nombre","nombreCampo":"NOMBRE","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":16,"insert":True,"update":True,"opcional":False})
        
        metamodelo["propiedades"].append({"nombre":"descripcion","nombreCampo":"DESCRIPCION","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":256,"insert":True,"update":True,"opcional":True})
        
        metamodelo["propiedades"].append({"nombre":"idObjetoPadre","nombreCampo":"ID_OBJETO_PADRE","incremental":False,"pk":False,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":True,"update":True,"opcional":True})
        metamodelo["propiedades"].append({"nombre":"orden","nombreCampo":"ORDEN","incremental":False,"pk":False,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":True,"update":True,"opcional":False})
        metamodelo["namedQueries"].append({"nombre":"getById","whereClause":["idObjeto" ],"orderBy":[ ]})
        metamodelo["namedQueries"].append({"nombre":"getByModelo","whereClause":["idModelo" ],"orderBy":["nombre"]})
        metamodelo[ "namedQueries"].append({"nombre":"getByObjetoPadre","whereClause":["idObjetoPadre" ,"idJerarquia"],"orderBy":["orden"]})
        
        
        self.setMetamodelo (metamodelo)
        
        self.__eliminarPorModelo = ("delete from %s where ID_MODELO = :idModelo " % metamodelo["nombreTabla"])
        self.__eliminarPorObjeto = ("delete from %s where ID_OBJETO = :idObjeto " % metamodelo["nombreTabla"])
        
        self.__getByModeloTipo = ("""SELECT a.ID_OBJETO AS idObjeto,
        a.ID_MODELO as idModelo,
        a.ID_TIPO_METAMODELO as idTipoMetamodelo,
        a.ID_JERARQUIA as idJerarquia,
        a.NOMBRE as nombre,
        a.DESCRIPCION as descripcion,
        a.ID_OBJETO_PADRE as idObjetoPadre,
        a.ORDEN as orden,
        b.NOMBRE as nombrePadre
        from XMOBJTMDL a 
        left join XMOBJTMDL b on b.ID_OBJETO = a.ID_OBJETO_PADRE
        where a.ID_MODELO = :idModelo
        and a.ID_TIPO_METAMODELO = :idTipoMetamodelo
        order by a.ID_OBJETO_PADRE, a.ORDEN
        """)
    
    def getById(self, conexion, idObjeto ):
        # incluido en pruebas
        return self.getNamedQuery(conexion,"getById", {"idObjeto":idObjeto } )[0]

    def getByModelo(self, conexion, idModelo ):
        return self.getNamedQuery(conexion,"getByModelo", {"idModelo":idModelo } )
        
    def getByObjetoPadre(self, conexion, idObjetoPadre, idJerarquia ):
        return self.getNamedQuery(conexion,"getByObjetoPadre", {"idObjetoPadre":idObjetoPadre ,"idJerarquia":idJerarquia} )
    
    def getByModeloTipo(self, conexion, idModelo, idTipoMetamodelo):
        return conexion.consultar( self.__getByModeloTipo , {"idModelo":idModelo,"idTipoMetamodelo":idTipoMetamodelo} , ( "idObjeto", "idModelo", "idTipoMetamodelo", "idJerarquia", "nombre", "descripcion", "idObjetoPadre", "orden", "nombrePadre" ) )
    
    def eliminarPorModelo(self, conexion, idModelo ):
        cursor = conexion.cursor()
        cursor.execute ( self.__eliminarPorModelo , {"idModelo":idModelo} )
        if config.DEBUG_MODE:
            print("jerarquias x metamodelo borrados")

    def eliminarPorObjeto(self, conexion, idObjeto ):
        cursor = conexion.cursor()
        cursor.execute ( self.__eliminarPorObjeto , {"idObjeto":idObjeto} )
        if config.DEBUG_MODE:
            print("jerarquias x metamodelo borrados")

class AtributoObjetoDao(xpdbdd.DaoBase):
    def __init__(self):
        # Incluido en pruebas
        metamodelo={"nombreTabla":"XMATRBTOBJT","propiedades":[],"namedQueries":[]}
        metamodelo["propiedades"].append({"nombre":"idObjeto","nombreCampo":"ID_OBJETO" ,"incremental":False,"pk":True,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":True,"update":False,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"idAtributoMetamodelo","nombreCampo":"ID_ATRIBUTO_METAMODELO","incremental":False,"pk":True,"tipo":xpdbdd.XPDSTRING,"tamano":32,"insert":True,"update":False,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"valor","nombreCampo":"VALOR","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":32,"insert":True,"update":True,"opcional":True})
        #TODO DEFINIR COnsulta manualmente
        metamodelo["namedQueries"].append({"nombre":"getByObjeto","whereClause":["idObjeto" ],"orderBy":[]})

        self.setMetamodelo (metamodelo)
        self.__getByObjeto = ("""SELECT 
            d.ID_OBJETO as idObjeto, b.ID_ATRIBUTO_METAMODELO as idAtributoMetamodelo, a.VALOR as valor 
          , b.ID_TIPO_PRIMITIVO as idTipoPrimitivo, b.ID_TIPO_METAMODELO_REF as idTipoMetamodeloRef, b.ES_OBLIGATORIO as esObligatorio, b.LONGITUD_ATRIBUTO as longitudAtributo, b.PRECISION_ATRIBUTO as precisionAtributo, b.ORDEN as orden, b.EXP_REGULAR_VALIDACION as expRegularValidacion , b.VALOR_DEFECTO as valorDefecto
          , c.EXP_REGULAR_DEFAULT as expRegularDefault
          , d.ID_OBJETO as idObjetoCreado
          , b.ID_CATALOGO as idCatalogo
          , f.NOMBRE as nombreRef
          , a.ID_OBJETO as idObjetoExistente
        FROM XMOBJTMDL d
        INNER JOIN XMMDL e on e.ID_MODELO = d.ID_MODELO
        INNER JOIN XMATRBTMTMDL b on b.ID_METAMODELO = e.ID_METAMODELO AND b.ID_TIPO_METAMODELO = d.ID_TIPO_METAMODELO
        LEFT JOIN XMATRBTOBJT a on a.ID_OBJETO = d.ID_OBJETO and a.ID_ATRIBUTO_METAMODELO = b.ID_ATRIBUTO_METAMODELO
        LEFT JOIN XMTPPRMTV c on c.ID_TIPO_PRIMITIVO = b.ID_TIPO_PRIMITIVO
        LEFT JOIN XMOBJTMDL f on f.ID_OBJETO = a.VALOR
        WHERE 
        d.ID_OBJETO = :idObjeto
        ORDER BY b.ORDEN""")
        
        self.__eliminarPorObjeto = ("delete from %s where ID_OBJETO = :idObjeto " % metamodelo["nombreTabla"])
        
    def getByObjeto (self, conexion, idObjeto ):
        # Incluido en pruebas
        #return self.getNamedQuery(conexion,"getByObjeto", {"idObjeto":idObjeto } )
        return conexion.consultar( self.__getByObjeto , {"idObjeto":idObjeto} , ( "idObjeto", "idAtributoMetamodelo", "valor", "idTipoPrimitivo", "idTipoMetamodeloRef", "esObligatorio", "longitudAtributo", "precisionAtributo", "orden", "expRegularValidacion", "valorDefecto", "expRegularDefault", "idObjetoCreado", "idCatalogo" , "nombreRef", "idObjetoExistente") )
    
    def eliminarPorObjeto(self, conexion, idObjeto ):
        cursor = conexion.cursor()
        cursor.execute ( self.__eliminarPorObjeto , {"idObjeto":idObjeto} )
        if config.DEBUG_MODE:
            print("jerarquias x metamodelo borrados")

class GeneradorDao(xpdbdd.DaoBase):
    def __init__(self):
        metamodelo={"nombreTabla":"XMGNRDR","propiedades":[],"namedQueries":[]}
        metamodelo["propiedades"].append({"nombre":"idMetamodelo","nombreCampo":"ID_METAMODELO" ,"incremental":False,"pk":True,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":True,"update":False,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"idGenerador","nombreCampo":"ID_GENERADOR" ,"incremental":False,"pk":True,"tipo":xpdbdd.XPDSTRING,"tamano":8,"insert":True,"update":False,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"nombreGenerador","nombreCampo":"NOMBRE_GENERADOR" ,"incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":16,"insert":True,"update":True,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"programaGenerador","nombreCampo":"PROGRAMA_GENERADOR" ,"incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":64,"insert":True,"update":True,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"mimeType","nombreCampo":"MIME_TYPE" ,"incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":8,"insert":True,"update":True,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"extension","nombreCampo":"EXTENSION" ,"incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":8,"insert":True,"update":True,"opcional":False})
        
        metamodelo["namedQueries"].append({"nombre":"getById","whereClause":["idMetamodelo","idGenerador" ],"orderBy":[]})
        metamodelo["namedQueries"].append({"nombre":"getByMetamodelo","whereClause":["idMetamodelo"],"orderBy":[]})

        self.setMetamodelo (metamodelo)
        
    def getById (self, conexion, idMetamodelo, idGenerador ):
        return self.getNamedQuery(conexion,"getById", {"idMetamodelo":idMetamodelo, "idGenerador":idGenerador } )[0]

    def getByMetamodelo (self, conexion, idMetamodelo ):
        return self.getNamedQuery(conexion,"getByMetamodelo", {"idMetamodelo":idMetamodelo } )

class ParcheDao(xpdbdd.DaoBase):
    def __init__(self):
        metamodelo={"nombreTabla":"XMPRCH","propiedades":[],"namedQueries":[]}
        metamodelo["propiedades"].append( {"nombre":"idParche","nombreCampo":"ID_PARCHE" ,"incremental":True,"pk":True,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":False,"update":False,"opcional":True})
        metamodelo["propiedades"].append({"nombre":"archivoParche","nombreCampo":"ARCHIVO_PARCHE" ,"incremental":False,"pk":False,"tipo": xpdbdd.XPDSTRING,"tamano":32,"insert":True,"update":False,"opcional":False})
        metamodelo["propiedades"].append({"nombre":"fechaParche","nombreCampo":"FECHA_PARCHE" ,"incremental":False,"pk":False,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":True,"update":False,"opcional":False})
                
        metamodelo["namedQueries"].append({"nombre":"getByArchivo","whereClause":["archivoParche" ],"orderBy":[]})
        metamodelo["namedQueries"].append({"nombre":"getAll","whereClause":[],"orderBy":["fechaParche"]})

        self.setMetamodelo (metamodelo)
        
    def getByArchivo (self, conexion, archivoParche ):
        return self.getNamedQuery(conexion,"getByArchivo", {"archivoParche":archivoParche } )

    def getAll (self, conexion ):
        return self.getNamedQuery(conexion,"getAll", { } )

class CatalogoDao(xpdbdd.DaoBase):
    def __init__(self):
        metamodelo={"nombreTabla":"XMCTLG","propiedades":[],"namedQueries":[]}
        
        metamodelo[ "propiedades" ].append({"nombre":"idMetamodelo","nombreCampo":"ID_METAMODELO","incremental":False,"pk":True,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":True,"update":False ,"opcional":False })
        metamodelo["propiedades"].append( {"nombre" : "idCatalogo",		"nombreCampo" : "ID_CATALOGO",		"incremental" : False,	"pk" : True,	"tipo" : xpdbdd.XPDSTRING,	"tamano" : 16,		"insert" : False,	"update" : False,	"opcional" : False } )
        metamodelo["propiedades"].append( {"nombre" : "nombreCatalogo",	"nombreCampo" : "NOMBRE_CATALOGO",	"incremental" : False,	"pk" : False,	"tipo" : xpdbdd.XPDSTRING,	"tamano" : 64,		"insert" : False,	"update" : False,	"opcional" : False } )
        
        metamodelo["namedQueries"].append( {"nombre" : "getByMetamodelo",	"whereClause" : ['idMetamodelo'],	"orderBy" : ["idCatalogo"] } )
        
        self.setMetamodelo (metamodelo)
        
    def getByMetamodelo (self, conexion , idMetamodelo ):
        return self.getNamedQuery(conexion,"getByMetamodelo", { 'idMetamodelo': idMetamodelo } )
        
class CatalogoValorDao(xpdbdd.DaoBase):
    def __init__(self):
        metamodelo={"nombreTabla": "XMCTLGVLR" ,"propiedades":[],"namedQueries":[]}
        
        metamodelo["propiedades"].append({"nombre":"idMetamodelo","nombreCampo":"ID_METAMODELO","incremental":False,"pk":True,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":True,"update":False ,"opcional":False })
        metamodelo["propiedades"].append( {"nombre" : "idCatalogo",	"nombreCampo" : "ID_CATALOGO",	"incremental" : False,	"pk" : True,	"tipo" : xpdbdd.XPDSTRING,	"tamano" : 16,		"insert" : False,	"update" : False,	"opcional" : False })
        metamodelo["propiedades"].append( {"nombre" : "clave",		"nombreCampo" : "CLAVE",		"incremental" : False,	"pk" : True,	"tipo" : xpdbdd.XPDSTRING,	"tamano" : 16,		"insert" : False,	"update" : False,	"opcional" : False })
        metamodelo["propiedades"].append( {"nombre" : "etiqueta",		"nombreCampo" : "ETIQUETA",	"incremental" : False,	"pk" : False,	"tipo" : xpdbdd.XPDSTRING,	"tamano" : 64,		"insert" : False,	"update" : False,	"opcional" : False })
        metamodelo["propiedades"].append( {"nombre" : "orden",		"nombreCampo" : "ORDEN",		"incremental" : False,	"pk" : False,	"tipo" : xpdbdd.XPDINTEGER,	"tamano" :  0,		"insert" : False,	"update" : False,	"opcional" : False })

        metamodelo["namedQueries"].append( {"nombre" : "getByMetamodelo",	"whereClause" : ['idMetamodelo'],	"orderBy" : ["idCatalogo", "orden"] } )
        
        self.setMetamodelo (metamodelo)
    
    def getByMetamodelo (self, conexion , idMetamodelo):
        return self.getNamedQuery(conexion,"getByMetamodelo", { 'idMetamodelo' : idMetamodelo } )

class ValidacionDao(xpdbdd.DaoBase):
    def __init__(self):
        metamodelo={"nombreTabla": "XMVLDCN" ,"propiedades":[],"namedQueries":[]}
        
        metamodelo["propiedades"].append( {"nombre" : "idMetamodelo","nombreCampo":"ID_METAMODELO","incremental":False,"pk":True,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":False,"update":False ,"opcional":False })
        metamodelo["propiedades"].append( {"nombre" : "idValidacion",	"nombreCampo" : "ID_VALIDACION",	"incremental" : False,	"pk" : True,	"tipo" : xpdbdd.XPDINTEGER,	"tamano" : 0,		"insert" : False,	"update" : False,	"opcional" : False })
        metamodelo["propiedades"].append( {"nombre" : "descripcion",		"nombreCampo" : "DESCRIPCION",		"incremental" : False,	"pk" : False,	"tipo" : xpdbdd.XPDSTRING,	"tamano" : 64,		"insert" : False,	"update" : False,	"opcional" : False })
        metamodelo["propiedades"].append( {"nombre" : "consulta",		"nombreCampo" : "CONSULTA",	"incremental" : False,	"pk" : False,	"tipo" : xpdbdd.XPDSTRING,	"tamano" : 1024,		"insert" : False,	"update" : False,	"opcional" : False })
        
        metamodelo["namedQueries"].append({"nombre":"getAll","whereClause":[],"orderBy":["descripcion"]})
        metamodelo["namedQueries"].append( {"nombre" : "getByMetamodelo",	"whereClause" : ['idMetamodelo'],	"orderBy" : ["idValidacion"] } )
        
        self.setMetamodelo (metamodelo)
    
    def getByMetamodelo (self, conexion , idMetamodelo):
        return self.getNamedQuery(conexion,"getByMetamodelo", { 'idMetamodelo' : idMetamodelo } )
        
    def getAll (self, conexion):
        # Incluido en pruebas
        return self.getNamedQuery(conexion,"getAll",{})
        
    def consultarValidacion (self, conexion, consulta, idModelo ):
        return conexion.consultar( consulta , {"idModelo":idModelo} , ( "idObjeto", "idModelo", "idTipoMetamodelo", "idJerarquia", "nombre", "descripcion", "idObjetoPadre", "orden", "nombrePadre", "descripcionValidacion", "nivel" ) )

def regenerarMetamodelo():
    # incluido en pruebas
    print("Inicia Reinicio de Repositorio")
    conexion = None
    respuestaDao = None
    paso = 0
    try:
        paso = 1
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        paso = 2
        
        # ejecuta script de datos iniciales
        conexion.ejecutarFileScript(config.INIT_SCRIPT)
        
        conexion.commit ()
        return True
    except (Exception) as ex:
        if not(conexion is None):
            conexion.rollback()
        print("Error Inicializacion "+str(paso)+": "+repr(ex))
        return False
        #pass
    finally:
        if not (conexion is None):
            conexion.close()
            conexion = None
    #print("Fin Reinicio de Repositorio")


def inicializarBase():
    # Incluido en pruebas
    print("Inicia Reinicio de Repositorio")
    conexion = None
    bancoDao = None
    tipoRespuestaDao = None
    preguntaDao = None
    respuestaDao = None
    
    paso = 0
    try:
        paso = 1
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        paso = 2
        
        # define los daos cuyo script de creacion va a ejecutar
        daos = ( MetamodeloDao() , TipoMetamodeloDao() , TipoPrimitivoDao() , AtributoTipoMetamodeloDao() , JerarquiaTipoMetamodeloDao() , GeneradorDao(), ModeloDao() , ObjetoModeloDao() , AtributoObjetoDao () , ParcheDao(), CatalogoDao() , CatalogoValorDao() , ValidacionDao() )
        for dao in daos:
            paso = paso + 1
            dao.crearTabla(conexion)
        paso = paso + 1
        
        # ejecuta script de datos iniciales
        conexion.ejecutarFileScript(config.INIT_SCRIPT)
        
        conexion.commit ()
        return True
    except (Exception) as ex:
        if not(conexion is None):
            conexion.rollback()
        print("Error Inicializacion "+str(paso)+": "+repr(ex))
        return False
        #pass
    finally:
        if not (conexion is None):
            conexion.close()
            conexion = None
    #print("Fin Reinicio de Repositorio")

def getMetamodelos():
    # Incluido en pruebas
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        dao=MetamodeloDao()
        lista = dao.getAll(conexion)
        return lista
    except (Exception) as ex:
        print("Error al listar metamodelos:" +repr(ex))
        raise xpdbdd.XpdException("error metamodelos %s"%(repr(ex)))
    finally:
        if not (conexion is None):
            conexion.close()
            conexion = None
    
def getModelos():
    # Incluido en pruebas
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        dao = ModeloDao()
        lista = dao.getAll(conexion)
        return lista
    except (Exception) as ex:
        print(repr(ex))
        raise xpdbdd.XpdException("error al consultar modelos ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None
            
def getJerarquiasByTipo( idMetamodelo , idTipoMetamodelo, esMultiple ):
    # Incluido en pruebas
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        dao = JerarquiaTipoMetamodeloDao()
        lista = dao.getByTipoMetamodelo( conexion, idMetamodelo , idTipoMetamodelo, esMultiple )
        return lista
    except (Exception) as ex:
        print(repr(ex))
        raise xpdbdd.XpdException("error al consultar jerarquias por tipo ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None
            
def getObjetosModeloByPadre( idObjeto , idJerarquia ):
    # Incluido en pruebas
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        dao = ObjetoModeloDao()
        modeloDao = ModeloDao()
        padre = dao.getById(conexion, idObjeto)
        modelo = modeloDao.getById(conexion, padre["idModelo"])
        lista = dao.getByObjetoPadre(conexion, idObjeto, idJerarquia )
        if config.DEBUG_MODE:
            print("modelo:" + str(modelo) )
        for objeto in lista:
            obtenerDataObjetoModelo(objeto,modelo["idMetamodelo"],conexion)
        return lista
    except (Exception) as ex:
        print(repr(ex))
        raise xpdbdd.XpdException("error al consultar jerarquias por tipo ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None

def getObjetosModeloByModeloTipo( idModelo, idTipoMetamodelo ):
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        dao = ObjetoModeloDao()
        lista = dao.getByModeloTipo(conexion, idModelo, idTipoMetamodelo )
        return lista
    except (Exception) as ex:
        print(repr(ex))
        raise xpdbdd.XpdException("error al consultar jerarquias por tipo ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None

def getAtributosByObjetoModelo( idObjeto ):
    # Incluido en pruebas
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        objetoModeloDao = ObjetoModeloDao()
        dao = AtributoObjetoDao()
        objetoModelo = objetoModeloDao.getById(conexion,idObjeto)
        lista = dao.getByObjeto( conexion, idObjeto )
        for atributo in lista:
            if atributo["valor"] is None:
                atributo["valor"] = atributo["valorDefecto"]
            if atributo["expRegularValidacion"] is None:
                atributo["expRegularValidacion"] = atributo["expRegularDefault"]
            if atributo["idObjetoCreado"] is None:
                dao.insertar(conexion,atributo)
        objetoModelo["_atributos"] = lista
        conexion.commit()
        return objetoModelo
    except (Exception) as ex:
        if not (conexion is None):
            conexion.rollback()
        print(repr(ex))
        raise xpdbdd.XpdException("error al consultar jerarquias por tipo ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None
            
def getDiccionarioAtributosByObjetoModelo( idObjeto ):
    #incluido en pruebas
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        return getDiccionarioAtributosByObjetoModeloConexion(idObjeto, conexion)
    except (Exception) as ex:
        print(repr(ex))
        raise xpdbdd.XpdException("error al consultar jerarquias por tipo ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None

def getDiccionarioAtributosByObjetoModeloConexion( idObjeto , conexion):
    #incluido en pruebas
    try:
        diccionario = {}
        dao = AtributoObjetoDao()
        lista = dao.getByObjeto( conexion, idObjeto )
        for atributo in lista:
            diccionario[atributo["idAtributoMetamodelo"]] = atributo["valor"]
        return diccionario
    except (Exception) as ex:
        print(repr(ex))
        raise xpdbdd.XpdException("error al consultar jerarquias por tipo ")

def crearObjetoModelo(objetoModelo,conexion):
    # incluido en pruebas
    conexionInterna = (conexion is None)
    try:
        # instancia conexion interna
        if conexionInterna:
            conexion=xpdbdd.Conexion(config.XPDBASEPATH)
            
        # instanciar todos los daos necesarios
        objetoModeloDao = ObjetoModeloDao()
        atributoObjetoDao = AtributoObjetoDao()
        modeloDao = ModeloDao()
        atributoTipoMetamodeloDao = AtributoTipoMetamodeloDao()
        jerarquiaTipoMetamodeloDao = JerarquiaTipoMetamodeloDao()
        
        # recupera informacion de tipo en el metamodelo
        modelo = modeloDao.getById(conexion, objetoModelo["idModelo"])
        atributosTipo = atributoTipoMetamodeloDao.getByTipoMetamodelo( conexion, modelo["idMetamodelo"] , objetoModelo["idTipoMetamodelo"] )
        # solo obtenemos las estructuras que no son multiples
        jerarquiasTipo = jerarquiaTipoMetamodeloDao.getByTipoMetamodelo( conexion, modelo["idMetamodelo"] , objetoModelo["idTipoMetamodelo"], '0' )
        
        #persiste objeto de modelo
        print("objeto modelo a crear "+str(objetoModelo))
        objetoModeloDao.insertar(conexion,objetoModelo)
        # perfila y persiste atributos con valores default
        for atributoTipo in atributosTipo:
            atributoObjeto = atributoObjetoDao.nuevoDiccionario()
            atributoObjeto ["idObjeto"] = objetoModelo ["idObjeto"]
            atributoObjeto ["idAtributoMetamodelo"] = atributoTipo ["idAtributoMetamodelo"]
            atributoObjeto ["valor"] = atributoTipo ["valorDefecto"]
            atributoObjetoDao.insertar(conexion, atributoObjeto )
        
        # perfila y persiste en la misma transaccion los jerarquicos unitarios
        for jerarquiaTipo in jerarquiasTipo:
            objetoHijo = objetoModeloDao.nuevoDiccionario()
            objetoHijo ["idModelo"] = objetoModelo ["idModelo"]
            objetoHijo ["idObjetoPadre"] = objetoModelo ["idObjeto"]
            objetoHijo ["idTipoMetamodelo"] = jerarquiaTipo ["idTipoMetamodeloHijo"]
            objetoHijo ["nombre"] = jerarquiaTipo ["idJerarquia"]
            crearObjetoModelo(objetoHijo,conexion)
        
        # acomete cambios solo si es conexion interna. la conexion externa la acomete el llamante
        if conexionInterna:
            conexion.commit()
            
        return objetoModelo
    except (Exception) as ex:
        if conexionInterna and not (conexion is None):
            conexion.rollback()
        print(repr(ex))
        raise xpdbdd.XpdException("error al crear objeto de modelo ")
    finally:
        if conexionInterna and not (conexion is None):
            conexion.close ()
            conexion = None

def crearModelo(modelo):
    # incluido en pruebas
    conexion = None
    try:
        # instancia conexion y daos
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        metamodeloDao = MetamodeloDao()
        modeloDao = ModeloDao()
        objetoModeloDao = ObjetoModeloDao()
        
        # recupera metamodelo para producir excepcion si no existe
        metamodelo = metamodeloDao.getById(conexion,modelo["idMetamodelo"])
        
        # persiste modelo
        modeloDao.insertar(conexion,modelo);
        
        # persiste objeto raiz
        objetoModelo = objetoModeloDao.nuevoDiccionario()
        objetoModelo ["idModelo"] = modelo ["idModelo"]
        objetoModelo ["idTipoMetamodelo"] = metamodelo ["idTipoRaiz"]
        objetoModelo ["nombre"] = modelo ["nombre"]
        objetoModelo = crearObjetoModelo(objetoModelo,conexion)
        
        #actualiza modelo con referencia de objeto raiz
        modelo["idObjetoRaiz"] = objetoModelo["idObjeto"]
        modeloDao.actualizar(conexion,modelo);
        
        # acomete transaccion
        conexion.commit()
        return modelo
    except (Exception) as ex:
        if not (conexion is None):
            conexion.rollback()
        print(repr(ex))
        raise xpdbdd.XpdException("error al crear modelo ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None
            
def crearObjetoHijo(objetoModelo):
    # Incluido en pruebas
    conexion = None
    try:
        # instancia conexion y daos
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        metamodeloDao = MetamodeloDao()
        modeloDao = ModeloDao()
        objetoModeloDao = ObjetoModeloDao()
        jerarquiaTipoMetamodeloDao = JerarquiaTipoMetamodeloDao()
        
        # recuprra objeto padre hermanos y modelo
        objetoModeloPadre = objetoModeloDao.getById(conexion, objetoModelo["idObjetoPadre"] )
        hermanos = objetoModeloDao.getByObjetoPadre(conexion, objetoModelo["idObjetoPadre"], objetoModelo["idJerarquia"] )

        modelo = modeloDao.getById(conexion, objetoModeloPadre["idModelo"])
        # recupera metamodelo para producir excepcion si no existe
        metamodelo = metamodeloDao.getById(conexion,modelo["idMetamodelo"])
        # recupera jerarquia para determinar tipo
        jerarquia = jerarquiaTipoMetamodeloDao.getById(conexion,metamodelo["idMetamodelo"],objetoModeloPadre["idTipoMetamodelo"],objetoModelo["idJerarquia"])
        if jerarquia["esMultiple"] != "1":
            raise xpdbdd.XpdException("Jerarquia no es valida")
        # persiste objeto raiz
        objetoModelo ["idModelo"] = modelo["idModelo"]
        objetoModelo ["idTipoMetamodelo"] = jerarquia["idTipoMetamodeloHijo"]
        if len(hermanos) > 0:
            objetoModelo ["orden"] = hermanos[ len(hermanos) -1 ]["orden"] + 1
        else:
            objetoModelo ["orden"] = 1
        print(str(objetoModelo))
        objetoModelo = crearObjetoModelo(objetoModelo,conexion)
        
        # acomete transaccion
        conexion.commit()
        return objetoModelo
    except (Exception) as ex:
        if not (conexion is None):
            conexion.rollback()
        print(repr(ex))
        raise xpdbdd.XpdException("error al crear modelo ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None

def actualizarObjetoModelo_deprecado(objetoModelo, conexion):    
    conexionInterna = (conexion is None)
    try:
        # instancia conexion interna
        if conexionInterna:
            conexion=xpdbdd.Conexion(config.XPDBASEPATH)
            
        # instanciar todos los daos necesarios
        objetoModeloDao = ObjetoModeloDao()
                
        #persiste objeto de modelo
        objetoModeloDao.actualizar(conexion,objetoModelo)
                
        # acomete cambios solo si es conexion interna. la conexion externa la acomete el llamante
        if conexionInterna:
            conexion.commit()
            
        return objetoModelo
    except (Exception) as ex:
        if conexionInterna and not (conexion is None):
            conexion.rollback()
        print(repr(ex))
        raise xpdbdd.XpdException("error al actualizar objeto de modelo ")
    finally:
        if conexionInterna and not (conexion is None):
            conexion.close ()
            conexion = None

def actualizarAtributosObjeto( objetoModelo1 ,conexion ):
    #incluido en pruebas
    conexionInterna = (conexion is None)
    try:
        # instancia conexion interna
        if conexionInterna:
            conexion=xpdbdd.Conexion(config.XPDBASEPATH)
            
        # instanciar todos los daos necesarios
        objetoModeloDao = ObjetoModeloDao()
        atributoObjetoDao = AtributoObjetoDao()
        modeloDao = ModeloDao()
        atributoTipoMetamodeloDao = AtributoTipoMetamodeloDao()
                
        # recupera informacion de tipo en el metamodelo
        objetoModelo = objetoModeloDao.getById(conexion, objetoModelo1["idObjeto"])
        modelo = modeloDao.getById(conexion, objetoModelo["idModelo"])
        # atributosTipo = atributoTipoMetamodeloDao.getByTipoMetamodelo( conexion, modelo["idMetamodelo"] , objetoModelo["idTipoMetamodelo"] )
        atributosTipo = atributoObjetoDao.getByObjeto( conexion, objetoModelo1["idObjeto"] )
        
        # actualiza objrto modelo
        objetoModelo["nombre"] = objetoModelo1["nombre"]
        objetoModelo["descripcion"] = objetoModelo1["descripcion"]
        objetoModeloDao.actualizar(conexion,objetoModelo)
        objetoModelo["__errorCode"] = 0
        objetoModelo["__mensajes"] = []
        
        # perfila y persiste atributos con valores default
        for atributoTipo in atributosTipo:
            atributoObjeto = atributoObjetoDao.nuevoDiccionario()
            atributoObjeto ["idObjeto"] = objetoModelo ["idObjeto"]
            atributoObjeto ["idAtributoMetamodelo"] = atributoTipo ["idAtributoMetamodelo"]
            atributoObjeto ["idObjetoExistente"] = atributoTipo ["idObjetoExistente"]
            
            # empieza asignando valor por defecto y luego busca en el listado
            valor = atributoTipo ["valorDefecto"]
            for atributoEntrada in objetoModelo1["__atributos"]:
              if atributoEntrada ["idAtributoMetamodelo"] == atributoTipo ["idAtributoMetamodelo"]:
                  if not (atributoEntrada ["valor"] is None):
                      valor = atributoEntrada["valor"]
                      #valida la expresion regular que aplica
                      if atributoTipo["esObligatorio"] == '0' and atributoEntrada["valor"] == "":
                          pass
                      elif atributoTipo["esObligatorio"] == '1' and atributoEntrada["valor"] == "":
                          objetoModelo["__errorCode"] = 1
                          objetoModelo["__mensajes"].append({"idAtributoMetamodelo": atributoEntrada["idAtributoMetamodelo"] ,"mensaje": "valor requerido" })
                      else:
                          expRegular = None
                          if atributoTipo["expRegularValidacion"] is None or atributoTipo["expRegularValidacion"] == "":
                              expRegular = atributoTipo["expRegularDefault"]
                          else:
                              expRegular = atributoTipo["expRegularValidacion"]
                          if not(expRegular is None or expRegular == ""):
                              #print("evalua \"%s\" con patron \"%s\""%( valor, expRegular))
                              if not(re.match(expRegular,valor)):
                                  objetoModelo["__errorCode"] = 2
                                  objetoModelo["__mensajes"].append({"idAtributoMetamodelo": atributoEntrada["idAtributoMetamodelo"] ,"mensaje": "%s no valido"%atributoEntrada["idAtributoMetamodelo"] })
                  break
            if objetoModelo["__errorCode"] == 0:
                atributoObjeto ["valor"] = valor
                if atributoObjeto ["idObjetoExistente"] is None:
                    atributoObjetoDao.insertar(conexion, atributoObjeto )
                else:
                    atributoObjetoDao.actualizar(conexion, atributoObjeto )
                
        # acomete cambios solo si es conexion interna. la conexion externa la acomete el llamante
        if conexionInterna:
            if objetoModelo["__errorCode"] == 0:
                conexion.commit()
            else:
                conexion.rollback()
        return objetoModelo
    except (Exception) as ex:
        if conexionInterna and not (conexion is None):
            conexion.rollback()
        print(repr(ex))
        raise xpdbdd.XpdException("error al actualizar objeto de modelo ")
    finally:
        if conexionInterna and not (conexion is None):
            conexion.close ()
            conexion = None

def obtenerDataObjetoModelo(objetoModelo,idMetamodelo,conexion):
    # incluido en pruebas
    objetoModeloDao = ObjetoModeloDao()
    jerarquiaDao = JerarquiaTipoMetamodeloDao()
    jerarquias = jerarquiaDao.getByTipoMetamodelo( conexion, idMetamodelo , objetoModelo["idTipoMetamodelo"], '0' )
    listas = jerarquiaDao.getByTipoMetamodelo( conexion, idMetamodelo , objetoModelo["idTipoMetamodelo"], '1' )
    objetoModelo["_listas"] = listas
    objetoModelo["_jerarquias"] = []
    for jerarquia in jerarquias:
        objeto1 = objetoModeloDao.getByObjetoPadre(conexion, objetoModelo["idObjeto"], jerarquia["idJerarquia"] )
        if len(objeto1)>0:
            obtenerDataObjetoModelo(objeto1[0],idMetamodelo,conexion)
            objetoModelo["_jerarquias"].append( objeto1[0])
    return objetoModelo

def getRaizModelo(idModelo):
    # incluido en pruebas
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        modeloDao = ModeloDao()
        objetoModeloDao = ObjetoModeloDao()
        modelo = modeloDao.getById(conexion,idModelo)
        objetoModelo = objetoModeloDao.getById(conexion, modelo["idObjetoRaiz"] )
        objetoModelo = obtenerDataObjetoModelo(objetoModelo, modelo["idMetamodelo"] ,conexion)
        return objetoModelo
    except (Exception) as ex:
        print(repr(ex))
        raise xpdbdd.XpdException("error al consultar jerarquias por tipo ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None
            
def getGeneradoresByModelo(idModelo):
    # incluido en pruebas
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        modeloDao = ModeloDao()
        generadorDao = GeneradorDao()
        modelo = modeloDao.getById(conexion,idModelo)
        generadores = generadorDao.getByMetamodelo(conexion,modelo["idMetamodelo"])
        return generadores
    except (Exception) as ex:
        print(repr(ex))
        raise xpdbdd.XpdException("error al consultar jerarquias por tipo ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None
            
def getModeloGenerador(idModelo,idGenerador):
    # incluido en pruebas
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        modeloDao = ModeloDao()
        generadorDao = GeneradorDao()
        modelo = modeloDao.getById(conexion,idModelo)
        generador = generadorDao.getById(conexion,modelo["idMetamodelo"],idGenerador)
        modelo["__generador"] = generador
        return modelo
    except (Exception) as ex:
        print(repr(ex))
        raise xpdbdd.XpdException("error al obtenerModelo con generador")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None
            
def getParches(incluirAplicados):
    # Incluido en pruebas
    archivos = os.listdir(config.PARCHE_ROOT)
    lista = []
    filtro =[]
    if incluirAplicados == 0:
        conexion = None
        try:
            conexion=xpdbdd.Conexion(config.XPDBASEPATH)
            parcheDao = ParcheDao()
            listaFiltro = parcheDao.getAll(conexion)
            for filtrable in listaFiltro:
                filtro.append(filtrable["archivoParche"])
        except (Exception) as ex:
            print(repr(ex))
        finally:
            if not (conexion is None):
                conexion.close ()
                conexion = None
    for archivo in archivos:
        if not(archivo in filtro):
            lista.append({"archivoParche":archivo})
    return lista
    
def verificarParche(archivoParche):
    # Incluido en pruebas
    resultado = None
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        parcheDao = ParcheDao()
        listaFiltro = parcheDao.getByArchivo(conexion,archivoParche)
        if len(listaFiltro) > 0:
            resultado = listaFiltro[0]
            resultado["aplicado"] = True
    except (Exception) as ex:
        print(repr(ex))
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None
    if resultado is None:
        resultado = {"archivoParche":archivoParche,"aplicado":False}
    return resultado

def aplicarParche(archivoParche):
    # Incluido en pruebas
    resultado = "1"
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        
        # ejecuta el parche como python o como sql
        if archivoParche.endswith(".py"):
            parche = imp.load_source("parche", config.PARCHE_ROOT+"/"+archivoParche )
            getattr(moduloGenerador,"__main__")()
        else:
            conexion.ejecutarFileScript( config.PARCHE_ROOT+"/"+archivoParche )
        
        #determina si debe registrar ejecucion de parche
        parcheDao = ParcheDao()
        listaFiltro = parcheDao.getByArchivo(conexion,archivoParche)
        if len(listaFiltro) == 0:
            parche = parcheDao.nuevoDiccionario()
            parche["archivoParche"] = archivoParche
            parche["fechaParche"] = 0
            parcheDao.insertar(conexion,parche)
            
        conexion.commit()
    except (Exception) as ex:
        if not (conexion is None):
            conexion.rollback()
        resultado = repr(ex)
        print("Error al ejecutar parche %s"%repr(ex))
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None
    return resultado
    
def exportarModelo(idModelo, nombreArchivo = None):
    "Exporta todo el modelo en formato json"
    # incluido en pruebas
    conexion = None
    archivo = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        modeloDao = ModeloDao()
        jerarquiaDao = JerarquiaTipoMetamodeloDao()
        objetoModeloDao = ObjetoModeloDao()
        
        modelo = modeloDao.getById(conexion,idModelo)
        objetoModelo = objetoModeloDao.getById(conexion, modelo["idObjetoRaiz"] )
        colaObjetos = [objetoModelo]
        idMetamodelo = modelo["idMetamodelo"]
        while len(colaObjetos) > 0:
            ob = colaObjetos.pop(0)
            
            # recupera Atributos
            ob["__atributos"] = getDiccionarioAtributosByObjetoModeloConexion( ob["idObjeto"],conexion )
            
            #recupera jerarquias y listas
            jerarquias = jerarquiaDao.getByTipoMetamodelo( conexion, idMetamodelo , ob["idTipoMetamodelo"], '0' )
            listas = jerarquiaDao.getByTipoMetamodelo( conexion, idMetamodelo , ob["idTipoMetamodelo"], '1' )
            
            # procesa Jerarquias
            ob["__jerarquias"] = {}
            for jerarquia in jerarquias:
                ob["__jerarquias"][jerarquia["idJerarquia"]] = objetoModeloDao.getByObjetoPadre(conexion, ob["idObjeto"], jerarquia["idJerarquia"] )[0]
                colaObjetos.append( ob["__jerarquias"][jerarquia["idJerarquia"]] )
            
            # procesa Listas
            ob["__listas"] = {}
            for lista in listas:
                ob["__listas"][ lista["idJerarquia"] ] = objetoModeloDao.getByObjetoPadre(conexion, ob["idObjeto"], lista["idJerarquia"] )
                for hijo in ob["__listas"][ lista["idJerarquia"] ]:
                    colaObjetos.append(hijo)
            
        modelo["__objetoRaiz"] = objetoModelo
        if not(nombreArchivo is None):
            salida = json.dumps( modelo, sort_keys = True, indent = 2, separators = (',',': ') )
            archivo = open("%s/%s"%(config.FS_ROOT,nombreArchivo),'w')
            archivo.write(salida)
            archivo.flush()
            
        return modelo
    except (Exception) as ex:
        print(repr(ex))
        raise xpdbdd.XpdException("error al consultar jerarquias por tipo ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None
        if not(archivo is None):
            archivo.close()
            archivo = None

def importarObjetoModelo( conexion , objetoModelo , idModelo , idObjetoPadre ):
    "Importa un objeto y su jerarquia desee un objeto JSON"
    # incluido en pruebas
    objetoModelo["idObjetoAnt"] = objetoModelo["idObjeto"]
    objetoModelo["idObjetoPadre"] = idObjetoPadre
    objetoModelo["idModelo"] = idModelo
    objetoModeloDao = ObjetoModeloDao()
    objetoModeloDao.insertar(conexion,objetoModelo)
    
    # inserta atributos
    atributoDao = AtributoObjetoDao()
    for idAtributo in objetoModelo["__atributos"].keys():
        atributo = atributoDao.nuevoDiccionario()
        atributo["idObjeto"] = objetoModelo["idObjeto"]
        atributo["idAtributoMetamodelo"] = idAtributo
        atributo["valor"] = objetoModelo["__atributos"][idAtributo]
        atributoDao.insertar(conexion,atributo)
    
    # inserta hijos de jerarquias
    for idJerarquia in objetoModelo["__jerarquias"].keys():
        importarObjetoModelo( conexion, objetoModelo["__jerarquias"][idJerarquia] , idModelo , objetoModelo["idObjeto"])
    
    # inserta hijos de listas
    for idJerarquia in objetoModelo["__listas"].keys():
        for objetoModeloHijo in objetoModelo["__listas"][idJerarquia]:
            importarObjetoModelo( conexion, objetoModeloHijo , idModelo , objetoModelo["idObjeto"])

def importarModelo(jsonModelo):
    "Importa un modelo desde un objeto json"
    # incluido en pruebas
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        modeloDao = ModeloDao()
        modeloDao.insertar(conexion,jsonModelo)
        importarObjetoModelo( conexion , jsonModelo["__objetoRaiz"] , jsonModelo["idModelo"] , None )
        jsonModelo["idObjetoRaiz"] = jsonModelo["__objetoRaiz"]["idObjeto"]
        modeloDao.actualizar(conexion,jsonModelo)
        conexion.commit()
        return jsonModelo["idModelo"]
    except (Exception) as ex:
        conexion.rollback()
        print(repr(ex))
        raise xpdbdd.XpdException("error al consultar jerarquias por tipo ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None

def getObjetosByModelo(idModelo):
    "listado lineal de objetos por modelo. Usado para verificar importacion y exportacion"
    # incluido en pruebas
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        dao = ObjetoModeloDao()
        return dao.getByModelo(conexion,idModelo)
    except (Exception) as ex:
        print(repr(ex))
        raise xpdbdd.XpdException("error al consultar jerarquias por tipo ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None
            
def moverObjeto(idObjeto , moverArriba):
    "ajusta el orden de todos los objetos"
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        dao = ObjetoModeloDao()
        objetoModelo = dao.getById(conexion,idObjeto)
        idObjetoPadre = objetoModelo["idObjetoPadre"]
        hermanos = dao.getByObjetoPadre(conexion,idObjetoPadre,objetoModelo["idJerarquia"])
        orden = 1
        indice = -1
        for hermano in hermanos:
            hermano["orden"] = orden
            if hermano ["idObjeto"] == objetoModelo ["idObjeto"]:
                indice = orden - 1
            orden = orden + 1
        if moverArriba == 1:
            hermanos[indice]["orden"] = hermanos[indice]["orden"] - 1
            hermanos[indice - 1]["orden"] = hermanos[indice]["orden"] + 1
        else:
            hermanos[indice]["orden"] = hermanos[indice]["orden"] + 1
            hermanos[indice + 1]["orden"] = hermanos[indice]["orden"] - 1
        for hermano in hermanos:
            dao.actualizar(conexion, hermano)
        conexion.commit()
        return ("1")
    except (Exception) as ex:
        conexion.rollback()
        print(repr(ex))
        raise xpdbdd.XpdException("error al consultar jerarquias por tipo ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None

def eliminarObjeto(idObjeto, conexion):
    "Elimina ObjetoModelo con sus atributos e hijos"
    conexionInterna = (conexion is None)
    try:
        if conexionInterna:
            conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        modeloDao = ModeloDao()
        jerarquiaDao = JerarquiaTipoMetamodeloDao()
        objetoModeloDao = ObjetoModeloDao()
        atributoObjetoDao = AtributoObjetoDao()

        objetoModelo = objetoModeloDao.getById(conexion, idObjeto )
        modelo = modeloDao.getById(conexion,objetoModelo["idModelo"])
        idMetamodelo = modelo["idMetamodelo"]
        idTipoMetamodelo = objetoModelo["idTipoMetamodelo"]
        
        #recupera jerarquias y listas
        jerarquias = jerarquiaDao.getByTipoMetamodelo( conexion, idMetamodelo , idTipoMetamodelo , '0' )
        listas = jerarquiaDao.getByTipoMetamodelo( conexion, idMetamodelo , idTipoMetamodelo , '1' )
            
        # procesa Jerarquias
        for jerarquia in jerarquias:
            hijos = objetoModeloDao.getByObjetoPadre(conexion, idObjeto , jerarquia["idJerarquia"] )
            for hijo in hijos:
                eliminarObjeto(hijo["idObjeto"],conexion)
                        
        # procesa Listas
        for lista in listas:
            hijos = objetoModeloDao.getByObjetoPadre(conexion, objetoModelo["idObjeto"], lista["idJerarquia"] )
            for hijo in hijos:
                eliminarObjeto(hijo["idObjeto"],conexion)
        
        # elimina Atributos y el objeto mismo
        atributoObjetoDao.eliminarPorObjeto(conexion, idObjeto )
        objetoModeloDao.eliminar(conexion, objetoModelo)

        if conexionInterna:
            conexion.commit()
        return ("1")
    except (Exception) as ex:
        if conexionInterna and not (conexion is None):
            conexion.rollback()
        print(repr(ex))
        raise xpdbdd.XpdException("error al consultar jerarquias por tipo ")
    finally:
        if conexionInterna and  not (conexion is None):
            conexion.close ()
            conexion = None
            
def getCatalogoByModelo(idModelo):
    "listado de valores de catalogo por metamodelo"
    # incluido en pruebas
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        catalogoValorDao = CatalogoValorDao()
        
        modeloDao = ModeloDao()
        catalogoDao = CatalogoDao()
        modelo = modeloDao.getById(conexion,idModelo)
        catalogos = catalogoDao.getByMetamodelo(conexion,modelo['idMetamodelo'])
        catalogosValor = catalogoValorDao.getByMetamodelo(conexion,modelo['idMetamodelo'])
        resultado = {}
        #print('CATALOGOS:' + str(catalogos) )
        for catalogo in catalogos:
            # resultado[ catalogo['idCatalogo'] ] = catalogosValor[ [catalogoValor['idCatalogo'] == catalogo['idCatalogo'] for catalogoValor in catalogosValor] ]  
            resultado[ catalogo['idCatalogo'] ] = []
        for catalogoValor in catalogosValor:
            resultado[ catalogoValor['idCatalogo'] ] .append( catalogoValor )
        return resultado
    except (Exception) as ex:
        print(repr(ex))
        raise xpdbdd.XpdException("error al consultar valores de catalogo ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None

def validarModelo( idModelo ):
    conexion = None
    try:
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        
        modeloDao = ModeloDao()
        validadorDao = ValidacionDao()
        
        modelo = modeloDao.getById(conexion,idModelo)
        
        validaciones = validadorDao.getByMetamodelo( conexion , 0 )
        validaciones += validadorDao.getByMetamodelo( conexion , modelo['idMetamodelo'] )
        
        lista = []
        
        for validacion in validaciones:
            lista += validadorDao.consultarValidacion(conexion, validacion['consulta'], idModelo)
        
        for objeto in lista:
            obtenerDataObjetoModelo(objeto,modelo["idMetamodelo"],conexion)
            if objeto['idObjetoPadre'] is None:
                objeto['idObjetoPadre'] = 0
        return lista
        #return sorted(lista, key = lambda x : '{0: >8}:{1:0>6}:{2:0>6}'.format( x['nivel'], x['idObjetoPadre'], x['orden'] ) )
    except (Exception) as ex:
        print('ERROR VALIDACION ' + repr(ex))
        raise xpdbdd.XpdException("error al validar modelo ")
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None
            
def generarModelo( idModelo, idGenerador ):
    conexion = None
    try:
        modelo = exportarModelo( idModelo )
        
        conexion=xpdbdd.Conexion(config.XPDBASEPATH)
        generadorDao = GeneradorDao()
        generador = generadorDao.getById( conexion , modelo['idMetamodelo'] , idGenerador )
        
        return GeneradorModelo.generarModelo(modelo, generador)
        
    except (Exception) as ex:
        print('ERROR VALIDACION ' + repr(ex))
        return {"error":repr(ex)}
    finally:
        if not (conexion is None):
            conexion.close ()
            conexion = None

            
