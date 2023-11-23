prompt = '> '

despedida = [
    'chao',
    'adios',
    'gracias'
    ]

presentacion = [
    'ELIZA.ES\n---------',
    'Puedes conversar con el programa escribiéndole en Español, usando mayusculas,',
    'minisculas y puntuación de manera normal. escribe "chao" para terminar.',
    '='*72 ,
    'Hola. Como te sientes hoy?'
    ]

#----------------------------------------------------------------------
# gReflections, a translation table used to convert things you say
# into things the computer says back, e.g. "I am" --> "you are"
#----------------------------------------------------------------------
gReflections = {
    'soy' : 'eres',
    'estoy' : 'estás',
    "fui" : "fuiste",
    'estuve': 'estuviste',
    "yo" : "tú",
    "he" : "has",
    "voy a" : "vas a",
    "mi" : "tu",
    "eres" : "soy",
    'estás' : 'estoy',
    "has": "he",
    "vas a": "voy a",
    "tu" : "mi",
    "tuyo" : "mío",
    'mío' : 'tuyo',
    'mio' : 'tuyo',
    "tí" : "mí",
    "ti" : "mí",
    "a mí" : "a tí",
    "para mí" : "para tí"
    }

#----------------------------------------------------------------------
# gPats, the main response table. Each element of the list is a# two-element list; the first is a regexp, and the second is a
# list of possible responses, with group-macros labelled as
# %1, %2, etc.
#----------------------------------------------------------------------
gPats = [ 
    [r'Necesito (.*)', 
    [ "Por qué necesitas %1?", 
    "Realmente te haría bien %1?", 
    "Estás seguro que necesitas %1?"]], 

    [r'Por que no puedo ([^\?]*)\??', 
    [ "Piensas que deberías ser capaz de %1?", 
    "Qué harías si pudieras %1?", 
    "No sé -- por qué no podrías %1?", 
    "Realmente lo has intentado?"]],    
 
    [r'Por que no ([^\?]*)\??', 
    [ "Realmente piensas que yo no %1?", 
    "Quizás, eventualmente, yo voy a %1.",
    "Realmente quieres que yo %1?"]], 
    
    [r'No puedo (.*)', 
    [ "Cómo sabes que no puedes %1?", 
    "Talvez podrías %1 si lo intentaras.",
    "Qué necesitarías para %1?"]], 
    
    [r'Soy (.*)', 
    [ "Has venido conmigo porque eres %1?", 
    "Por cuanto tiempo tú has sido %1?", 
    "Cómo te sientes por el hecho ser %1?"]], 
    
    [r'Estoy (.*)', 
    [ "Has venido conmigo porque estás %1?", 
    "Por cuanto tiempo tú has estado %1?", 
    "Cómo te sientes por el hecho estar %1?"]],
    
    [r'Yo soy (.*)', 
    [ "Como te sientes por el hecho de ser %1?", 
    "Disfrutas siendo %1?", 
    "Por qué me cuentas que eres %1?", 
    "Por qué piensas que eres %1?"]],
    
    [r'Yo estoy (.*)', 
    [ "Como te sientes por el hecho de estar %1?", 
    "Disfrutas estando %1?", 
    "Por qué me cuentas que estás %1?", 
    "Por qué piensas que estás %1?"]],

    [r'Me siento (.*)', 
    [ "Como te sientes por el hecho de estar %1?", 
    "Disfrutas estando %1?", 
    "Por qué me cuentas que estás %1?", 
    "Por qué piensas que estás %1?"]],

    [r'Yo me siento (.*)', 
    [ "Como te sientes por el hecho de estar %1?", 
    "Disfrutas estando %1?", 
    "Por qué me cuentas que estás %1?", 
    "Por qué piensas que estás %1?"]],
    
    [r'Eres ([^\?]*)\??', 
    [ "Importa acaso que yo sea %1?", 
    "Preferirías que yo no fuera %1?",
    "Talvez tú crees que yo soy %1.", 
    "Podría ser yo %1 -- qué te parece?"]], 

    [r'Tu eres ([^\?]*)\??', 
    [ "Importa acaso que yo sea %1?", 
    "Preferirías que yo no fuera %1?",
    "Talvez tú crees que yo soy %1.", 
    "Podría ser yo %1 -- qué te parece?"]], 

    [r'Que (.*)', 
    [ "Por qué lo preguntas?", 
    "De que manera puede ayudarte mi respuesta?", 
    "Qué piensas tú?"]],

    [r'Como (.*)', 
    [ "Cómo supones tú?", 
    "Quizás tú puedes contestar tu propia pregunta.", 
    "Que es lo que estás preguntando realmente?"]], 
    
    [r'Porque (.*)', 
    [ "Esa es la verdadera razón?", 
    "Qué otras razones vienen a tu mente?", 
    "Esa razón se aplica a todo lo demás?", 
    "Si %1, qué más debe ser cierto?"]], 
        
    [r'(.*) lo siento (.*)', 
    [ "En muchas ocasiones no es necesario disculparse.", 
    "Qué sentimientos tienes cuando te disculpas?"]], 
    
    [r'Hola(.*)', 
    [ "Hola... me alegra que pudieras escribir hoy.", 
    "Hola... cómo estás?", 
    "Hola, cómo te sientes hoy?"]], 
    
    [r'Pienso que (.*)', 
    [ "Dudas que %1?", 
    "Realmente piensas así?", 
    "Pero tú no estas seguro de que %1?"]], 
    
    [r'(.*) amig[o|a] (.*)', 
    [ "Cuéntame más de tus amigos.", 
    "Cuando piensas en un amigo, qué es lo viene a tu mente?", 
    "Porqué no me cuentas algo de un amigo de tu infancia?"]], 
    
    [r'Si', 
    [ "Te ves bastante seguro.", 
    "OK, pero mi puedes decir algo más?"]], 
    
    [r'(.*) computadora(.*)', 
    [ "Te refieres a mí?", 
    "Se te hace extraño conversar con una compuradora?", 
    "Cómo te hacen sentir las Computadoras?", 
    "Te sientes amenazado por las computadoras?"]], 
    
    [r'Se trata de (.*)', 
    [ "Piensas que se trata de %1?", 
    "Quiza se trata de %1 -- qué te parece?", 
    "Si se tratara de %1, qué harías?", 
    "Podría bien tratarse de %1."]], 
    
    [r'Es (.*)', 
    [ "Te veo muy seguro.", 
    "Si te contara que probablemente no es %1, que te parecería?"]], 
    
    [r'Puedes ([^\?]*)\??', 
    [ "Que te hace pensar que no puedo %1?", 
    "Si yo pudiera %1, entonces qué?", 
    "Por qué me preguntas si puedo %1?"]],
    
    [r'Puedo ([^\?]*)\??', 
    [ "Tal vez no quieres %1.", 
    "Quieres ser capaz de %1?", 
    "Si tú pudieras %1, lo harías?"]], 
    
    [r'Yo no (.*)',
    [ "Tú realmente no %1?", 
    "Por qué tú no %1?", 
    "Tú quieres %1?"]], 
    
    [r'Siento que (.*)', 
    [ "Bueno, cuentsme más de esos sentimientos.", 
    "A menudo sientes que %1?",
    "Usualmente, cuando sientes que %1?",
    "Cuando sientes que %1, qué haces?"]],
    
    [r'He (.*)',
    [ "Por qué me cuentas que tú has %1?",
    "Realmente has %1?",
    "Ahora que tú has %1, que sigué?"]], 
    
    [r'Quisiera (.*)', 
    [ "Podrías explicar por qué quisieras %1?", 
    "Por qué quisieras %1?", 
    "Quién más sabe que tú quisieras %1?"]], 
    
    [r'Habra (.*)', 
    [ "Piensas que habrá %1?", 
    "Es posible que haya %1.", 
    "Te gustariá que haya %1?"]], 
    
    [r'Mi (.*)', 
    [ "Ya veo, tu %1.", 
    "por qué doces que tú %1?", 
    "Cuando %1, como te sentirás?"]], 
    
    [r'Tu (.*)', 
    [ "Deberíamos estar discutiendo acerca de tí, no de mí.", 
    "Por qué dices eso acerca de mí?", 
    "por qué te imoorta si yo %1?"]], 
    
    [r'Por que (.*)', 
    [ "Por qué no me cuentas la razón por la que %1?", 
    "Por qué piensas que %1?" ]], 
    
    [r'Quiero (.*)', 
    [ "Que sería si a ti te %1?", 
    "Por qué quieres %1?", 
    "Qué harías si a tí te %1?", 
    "Si a ti te %1, entonces que harías?"]],
    
    [r'(.*) mama (.*)', 
    [ "Cuéntame más acerca de tu madre.", 
    "Cómo era la relación con tu madre?", 
    "Cómo te sientes con respecto a tu madre?", 
    "Cómo se relaciona esto con tus sentimientos hoy?", 
    "Las buenas relsciones con la familia son importantes."]], 
    
    [r'(.*) papa (.*)', 
    [ "Cuéntame más acerca de tu padre.", 
    "Cómo te hizo sentir tu padre?", 
    "Cómo te sientes con respecto a tu padre?", 
    "Hay alguna relación entre la relación con tu padre y los sentimientos que tienes hoy?", 
    "Do you have trouble showing affection with your family?"]], 
    
    [r'(.*) nino (.*)', 
    [ "Tenías amigos cercano cuando eras niño?", 
    "Cuál es el recuerdo que más te gusta de tu niñez?", 
    "Recuerdas algún sueño o pesadilla de tu niñez?", 
    "Did the other children sometimes tease you?", 
    "Cómo piensas que tus experiencias en la niñez se relacionan con los sentimientos que tienes ahora?"]], 
    
    [r'(.*)\?', 
    [ "Por qué preguntas eso?", 
    "Por favor considera que tú puedes contestar tu propia pregunta.", 
    "Quizá la respuesta está en tí misma?", 
    "Por qué no me lo cuentas a mi?"]], 
    
    [r'chao', 
    [ "Gracias por conversar conmigo.", 
    "Hasta luego.", 
    ]], 
    
    [r'(.*)', 
    [ "Por favor cuéntame más.", 
    "Cambiemos un poco el tema... Cuéntame acerca de tu familia.", 
    "Puedes darme más detalles ?", 
    "Por qué dices que %1 ?", 
    "Ya veo.", 
    "Muy interesante.", 
    "%1.", 
    "Ya veo. Y eso qué te dice a tí ?", 
    "Cómo te hace sentir eso?", 
    "Cómo te sientes cuando dices eso ?"]] 
    
    ]


