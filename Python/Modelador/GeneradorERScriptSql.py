import ModeladorDao
import config

def getObjetosModeloByTipo( modelo, idTipoMetamodelo ):
    resultado = []
    cola = [modelo['__objetoRaiz']]
    while len(cola) > 0:
        objetoModelo = cola.pop(0)
        if objetoModelo['idTipoMetamodelo'] == idTipoMetamodelo:
            resultado.append(objetoModelo)
        for lista in objetoModelo['__listas'].keys():
            for hijo in objetoModelo['__listas'][lista]:
                cola.append(hijo)
    return resultado

def getObjetoPadre(modelo, idObjeto):
    cola = [modelo['__objetoRaiz']]
    while len(cola) > 0:
        objetoModelo = cola.pop(0)
        for lista in objetoModelo['__listas'].keys():
            for hijo in objetoModelo['__listas'][lista]:
                if hijo['idObjeto'] == idObjeto:
                    return objetoModelo
                cola.append(hijo)
    return None

def getTipo(campo):
    if campo['__atributos']["tipo"] in ["STRING","EMAIL"]:
        return "varchar (%s)" % campo['__atributos']["tamano"]
    elif campo['__atributos']["tipo"] == 'INTEGER':
        return "integer"
    elif campo['__atributos']["tipo"] == 'LONG':
        return "bigint"
    elif campo['__atributos']["tipo"] == 'DECIMAL':
        return "decimal (%s,%s)"%(campo['__atributos']["tamano"],campo['__atributos']["precision"])
    elif campo['__atributos']["tipo"] == 'BOOLEAN':
        return "char(1)"
    else:
        return campo['__atributos']["tipo"]
        
def getObligatorio(campo):
    if campo['__atributos']["obligatorio"] == "1":
        return "NOT NULL"
    else:
        return ""
def getAutonumerico(campo):
    if campo['__atributos']["incremental"] == "1":
        return "auto_increment"
    else:
        return ""

def defaultTableNamer(entidad,modelo):
    prefijo = modelo['__objetoRaiz']['__atributos']['prefijo'].lower()
    nombreTabla = entidad['nombre']
    if entidad['idTipoMetamodelo'] == 'ENTIDAD':
        nombreTabla = entidad['__atributos']['nombreTabla']
    elif entidad['idTipoMetamodelo'] == 'NAMED_QUERY':
        nombreTabla = entidad['__atributos']['nombreIndice']
    return "{0}{1}".format(prefijo,nombreTabla)

def obtenerCreateTable(entidad, modelo, table_namer = defaultTableNamer):    
    nombreTabla = entidad['__atributos']['nombreTabla']
    campos = entidad['__listas']['Campos']
    camposPk = [x for x in campos if x['__atributos']['pk'] == '1' ]
    namedQueries = entidad['__listas']['NamedQuieries']

    if 'entidadUsuario' in entidad['__atributos'].keys() and entidad['__atributos']['entidadUsuario'] == '1':
        campos = campos + [{'nombre':'id_user' , '__atributos':{ 'nombreCampo':'ID_USER', 'tipo': 'INTEGER', 'obligatorio':True, 'incremental':False } }]

    maestro = getObjetoPadre(modelo, entidad['idObjeto']) if entidad['idJerarquia'] == 'EntidadesDetalle' else None
    if maestro is not None:
        id_maestro = "id_" + maestro['nombre'].lower()
        #fk_maestro = "FK_{0}_{1}".format( nombreTabla.upper(), maestro['nombre'].upper() ) 
        campos = campos + [{'nombre':id_maestro , '__atributos':{ 'nombreCampo':id_maestro.upper(), 'tipo': 'INTEGER', 'obligatorio':True, 'incremental':False } }]
        print("Se incorpora {0} a campos de {1}".format(id_maestro, entidad['nombre'])) 

    lista_campos = []
    for campo in campos:
        nombreCampo = campo['__atributos']['nombreCampo'].lower()
        tipo = getTipo(campo)
        obligatorio = getObligatorio(campo)
        autonumerico = getAutonumerico(campo)
        lista_campos.append( "\t{0} {1} {2} {3}".format( nombreCampo , tipo , obligatorio, autonumerico ) ) 
    if len(camposPk) > 0:
        lista_pk = [ campo['__atributos']['nombreCampo'].lower() for campo in camposPk ]
        lista_campos.append( "\tPRIMARY KEY  ( {0} )".format(", ".join(lista_pk)  ) )
    for namedQuery in namedQueries:
        unique_flag = ''
        campos_where = namedQuery['__listas']['camposWhere']
        lista_campos_key = [ "{0}".format( campo['__atributos']['nombreCampo'].lower() ) for campo_where in campos_where for campo in campos if campo['nombre'] == campo_where['nombre']  ]
        if namedQuery['__atributos']['indiceUnico'] == '1':
            unique_flag = 'UNIQUE '
        if len(lista_campos_key) > 0:
            lista_campos.append( "\t{0}KEY {1} ({2})".format( unique_flag, table_namer(namedQuery,modelo), ", ".join(lista_campos_key) ) )
    archivo = "CREATE TABLE {0} (\n{1}\n);\n".format( table_namer(entidad,modelo) , ",\n".join(lista_campos) )
    return archivo
            
def generarModelo(modelo):
    resultado = { 'archivos' : [ { 'path':'/script.sql', 'contenido':''} ]}
    archivo = ''
    entidades = getObjetosModeloByTipo(modelo, 'ENTIDAD') # modelo['__objetoRaiz']['__listas']['Entidades']    
    for entidad in entidades:
        archivo += obtenerCreateTable(entidad , modelo )
    archivo += "-- Fin de Generacion\n"
    
    #print(archivo)
    resultado['archivos'][0]['contenido'] = archivo
    return resultado
    
    
    
    


            