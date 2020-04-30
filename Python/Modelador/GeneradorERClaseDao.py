import ModeladorDao
import config

def getTipo(campo):
    return ("xpdbdd.XPD%s"%campo["tipo"])
        
def getObligatorio(campo):
    if campo["obligatorio"] == "1":
        return ("NOT NULL")
    else:
        return ("")
        
def parseBoolean(valor):
    if valor =="1":
        return ("True")
    else:
        return ("False")
        
def getCantidad(campo,atributo):
    if campo[atributo] is None or campo[atributo] == "":
        return ("")
    else:
        return campo[atributo]
        
def getListaCampos(listaCampos):
    resultado = ("")
    primercampo = True
    for campo in listaCampos:
        if not(primercampo):
            resultado = resultado + ","
        resultado = ("%s\"%s\"" % (resultado,campo["nombre"]))
        primercampo = False
    return resultado

def generarModelo(modelo , archivo):
    print("inicia GeneradorERScriptSql")
    try:
        fileName = ( "%s%s" % (modelo["nombre"],modelo["__generador"]["extension"]) )
        raiz = ModeladorDao.getRaizModelo(modelo["idModelo"])
        entidades = ModeladorDao.getObjetosModeloByPadre( raiz["idObjeto"] , "Entidades" )
        
        archivo.write("import xpdbdd\n")
        
        for entidad in entidades:
            atributosEntidad = ModeladorDao.getDiccionarioAtributosByObjetoModelo( entidad["idObjeto"] )
            namedQueries = ModeladorDao.getObjetosModeloByPadre(entidad["idObjeto"],"NamedQueries")
            campos =       ModeladorDao.getObjetosModeloByPadre(entidad["idObjeto"],"Campos")
            
            archivo.write("\nclass %sDao(xpdbdd.DaoBase):\n    def __init__(self):" % entidad["nombre"] )
            archivo.write("\n       metamodelo={\"nombreTabla\":\"%s\",\"propiedades\":[],\"namedQueries\":[]}" % atributosEntidad["nombreTabla"] )

            for campo in campos:
                atributosCampo = ModeladorDao. getDiccionarioAtributosByObjetoModelo( campo["idObjeto"] )
                tipo = getTipo(atributosCampo)
                tamano = getCantidad(atributosCampo,"tamano")
                opcional = "0"
                if parseBoolean(atributosCampo["obligatorio"]) == "0":
                    opcional = "1"
                archivo.write("\n       metamodelo[\"propiedades\"].append({\"nombre\":\"%s\",\"nombreCampo\":\"%s\",\"incremental\":%s,\"pk\":%s,\"tipo\":%s,\"tamano\":%s,\"insert\":%s,\"update\":%s,\"opcional\":%s})" % ( campo["nombre"], atributosCampo["nombreCampo"] , parseBoolean(atributosCampo["incremental"]) , parseBoolean(atributosCampo["pk"]) , tipo , tamano , parseBoolean(atributosCampo["insert"]) , parseBoolean(atributosCampo["update"]) , opcional ) )
            
            for namedQuery in namedQueries:
                camposWhere = ModeladorDao.getObjetosModeloByPadre(namedQuery["idObjeto"],"camposWhere")
                namedQuery["camposWhere"] = camposWhere
                camposOrderBy = ModeladorDao.getObjetosModeloByPadre(namedQuery["idObjeto"],"camposOrderBy")
                archivo.write("\n        metamodelo[\"namedQueries\"].append({\"nombre\":\"%s\",\"whereClause\":[%s],\"orderBy\":[%s]})" % ( namedQuery["nombre"] , getListaCampos(camposWhere) , getListaCampos(camposOrderBy) ))
            
            archivo.write( "\n        self.setMetamodelo (metamodelo)" )
            
            for namedQuery in namedQueries:
                camposWhere = namedQuery["camposWhere"]
                archivo.write("\n    \n    def %s (self, conexion" % namedQuery["nombre"] )
                for campoWhere in camposWhere:
                    archivo.write(", %s" % campoWhere["nombre"])
                archivo.write("):")
                archivo.write("\n        return self.getNamedQuery(conexion,\"%s\", {" % namedQuery["nombre"] )
                primercampo = True
                for campoWhere in camposWhere:
                    if not (primercampo):
                        archivo.write(",")
                    archivo.write("\"%s\":%s" % ( campoWhere["nombre"] , campoWhere["nombre"] ))
                    primercampo = False

                archivo.write("} ) ")
            
            archivo.write("\n")
            archivo.flush()
            
        resultado = {"fileName":fileName,"mimeType":modelo["__generador"]["mimeType"]}
        return resultado
    except (Exception) as ex:
        print(repr(ex))
        return {"error":repr(ex)}

            