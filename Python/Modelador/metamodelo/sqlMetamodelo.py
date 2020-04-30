import json

def nullSiVacio( valor1 , con_comillas = True):
    if valor1 is None or valor1 == '' or valor1 == "null":
        return 'NULL'
    else:
        comillas = "'" if con_comillas else ''
        return "{0}{1}{0}".format(comillas, valor1)

def generarModelo( modelo ):
        
    #cargar raiz ,tipos, catalogos, generadores
    metamodelo = modelo['__objetoRaiz']
    tiposMetamodelo = metamodelo['__listas']['Tipos']
    tipoRaiz = [tipo for tipo in tiposMetamodelo if str(tipo['idObjeto']) == metamodelo['__atributos']['idTipoRaiz'] ] [0]
    idMetamodelo = metamodelo['__atributos']['idMetamodelo']
    catalogos = metamodelo['__listas']['Catalogos']
    generadores = metamodelo['__listas']['Generadores']
    
    print(json.dumps(tiposMetamodelo))
    
    archivo =  "--  {0}\n".format( modelo['nombre'] )
    archivo += "INSERT INTO XMMTMDL( ID_METAMODELO, NOMBRE_METAMODELO, ID_TIPO_RAIZ) VALUES( {0}, '{1}', '{2}');\n".format( 
        idMetamodelo,
        metamodelo['nombre'],
        tipoRaiz['nombre'])
    for tipo in tiposMetamodelo:
        tipoMetamodelo = tipo['nombre']
        campos = tipo['__listas']['Atributos']
        jerarquias = tipo['__listas']['Jerarquias']
        archivo += "  INSERT INTO XMTPMTMDL( ID_METAMODELO, ID_TIPO_METAMODELO, NOMBRE_TIPO_METAMODELO) VALUES ({0}, '{1}', '{2}');\n".format(
            idMetamodelo,
            tipoMetamodelo,
            tipoMetamodelo.capitalize()
            )
        orden = 1
        for campo in campos:
            idTipoPrimitivo = nullSiVacio( campo['__atributos']['tipoPrimitivo'] )
            idTipoMetamodeloRef = nullSiVacio( campo['__atributos']['tipoMetamodeloRef'] , False )
            if idTipoMetamodeloRef != 'NULL':
                print('buscando tipo ' + idTipoMetamodeloRef)
                filtrado = [ tipo1 for tipo1 in tiposMetamodelo if str(tipo1['idObjeto']) == idTipoMetamodeloRef ]
                idTipoMetamodeloRef = "'{0}'".format( filtrado[0]['nombre'] ) if len(filtrado) > 0 else "'NO_VALIDO'"
            obligatorio = nullSiVacio( campo['__atributos']['obligatorio'] )
            longitud = nullSiVacio( campo['__atributos']['longitud'] , False)
            precision = nullSiVacio( campo['__atributos']['precision'] , False)
            expRegularValidacion = nullSiVacio( campo['__atributos']['expresionRegularValidacion'] )
            valorDefecto = nullSiVacio( campo['__atributos']['valorDefecto'] )
            idCatalogo = nullSiVacio( campo['__atributos']['catalogo'], False )
            if idCatalogo != 'NULL':
                filtrado = [ catalogo1 for catalogo1 in catalogos if str(catalogo1['idObjeto']) == idCatalogo ]
                idCatalogo = "'{0}'".format( filtrado[0]['nombre']) 
            archivo += "    INSERT INTO XMATRBTMTMDL( ID_METAMODELO, ID_TIPO_METAMODELO, ID_ATRIBUTO_METAMODELO, ID_TIPO_PRIMITIVO, ID_TIPO_METAMODELO_REF, ES_OBLIGATORIO, LONGITUD_ATRIBUTO, PRECISION_ATRIBUTO, ORDEN, EXP_REGULAR_VALIDACION, VALOR_DEFECTO, ID_CATALOGO )VALUES( {0}, '{1}', '{2}', {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11});\n".format(
                idMetamodelo,
                tipoMetamodelo,
                campo['nombre'],
                idTipoPrimitivo,
                idTipoMetamodeloRef,
                obligatorio, 
                longitud,
                precision,
                orden, 
                expRegularValidacion,
                valorDefecto,
                idCatalogo
                )
            orden = orden + 1
        for jerarquia in jerarquias:
            idJerarquia = jerarquia['nombre']
            idTipoHijo = nullSiVacio( jerarquia['__atributos']['idTipoMetamodeloHijo'] ,False )
            if idTipoHijo != 'NULL':
                filtrado = filtrado = [ tipo1 for tipo1 in tiposMetamodelo if str(tipo1['idObjeto']) == idTipoHijo ]
                idTipoHijo = "'{0}'".format( filtrado[0]['nombre'] ) if len(filtrado) > 0 else "'NO_VALIDO'"
            esMultiple = nullSiVacio( jerarquia['__atributos']['esMultiple'] )
            archivo += "    INSERT INTO XMJRRQTP( ID_METAMODELO, ID_TIPO_METAMODELO_PADRE, ID_JERARQUIA, ID_TIPO_METAMODELO_HIJO, ES_MULTIPLE )VALUES( {0}, '{1}', '{2}', {3}, {4} );\n".format(
                idMetamodelo,
                tipoMetamodelo,
                idJerarquia,
                idTipoHijo,
                esMultiple
                )
                
    for catalogo in catalogos:
        idCatalogo = catalogo['nombre']
        valores = catalogo['__listas']['Valores']
        archivo += "  INSERT INTO XMCTLG( ID_METAMODELO, ID_CATALOGO, NOMBRE_CATALOGO )VALUES( {0}, '{1}' , '{2}');\n".format(
            idMetamodelo,
            idCatalogo,
            idCatalogo.capitalize()
            )
        orden = 1
        for valor in valores:
            clave = valor['nombre']
            etiqueta = valor['__atributos']['etiqueta']
            archivo += "      INSERT INTO XMCTLGVLR ( ID_METAMODELO, ID_CATALOGO, CLAVE, ETIQUETA, ORDEN )VALUES( {0}, '{1}', '{2}', '{3}', {4});\n".format(
                idMetamodelo,
                idCatalogo,
                clave,
                etiqueta,
                orden
                )
            orden = orden + 1
            
    for generador in generadores:
        idGenerador = generador['nombre']
        nombreGenerador = generador['__atributos']['nombreGenerador']
        programaGenerador = generador['__atributos']['programaGenerador']
        archivo += "  INSERT INTO XMGNRDR( ID_METAMODELO, ID_GENERADOR, NOMBRE_GENERADOR, PROGRAMA_GENERADOR, MIME_TYPE, EXTENSION )VALUES( {0}, '{1}' ,'{2}' ,'{3}','text/text','.sql' );\n".format(
            idMetamodelo,
            idGenerador,
            nombreGenerador,
            programaGenerador
            )
    resultado = { 'archivos' : [ 
        { 'path':'/script.sql', 'contenido':archivo} 
        , { 'path':'/export.json', 'contenido': json.dumps( modelo, sort_keys = False, indent = 2, separators = (',',':') ) }
        ]}
    return resultado
 
        
        
