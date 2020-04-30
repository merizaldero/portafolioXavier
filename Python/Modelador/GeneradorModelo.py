import imp
import config

generadorHash ={}

def generarModelo(modelo,generador):
    resultado = None
    try:
        modulo = None
        #Asegura que el modulo generador esté cargado
        if not ( modelo['idMetamodelo'] in generadorHash):
            generadorHash[ modelo['idMetamodelo'] ] = {}
        if generador['idGenerador'] in generadorHash[ modelo['idMetamodelo'] ] :
            modulo = generadorHash[ modelo['idMetamodelo'] ] [ generador['idGenerador'] ]
        else:
            modulo = imp.load_source( "generador_{0}_{1}".format( modelo['idMetamodelo'], generador['idGenerador'] )  , config.APP_ROOT+"/" + generador["programaGenerador"] + ".py" )
            generadorHash[ modelo['idMetamodelo'] ] [ generador['idGenerador'] ] = modulo
            #if not ('generarModelo' in modulo):
            #    modulo = None
        # si el modulo no tiene funcion generarModelo, no se devuelve resultado
        if modulo is None:
            return {'error': 'Generador no valido'}
        
        resultado = getattr(modulo,"generarModelo")(modelo)
        
        return resultado 
    except (Exception) as ex:
        return {"error":repr(ex)}
        
 
 
 
   