from os.path import abspath , dirname, exists, sep, isdir, join, basename
from os import listdir

from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH
from bottle import Bottle

CONFIG = {
    'ROOT_BVH' : '',
    'ROOT_FS_BVH' : '',    
}
ROOT_FS_BVH = ''

def buscar_archivos():
    resultado = []
    cola = [CONFIG['ROOT_FS_BVH']]
    while len(cola) > 0:
        dir = cola.pop( 0 )
        archivos = listdir( dir )
        cola += [ join(dir, x) for x in archivos if isdir( join(dir, x ) ) ]
        resultado += [ join(dir, x) for x in archivos if x.endswith('.bvh') ]
    return [ {'nombre':basename(x) , 'directorio':dirname(x) ,'path': x.replace(CONFIG['ROOT_FS_BVH'], CONFIG['ROOT_BVH'] + '/bvh' ).replace(sep, '/') } for x in resultado]

def servir_buscar_archivos():
    lista = buscar_archivos()
    print('{0} items encontrados'.format(len(lista)))
    return template('bvh_viewer/lista', lista = lista)

def servir_bvh(filepath):
    return static_file( filepath.replace('/', sep) , root = CONFIG['ROOT_FS_BVH'] )

def rutearModulo( app : Bottle, root_bvh : str , root_fs_bvh : str ):
    # encapsula Session Middleware
    CONFIG['ROOT_FS_BVH'] = root_fs_bvh
    CONFIG['ROOT_BVH'] = root_bvh

    app.route( root_bvh + '/buscar' , method = ['GET'])(servir_buscar_archivos)
    app.route( root_bvh + '/bvh/<filepath:path>' , method = ['GET'])(servir_bvh)
