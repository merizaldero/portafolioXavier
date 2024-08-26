import pyttsx4
import argparse
import datetime
from os.path import join, dirname, abspath

LOG_ENABLED = False

def loguear(texto, forzar = False):
    if LOG_ENABLED or forzar:
        fecha = datetime.datetime.now().isoformat()
        with open(join(dirname(abspath(__file__)), "log.log" ), 'at') as archivo :
            print('{0} {1}'.format(fecha,texto), file=archivo) 

def onStartUtterance(name):
   loguear('starting {0}'.format(name))

def onStartWord(name, location, length):
    loguear('starting word: {0},{1},{2}'.format(name, location, length))

def onFinishUtterance(name, completed):
    loguear('finishing: {0},{1}'.format(name, completed))

def onError(name, exception):
    loguear('error: {0},{1}'.format(name, repr(exception)), forzar=True)

def locutar(texto, arg_voz = None):
    if len(texto) == 0 :
        loguear('No tengo nada que decir')
    else:
        try:
            engine = pyttsx4.init()
            engine.connect("started-utterance", onStartUtterance)
            engine.connect("started-word", onStartWord)
            engine.connect("finished-utterance", onFinishUtterance)
            engine.connect("error", onError)
            #if engine.isBusy():
            #    print('El motor de Voz se encuentra ocupado')
            #else:
            voces = engine.getProperty('voices')
            voz = [x for x in voces if 'spanish' in x.name.lower() ] [0]
            if arg_voz is not None and arg_voz in [x.name for x in voces]:
                voz = [x for x in voces if x.name == arg_voz ] [0]
            engine.setProperty('voice', voz.id)
            engine.say(texto)
            engine.runAndWait()
            loguear("Dicho: {0}".format(texto))
        except Exception as ex:
            loguear('Error: {0}'.format(repr(ex)), forzar = True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Locutor en linea',
        description='locuta una linea de texto',
        epilog='Para uso del Teatro de los NPCs')
    parser.add_argument('--voz', default=None, required=False)
    parser.add_argument('--texto', default='', required=True)
    args = parser.parse_args()

    locutar( args.texto.strip() , args.voz )    