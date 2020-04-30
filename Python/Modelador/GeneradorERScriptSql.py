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
        return ("NOT NULL")
    else:
        return ("")

def generarModelo(modelo):
    resultado = { 'archivos' : [ { 'path':'/script.sql', 'contenido':''} ]}
    archivo = ''
    try:
        prefijo = modelo['__objetoRaiz']['__atributos']['prefijo'].lower()
        entidades = modelo['__objetoRaiz']['__listas']['Entidades']
    
        for entidad in entidades:
            nombreTabla = entidad['__atributos']['nombreTabla']
            campos = entidad['__listas']['Campos']
            camposPk = [x for x in campos if x['__atributos']['pk'] == '1' ]
        
            archivo += "create table {0}_{1}(\n".format( prefijo, nombreTabla )
        
            primerCampo = True
            for campo in campos:
          
                nombreCampo = campo['__atributos']['nombreCampo']
                tipo = getTipo(campo)
                obligatorio = getObligatorio(campo)
                if not(primerCampo):
                    archivo += ","
                archivo += "\t {0} {1} {2}\n".format( nombreCampo , tipo , obligatorio )
                primerCampo = False
            if len(camposPk) > 0:
                archivo += ",\tPRIMARY KEY ("
                primerCampo = True
                for campo in camposPk:
                    nombreCampo = campo['__atributos']['nombreCampo']
                    if not(primerCampo):
                        archivo += ","
                    archivo += " {0} ".format(nombreCampo)
                    primerCampo = False
                archivo += ")\n"
            archivo += ");\n"
        archivo += "-- Fin de Generacion\n"
    except (Exception) as ex:
        pass    
    #print(archivo)
    resultado['archivos'][0]['contenido'] = archivo
    return resultado
    
    
    
    


            