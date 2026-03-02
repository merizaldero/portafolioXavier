from gtts import gTTS
from os.path import join, dirname

def locutar(texto):
    tts_file = join( dirname(__file__),"static", "locucion.mp3")
    gtts = gTTS(texto, lang= "es", tld= "com.ec", slow=False)
    gtts.save(tts_file)
    print("AUDIO GENERADO: " + texto)
        
    return "/static/locucion.mp3"