from os.path import join, dirname, abspath
from os.path import exists as exists_file
from os import listdir
from urllib.parse import quote

from bottle import Bottle, static_file, redirect, abort
import mido
import threading

PATH_KARAOKES = join(dirname(abspath(__file__)),"kars")  # r'C:\Users\XAVIER\Music\midis'

PLAYING_THREAD = {'hilo':None}

def servir_main():
    redirect ("/static/index.html")

def servir_list_karaokes():
    lista = [ x for x in listdir(PATH_KARAOKES) if x.lower().endswith('.kar') ]
    lista = [ {'label':x[:-4], 'slug':quote(x) } for x in lista]
    return {'lista':lista}
    
def servir_midi_karaoke(nombre_archivo):
    filename = join(PATH_KARAOKES,f"{nombre_archivo}")
    if not exists_file(filename):
        abort(404, 'Karaoke Solicitado no existe')
    return static_file(f"{nombre_archivo}", root = PATH_KARAOKES, mimetype = 'audio/midi')

def servir_midi_letra(nombre_archivo):
    filename = join(PATH_KARAOKES, f"{nombre_archivo}")
    if not exists_file(filename):
        abort(404, 'Karaoke Solicitado no existe')
    mid = mido.MidiFile(filename)

    ticks_per_beat = mid.ticks_per_beat
    tempo = 500000
    tiempo_acumulado = 0.0
    mensajes = [x.dict() for x in mid.merged_track]
    for x in mensajes:
        if x['type'] == 'set_tempo':
            tempo = x['tempo']
        elif x['type'] == 'text':
            for reemplazable in ["/", "\\"]:
                x['text'] = x['text'].replace(reemplazable,"\n")
            x['previous_seconds'] = tiempo_acumulado
            tiempo_acumulado = 0.0
        if 'time' in x:
            tiempo_acumulado += mido.tick2second(x['time'], ticks_per_beat, tempo)

    textos = [x for x in mensajes if x['type'] == 'text' and not x['text'].startswith("@")]

    for indice,x in enumerate(textos):
        arreglo_antes = textos[ : indice ]
        arreglo_antes.reverse()
        arreglo_despues = textos[ indice + 1 : ]
        posiciones_salto_linea_antes = [indice1 for indice1, y in enumerate(arreglo_antes) if "\n" in y['text'] ]
        posiciones_salto_linea_despues = [indice1 for indice1, y in enumerate(arreglo_despues) if "\n" in y['text'] ]
        offset_inicial = 0
        offset_final = len(textos)
        if len(posiciones_salto_linea_antes) >= 2:
            offset_inicial = indice - posiciones_salto_linea_antes[1] - 1
            if offset_inicial < 0:
                offset_inicial = 0
        if len(posiciones_salto_linea_despues) >= 2:
            offset_final = indice + posiciones_salto_linea_despues[1] + 1
            if offset_final >= len(textos):
                offset_final = len(textos)
        x['texto_resaltado'] = "".join([y['text'] for y in textos[offset_inicial : indice + 1] ])
        x['texto_pendiente'] = "".join([y['text'] for y in textos[indice + 1 : offset_final] ])

    def reproducir_cancion():
        port = mido.open_output(mido.get_output_names()[0])
        for msg in mid.play():
            port.send(msg)
        port.close()
        PLAYING_THREAD['hilo'] = None
    
    if PLAYING_THREAD['hilo'] is not None:
        PLAYING_THREAD['hilo'].stop()

    PLAYING_THREAD['hilo'] = threading.Thread(target = reproducir_cancion, args=(), kwargs={})
    PLAYING_THREAD['hilo'].start()

    return {'letra': textos}

def rutearModulo( app : Bottle, ruta_base : str ):
    # encapsula Session Middleware

    app.route( ruta_base + '/' , method = ['GET'])(servir_main)
    app.route( ruta_base + '/karaokes/<nombre_archivo>' , method = ['GET'])(servir_midi_karaoke)
    app.route( ruta_base + '/letra/<nombre_archivo>' , method = ['GET'])(servir_midi_letra)
    app.route( ruta_base + '/karaokes' , method = ['GET'])(servir_list_karaokes)
    