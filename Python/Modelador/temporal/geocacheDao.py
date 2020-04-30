import xpdbdd

class PosicionDao(xpdbdd.DaoBase):
    def __init__(self):
       metamodelo={"nombreTabla":"AGO_POSICION","propiedades":[],"namedQueries":[]}
       metamodelo["propiedades"].append({"nombre":"idPosicion","nombreCampo":"ID_POSICION","incremental":True,"pk":True,"tipo":xpdbdd.XPDINTEGER,"tamano":0,"insert":False,"update":False,"opcional":0})
       metamodelo["propiedades"].append({"nombre":"fecha","nombreCampo":"FECHA","incremental":False,"pk":False,"tipo":xpdbdd.XPDDATE,"tamano":0,"insert":True,"update":False,"opcional":0})
       metamodelo["propiedades"].append({"nombre":"latitud","nombreCampo":"LATITUD","incremental":False,"pk":False,"tipo":xpdbdd.XPDDOUBLE,"tamano":0,"insert":True,"update":False,"opcional":0})
       metamodelo["propiedades"].append({"nombre":"longitud","nombreCampo":"LONGITUD","incremental":False,"pk":False,"tipo":xpdbdd.XPDDOUBLE,"tamano":0,"insert":True,"update":False,"opcional":0})
       metamodelo["propiedades"].append({"nombre":"sincronizado","nombreCampo":"SINCRONIZADO","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":1,"insert":True,"update":True,"opcional":0})
       metamodelo["propiedades"].append({"nombre":"idReferencia","nombreCampo":"ID_REFERENCIA","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":16,"insert":True,"update":False,"opcional":0})
       metamodelo["propiedades"].append({"nombre":"descripcion","nombreCampo":"DESCRIPCION","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":128,"insert":True,"update":False,"opcional":0})
        metamodelo["namedQueries"].append({"nombre":"getByEstado","whereClause":["sincronizado"],"orderBy":["fecha"]})
        self.setMetamodelo (metamodelo)
    
    def getByEstado (self, conexion, sincronizado):
        return self.getNamedQuery(conexion,"getByEstado", {"sincronizado":sincronizado} ) 

class ConfiguracionDao(xpdbdd.DaoBase):
    def __init__(self):
       metamodelo={"nombreTabla":"AGO_CONFIGURACION","propiedades":[],"namedQueries":[]}
       metamodelo["propiedades"].append({"nombre":"clave","nombreCampo":"CLAVE","incremental":False,"pk":True,"tipo":xpdbdd.XPDSTRING,"tamano":8,"insert":False,"update":False,"opcional":0})
       metamodelo["propiedades"].append({"nombre":"valor","nombreCampo":"VALOR","incremental":False,"pk":False,"tipo":xpdbdd.XPDSTRING,"tamano":128,"insert":True,"update":True,"opcional":0})
        metamodelo["namedQueries"].append({"nombre":"getAll","whereClause":[],"orderBy":["clave"]})
        metamodelo["namedQueries"].append({"nombre":"getByClave","whereClause":["clave"],"orderBy":[]})
        self.setMetamodelo (metamodelo)
    
    def getAll (self, conexion):
        return self.getNamedQuery(conexion,"getAll", {} ) 
    
    def getByClave (self, conexion, clave):
        return self.getNamedQuery(conexion,"getByClave", {"clave":clave} ) 
