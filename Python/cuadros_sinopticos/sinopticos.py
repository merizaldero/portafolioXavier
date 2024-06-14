from os.path import abspath , dirname, exists, join
from os import listdir
from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH
from bottle import Bottle
import json

CONFIG = {}

SINOPTICOS_PATH = join( dirname(abspath( __file__ )) , "sinopticos" )

def servir_lista():
    lista = [ x[:-5] for x in listdir(SINOPTICOS_PATH) if x.endswith('.json')]

    return template('sinopticos/lista', lista = lista)
                    
def servir_item(id_sinoptico):
    nombre_archivo = join(SINOPTICOS_PATH, '{0}.json'.format(id_sinoptico))
    texto = ""
    with open( nombre_archivo ,'rt') as archivo:
        for linea in archivo:
            texto += linea
    contenido_json = json.loads(texto)
    lista = []
    cola = [ contenido_json['__objetoRaiz'] ]
    while len(cola) > 0 :
        item = cola[0]
        if len(cola) == 1:
            cola = []
        else:
            cola = cola[1:]        
        lista.append(item)
        for hijo in item['__listas']['Hijos']:
            cola.append(hijo)
        del item['__listas']
        del item['__atributos']
        del item['__jerarquias']
    return template('sinopticos/item', lista = lista, nombre_modelo = contenido_json['nombre'])

def rutearModulo( app : Bottle, ruta_base : str ):
    # encapsula Session Middleware
    CONFIG['RUTA_BASE'] = ruta_base

    app.route( ruta_base + '/lista' , method = ['GET'])(servir_lista)
    app.route( ruta_base + '/item/<id_sinoptico>' , method = ['GET'])(servir_item)
