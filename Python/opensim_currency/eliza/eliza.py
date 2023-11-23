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
import eliza.esEC as default_lang

class eliza:
    def __init__(self, langMod = default_lang):
        self.langMod = langMod
        self.keys = list(map(lambda x:re.compile(x[0], re.IGNORECASE), langMod.gPats))
        self.values = list(map(lambda x:x[1], langMod.gPats))
        # print(repr(self.keys))    
    
    #---------------------------------------------------------------------- 
    # translate: take a string, replace any words found in dict.keys() 
    # with the corresponding dict.values() 
    #----------------------------------------------------------------------
    def translate(self,str,dict): 
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
    def respond(self,str, user = None):
        # find a match among keys 
        for i in range(0, len(self.keys)):
            match = self.keys[i].match(str)

            if match:
                # found a match ... stuff with corresponding value
                # chosen randomly from among the available options

                resp = random.choice(self.values[i])
                # we've got a response... stuff in reflected text where indicated
                pos = resp.find('%')
                while pos > -1:
                    num = int(resp[pos+1:pos+2])
                    resp = resp[:pos] + \
                        self.translate(match.group(num), self.langMod.gReflections) + \
                        resp[pos+2:]
                    pos = resp.find('%')
                    # fix munged punctuation at the end
                    if resp[-2:] == '?.':
                        resp = resp[:-2] + '.'
                    if resp[-2:] == '??':
                        resp = resp[:-2] + '?'
                return resp
        return 'NPI :P'
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

if __name__ == "__main__":
    command_interface()


