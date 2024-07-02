import lotto
import xpd_orm as orm
from nltk.probability import FreqDist
import numpy as np

import requests
import pytesseract
from os.path import join, exists
import cv2
from matplotlib import pyplot as plt
import re

PIC_FOLDER = 'lotto_pics'
URL_BASE = "https://ventas-api.loteria.com.ec/uploads/boletines/T{0}.jpg"

# Extrae imagenes
def extraer_boletines():
    sorteo = lotto.find_ultimo_sorteo()[0] + 1
    while True:
        path_archivo = join(PIC_FOLDER,"{0}.jpg".format(sorteo))
        if exists(path_archivo):
            print('Boletin {0} ya existe'.format(sorteo))
            sorteo += 1
            continue
        respuesta = requests.get(URL_BASE.format(sorteo), verify = False)
        if respuesta.status_code != 200:        
            respuesta.close()
            print('Boletin {0} no esta disponible'.format(sorteo))
            break
        archivo = open( path_archivo, "wb" )
        archivo.write(respuesta.content)
        archivo.close()
        print('Boletin {0} extraido'.format(sorteo))
        sorteo += 1

    print('Extraidos ultimos boletines')

def extraer_numeros_loteria(numero_sorteo, path_archivo, umbral = 242, mostrar_imagen=False, solo_numeros_loteria = True):
    imagen = cv2.imread(path_archivo, cv2.IMREAD_GRAYSCALE)
    imagen_umbralizada = imagen
    ret, imagen_umbralizada = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY)    
    tamano = imagen_umbralizada.shape[:2]
    imagen_umbralizada = imagen_umbralizada[ : int(tamano[0] * 0.55) ,  :  ]
    
    hallazgos = pytesseract.image_to_string( imagen_umbralizada ).split()
    expresion_num_loteria = re.compile(r'^\d{6}$')
    if solo_numeros_loteria:
        hallazgos = [ x for x in hallazgos if expresion_num_loteria.match(x) ]
    hallazgos1 = []
    sorteo = {'id': numero_sorteo, 'fecha': ''}
    lotto.transaccionar(lotto.crear_sorteo, sorteo)
    orden = 1
    for h in hallazgos:
        if h not in hallazgos1:
            premiado = {'id_sorteo': numero_sorteo, 'orden':orden, 'premiado': h}
            lotto.transaccionar(lotto.crear_premiado, premiado)
            hallazgos1.append(h)
            orden += 1
    if mostrar_imagen:
        print(imagen_umbralizada.shape)
        plt.figure(figsize=(10,10))
        plt.imshow(cv2.cvtColor(imagen_umbralizada, cv2.COLOR_GRAY2BGR))
        plt.show()
        plt.close()
    
    return hallazgos1

# Persiste los sorteos desde imagenes

def persistir_sorteos():
    sorteo = lotto.find_ultimo_sorteo()[0] + 1
    umbrales = [242,128,64]
    while True:
        path_archivo = join(PIC_FOLDER,"{0}.jpg".format(sorteo))
        if not exists(path_archivo):
            print("info para sorteo {0} no disponible".format(sorteo))
            break
        numeros_encontrados = []
        for umbral in umbrales:
            numeros_encontrados1 = extraer_numeros_loteria ( sorteo, path_archivo , umbral= umbral )
            if len(numeros_encontrados1) > len(numeros_encontrados):
                numeros_encontrados = numeros_encontrados1
        linea = "{0},{1}".format(sorteo,','.join(numeros_encontrados))
        print(linea)
        sorteo += 1
    print("Informacion de sorteos persistida")

def calcular_probabilidades():
    con = orm.Conexion(lotto.PATH_BDD)
    try:
        # recupera todos los premiados
        premiados = lotto.Premiados.getNamedQuery(con, "findAll",{})
        probabilidades = lotto.Probabilidades.getNamedQuery(con, 'findAll', {})
        for posicion in lotto.POSICIONES:
            vector = [ premiado['premiado'][posicion] for premiado in premiados ]
            probabilidades_posicion = dict(FreqDist(vector))
            probabilidades_posicion_persistencia = []
            for digito in lotto.DIGITOS:
                probabilidad = [ p for p in probabilidades if p['posicion'] == posicion and p['digito'] == digito ][0]
                if digito in probabilidades_posicion.keys():
                    probabilidad['probabilidad'] = (probabilidades_posicion[digito] + 0.0) / len(premiados)
                else:
                    probabilidad['probabilidad'] = 0.0
                probabilidades_posicion_persistencia.append(probabilidad)
            # probabilidades_lst = list(set( [ x['probabilidad'] for x in probabilidades_posicion_persistencia ] ))
            probabilidades_lst = [ x['probabilidad'] for x in probabilidades_posicion_persistencia ]
            # crea ranking por posicion
            avg_probabilidad = np.median(probabilidades_lst)
            std_probabilidad = np.std(probabilidades_lst)
            # min_green = min_probabilidad + ( max_probabilidad - min_probabilidad ) * 2 / 3
            min_green = avg_probabilidad + std_probabilidad
            # min_yellow = min_probabilidad + ( max_probabilidad - min_probabilidad ) * 2 / 3
            min_yellow = avg_probabilidad - std_probabilidad
            rankings = {}
            for probabilidad in set(probabilidades_lst):
                if probabilidad >= min_green:
                    rankings[probabilidad] = 'success'
                elif probabilidad >= min_yellow:
                    rankings[probabilidad] = 'warning'
                else:
                    rankings[probabilidad] = 'danger'
            # asigna ranking y actualiza probabilidad
            for probabilidad in probabilidades_posicion_persistencia:
                probabilidad['ranking'] = rankings[ probabilidad['probabilidad'] ]
                lotto.Probabilidades.actualizar(con, probabilidad)
        con.commit()
    except Exception as ex:
        con.rollback()
        print(repr(ex))
        raise Exception( str(ex) )
    finally:
        con.close()    

if __name__ == "__main__":
    extraer_boletines()
    persistir_sorteos()
    calcular_probabilidades()