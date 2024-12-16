import ModeladorDao
from os.path import join, exists
from os import sep as separador_dir
import argparse
import xpdbdd as orm
import config 
import sys

def generar(idModelo, idGenerador, path_salida):
    if not exists( path_salida ) : 
        raise Exception("path {0} no existe.").format(path_salida)
    
    archivoSalida = ModeladorDao.generarModelo(idModelo, idGenerador)
    if 'error' in archivoSalida.keys():
        raise Exception(archivoSalida['error'])
    for archivo in archivoSalida['archivos']:
        partes_path = archivo['path'].split("/")

        path_archivo = join(path_salida, separador_dir.join(partes_path))
        with open(path_archivo, 'wt', encoding='utf-8') as stream_archivo :
            stream_archivo.write(archivo['contenido'])
            stream_archivo.flush()
        print("Se ha generado " + path_archivo)
    print("Secuencia Finalizada Exitosamente.")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog = "python generar_cmd.py" , usage='%(prog)s ' + ' '.join(["<nombre_modelo>", "<nombre_generador>", "<path_salida>"]), description = "Genera Modelo por consola")
    parser.add_argument('nombre_modelo', type = str, help = 'Nombre de Modelo')
    parser.add_argument('nombre_generador', type = str, help = 'Nombre de Generador')
    parser.add_argument('path_salida', type = str, help = "Path Generacion")

    args = parser.parse_args()

    conexion = orm.Conexion(config.XPDBASEPATH)
    modeloDao = ModeladorDao.ModeloDao()
    modelo = modeloDao.getNamedQuery( conexion, "getByNombre", {'nombre':args.nombre_modelo})
    conexion.close()

    try:
        if len(modelo) == 0:        
            raise Exception("Modelo no encontrado")
        modelo = modelo[0]        
        generador = ModeladorDao.getGeneradoresByModelo(modelo['idModelo'])
        generador = [x for x in generador if x['nombreGenerador'] == args.nombre_generador]
        if len(generador) == 0:
            raise Exception("Generador no encontrado")
        generador = generador[0]

        generar(modelo['idModelo'], generador['idGenerador'], args.path_salida)
    
    except Exception as ex:
        print("Error "+ repr(ex), file = sys.stderr)
        raise ex

