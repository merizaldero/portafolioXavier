#----------------------------------------------------------------------
# eliza.py
#
# a cheezy little Eliza knock-off by Joe Strout
# with some updates by Jeff Epler
# hacked into a module and updated by Jez Higgins
#----------------------------------------------------------------------

import string
import re
import random
import enUS as default_lang

class eliza:
    def __init__(self, langMod = default_lang):
        self.langMod = langMod
        self.patrones = [ { 'patron':x[0], 're': re.compile(x[0], re.IGNORECASE), 'respuestas':x[1] , 'feedbacks': x[2] if len(x) > 2 else [] } for x in langMod.gPats]
        self.discovery_space = [ x for x in self.patrones if x['patron'] == r'(.*)' ]
        if len(self.discovery_space) == 0 :
            self.discovery_space = None
        else:
            self.discovery_space = self.discovery_space[0]
        self.findings =[]
        print("{0} patrones".format( len (self.patrones) ))
        
    
    #---------------------------------------------------------------------- 
    # translate: take a string, replace any words found in dict.keys() 
    # with the corresponding dict.values() 
    #----------------------------------------------------------------------
    def __translate(self,str,dict): 
        words = str.lower().split()
        keys = dict.keys();
        for i in range(0,len(words)):
            if words[i] in keys:
                words[i] = dict[words[i]]
        return ' '.join(words)
    
    #----------------------------------------------------------------------
    # respond: take a string, a set of regexps, and a corresponding
    # set of response lists; find a match, and return a randomly
    # chosen response from the corresponding list.
    #----------------------------------------------------------------------
    def respond(self,str):
        # find a match among keys
        matching = [ x for x in self.patrones if x['re'].match(str) ]
        if len(matching) == 0:
            matching = self.discovery_space
        else:
            matching = matching[0]
            
        # found a match ... stuff with corresponding value
        # chosen randomly from among the available options
        match = matching['re'].match(str)
        # retroalimeenta
        for feedback in matching['feedbacks']:
           afirmacion = self.__procesar_respuesta( feedback[0], match)
           self.findings.append (afirmacion)
           self.discovery_space ['respuestas'].append (afirmacion)
           for pregunta in feedback[1]:
               patron = [ x for x in self.patrones if x['patron'] == pregunta]
               if len(patron) == 0:
                   patron = {'patron': pregunta, 're': re.compile(pregunta, re.IGNORECASE), 'respuestas': [], 'feedbacks':[] }
                   self.patrones.insert ( 0, patron)
               else:
                   patron = patron[0]
               patron['respuestas'].append (afirmacion)
        resp = random.choice( matching['respuestas'] )
        # we've got a response... stuff in reflected text where indicated
        resp = self.__procesar_respuesta( resp, match)
        return resp
        
    def __procesar_respuesta( self, resp1, match):
        resp = '{0}'.format( resp1)
        pos = resp.find('%')
        while pos > -1:
            num = int(resp[pos+1:pos+2])
            resp = resp[:pos] + self.__translate(match.group(num), self.langMod.gReflections) + resp[pos+2:]
            pos = resp.find('%')
            # fix munged punctuation at the end
            if resp[-2:] == '?.':
                resp = resp[:-2] + '.'
            if resp[-2:] == '??':
                resp = resp[:-2] + '?'
        return resp
     
#----------------------------------------------------------------------
# command_interface
#----------------------------------------------------------------------
def command_interface( langMod = default_lang ):
    for frase in langMod.presentacion:
        print(frase)
    s = ''
    therapist = eliza( langMod )
    while not(s in langMod.despedida ):
        try:
            s = input( langMod.prompt )
        except EOFError:
            s = langMod.despedida[0]
        #print(s)
        while s[-1] in '!.':
            s = s[:-1]
        print(therapist.respond(s))
    print('He aprendido lo siguiente:\n\n{0}'.format("\n".join(therapist.findings)))

if __name__ == "__main__":
    command_interface()


