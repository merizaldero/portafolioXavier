from os.path import abspath , dirname, exists, join
from os import listdir
from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH
from bottle import Bottle
import json

CONFIG = {}

NOVELAS_PATH = join( dirname(abspath( __file__ )) , 'static', "novelas" )

def servir_lista():
    lista = [ x for x in listdir(NOVELAS_PATH)]

    return template('novelas/lista', lista = lista)
                    
def rutearModulo( app : Bottle, ruta_base : str ):
    # encapsula Session Middleware
    CONFIG['RUTA_BASE'] = ruta_base

    app.route( ruta_base + '/lista' , method = ['GET'])(servir_lista)
