import config

def getValorVarchar(valor):
    if valor is None :
        return ("NULL")
    else:
        return ("'%s'" % valor)
            
def getValorNumber(valor):
    if valor is None :
        return ("NULL")
    else:
        return str(valor)
        
def generarModelo(modelo):
    
    print("inicia GeneradorMetamodeloSql")
    try:
        fileName = ( "%s%s" % (modelo["nombre"],modelo["__generador"]["extension"]) )
        metamodelo = ModeladorDao.getRaizModelo(modelo["idModelo"])
        atributosMetamodelo = ModeladorDao. getDiccionarioAtributosByObjetoModelo( metamodelo["idObjeto"] )
        idMetamodelo = atributosMetamodelo["idMetamodelo"]
        archivo.write ("-- Metamodelo: %s \nINSERT INTO XMMTMDL( ID_METAMODELO, NOMBRE_METAMODELO, ID_TIPO_RAIZ)VALUES(%s,'%s','%s');\n" % ( metamodelo["nombre"] , idMetamodelo , metamodelo["nombre"] , atributosMetamodelo["idTipoRaiz"] ) )
        tipos = ModeladorDao.getObjetosModeloByPadre( metamodelo["idObjeto"] , "Tipos" )
        for tipo in tipos:
            
            atributosTipo = ModeladorDao.getDiccionarioAtributosByObjetoModelo( tipo["idObjeto"] )
            idTipoMetamodelo = getValorVarchar (tipo[ "nombre" ])
            
            atributos = ModeladorDao.getObjetosModeloByPadre(tipo["idObjeto"],"Atributos")
            jerarquias = ModeladorDao.getObjetosModeloByPadre(tipo["idObjeto"],"Jerarquias")
            generadores = ModeladorDao.getObjetosModeloByPadre(tipo["idObjeto"],"Generadores")
            
            archivo.write("INSERT INTO XMTPMTMDL( ID_METAMODELO, ID_TIPO_METAMODELO, NOMBRE_TIPO_METAMODELO)VALUES(%s,%s,'%s');\n" % ( idMetamodelo , idTipoMetamodelo ,tipo["nombre"] ) )
            
            for atributo in atributos:
                atributosAtributo = ModeladorDao.getDiccionarioAtributosByObjetoModelo( atributo["idObjeto"] )
                archivo.write("INSERT INTO XMATRBTMTMDL( ID_METAMODELO,ID_TIPO_METAMODELO,ID_ATRIBUTO_METAMODELO, ID_TIPO_PRIMITIVO,ID_TIPO_METAMODELO_REF,ES_OBLIGATORIO, LONGITUD_ATRIBUTO,PRECISION_ATRIBUTO,ORDEN, EXP_REGULAR_VALIDACION,VALOR_DEFECTO )")
                archivo.write("VALUES( %s,%s,%s,%s,%s,%s, %s,%s,%s, %s,%s );\n" % ( idMetamodelo , idTipoMetamodelo , getValorVarchar(atributo["nombre"]) , getValorVarchar(atributosAtributo["idTipoPrimitivo"]) , getValorVarchar(atributosAtributo["idTipoMetamodeloRef"]) , getValorVarchar(atributosAtributo["esObligatorio"]) , getValorNumber(atributosAtributo["longitudAtributo"]) , getValorNumber(atributosAtributo["precisionAtributo"]) , getValorNumber(atributosAtributo["orden"]) , getValorVarchar(atributosAtributo["expRegularValidacion"]) , getValorVarchar(atributosAtributo["valorDefecto"]) ) )
            
            for jerarquia in jerarquias:
                atributosJerarquia = ModeladorDao.getDiccionarioAtributosByObjetoModelo( jerarquia["idObjeto"] )
                archivo.write("INSERT INTO XMJRRQTP( ID_METAMODELO,ID_TIPO_METAMODELO_PADRE,ID_JERARQUIA,ID_TIPO_METAMODELO_HIJO,ES_MULTIPLE )VALUES(%s,%s,%s,%s,%s);\n" % (idMetamodelo, idTipoMetamodelo, getValorVarchar(jerarquia["nombre"]) , getValorVarchar(atributosJerarquia["idTipoMetamodeloHijo"]) , getValorVarchar(atributosJerarquia["esMultiple"]) ) )
            
            for generador in generadores:
                atributosGenerador = ModeladorDao.getDiccionarioAtributosByObjetoModelo( generador["idObjeto"] )
                archivo.write("INSERT INTO XMGNRDR( ID_METAMODELO,ID_GENERADOR,NOMBRE_GENERADOR,PROGRAMA_GENERADOR,MIME_TYPE,EXTENSION )VALUES( %s,%s,%s,%s,%s,%s);\n" % ( idMetamodelo, getValorVarchar(atributosGenerador["idGenerador"]) , getValorVarchar(generador["nombre"]) , getValorVarchar(atributosGenerador["programaGenerador"]) , getValorVarchar(atributosGenerador["mimeType"]) , getValorVarchar(atributosGenerador["extension"]) ))
                
            archivo.write( "\n" )
            archivo.flush()
        resultado = {"fileName":fileName,"mimeType":modelo["__generador"]["mimeType"]}
        return resultado
    except (Exception) as ex:
        print(repr(ex))
        return {"error":repr(ex)}
            