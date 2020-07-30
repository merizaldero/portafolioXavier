import ModeladorDao
import config

def getTipo(campo):
    if campo['__atributos']["tipo"] == "STRING":
        return ("VARCHAR (%s)"%campo['__atributos']["tamano"])
    elif campo['__atributos']["tipo"] == 'INTEGER':
        return ("INTEGER")
    elif campo['__atributos']["tipo"] == 'LONG':
        return ("BIGINT")
    elif campo['__atributos']["tipo"] == 'DECIMAL':
        return ("DECIMAL (%s,%s)"%(campo['__atributos']["tamano"],campo['__atributos']["precision"]))
    elif campo['__atributos']["tipo"] == 'BOOLEAN':
        return ("CHAR(1)")
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
    nombreTabla = entidad['__atributos']['nombreTabla']
    return "{0}{1}".format(prefijo,nombreTabla)

def obtenerCreateTable(entidad, modelo, table_namer = defaultTableNamer):    
    nombreTabla = entidad['__atributos']['nombreTabla']
    campos = entidad['__listas']['Campos']
    camposPk = [x for x in campos if x['__atributos']['pk'] == '1' ]
    lista_campos = []
    for campo in campos:
        nombreCampo = campo['__atributos']['nombreCampo'].lower()
        tipo = getTipo(campo)
        obligatorio = getObligatorio(campo)
        autonumerico = getAutonumerico(campo)
        lista_campos.append( "\t{0} {1} {2} {3}".format( nombreCampo , tipo , obligatorio, autonumerico ) ) 
    if len(camposPk) > 0:
        lista_pk = [ campo['__atributos']['nombreCampo'].lower() for campo in camposPk ]
        lista_campos.append( "\tPRIMARY KEY ( {0} )".format(", ".join(lista_pk)) )
    archivo = "create table {0} (\n{1}\n);\n".format( table_namer(entidad,modelo) , ",\n".join(lista_campos) )
    return archivo
            
def generarModelo(modelo):
    resultado = { 'archivos' : [ { 'path':'/script.sql', 'contenido':''} ]}
    archivo = ''
    entidades = modelo['__objetoRaiz']['__listas']['Entidades']    
    for entidad in entidades:
        archivo += obtenerCreateTable(entidad , modelo )
    archivo += "-- Fin de Generacion\n"
    
    #print(archivo)
    resultado['archivos'][0]['contenido'] = archivo
    return resultado
    
    
    
    


            