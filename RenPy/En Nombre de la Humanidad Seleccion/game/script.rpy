﻿# Coloca el código de tu juego en este archivo.

define nombre_prota = "Juan Salvador" 

# Declara los personajes usados en el juego como en el ejemplo:

# representa su lealtad, confianza y sabiduría, junto con tonos de verde oliva (#556B2F) para reflejar su pragmatismo y habilidad para adaptarse a diferentes situaciones.
define prota = Character("[nombre_prota]", color = "#0F52BA")
# reflejar su ambición y pasión, con tonos de rosa (#FF69B4) para reflejar su encanto y empatía.
define carla = Character("Carla", color = "#8B0000")
# representar su perfeccionismo, seriedad y autoridad, con tonos de morado (#9400D3) para reflejar su creatividad y determinación.
define anta = Character("Alexander", color = "#363636")
# reflejar su tranquilidad y serenidad, con tonos de gris claro (#D3D3D3) para representar su neutralidad y objetividad.
define jefe_prota = Character("Jefe", color = "#ADD8E6")
# Compañera de trabajo Emily representar su dulzura, junto con tonos de amarillo (#FFFF00) para reflejar su entusiasmo y optimismo.
define emily = Character("Emily", color = "#FFB6C1", who_outlines=[( 1, "#884040", 0, 0 )] )
# Científico jefe del proyecto: Verde oscuro (#006400) para representar su conocimiento y perspicacia, con tonos de gris claro (#D3D3D3) para representar su imparcialidad y sentido común
define cientifico_jefe = Character("Científico Jefe", color = "#006400")
# Piloto de la nave: Gris oscuro (#363636) para reflejar su profesionalismo y seriedad, con tonos de azul claro (#87CEFA) para representar su habilidad y seguridad.
define piloto = Character("Piloto", color = "#363636")
# Ingeniero jefe: Naranja oscuro (#FF8C00) para representar su energía y creatividad, con tonos de amarillo (#FFFF00) para reflejar su ingenio y optimismo.
define ingeniero_jefe = Character("Ingeniero Jefe", color = "#FF8C00")
# Técnico de la nave: Gris claro (#D3D3D3) para representar su neutralidad y practicidad, con tonos de verde claro (#ADFF2F) para reflejar su tranquilidad y confiabilidad.
define tecnico_nave = Character("Técnico jefe", color = "#D3D3D3")
# Fuerzas Especiales podría ser el negro (#000000), que transmite una sensación de autoridad, misterio y oscuridad. También puede ser un tono de gris oscuro como #333333 o #444444 para representar un tono más discreto y sigiloso.
define fuerzas_especiales = Character("Técnico jefe", color = "#444444")

# Mr Thompson. jefe de recursos humanos
define sr_thompson = Character("Sr. Thompson", color = "#ADD8E6", who_outlines=[( 1, "#566473", 0, 0 )])
# Compañera de trabajo Emily representar su dulzura, junto con tonos de amarillo (#FFFF00) para reflejar su entusiasmo y optimismo.
define secretaria = Character("Secretaria", color = "#FFB6C1", who_outlines=[( 1, "#884040", 0, 0 )] )

#Presentador de capitulos
define presentador_capitulos = Character(what_xalign=0.5, what_yalign=0.5, what_bold = True, what_color = "#ffffff", what_size = 40, window_background = None, window_yalign = 0.5, what_outlines=[( 1, "#404040", 0, 0 )])

# Logo Saga 
image logo_saga text = Text("EN NOMBRE DE LA HUMANIDAD", size=40, color="#8B0000" )

image logo_seleccion text = Text("Selección", size=40, color="#620404" )

image bg negro = "#000000"

# Pantalla Completa
transform pantalla_completa:
    size(1280, 720)
    xalign 0.5
    yalign 0.5

transform posicion_subtitulo:
    xalign 0.5
    yalign 0.65

transform prota_aureo:
    xalign 0.67
    yalign 0.5

transform anti_aureo:
    xalign 0.33
    yalign 0.5

transform cuarto_1:
    xalign 0.15
    yalign 0.5

transform cuarto_3:
    xalign 0.85
    yalign 0.5

# El juego comienza aquí.

label start:

    # La pantalla muestra el título de la novela visual "Seleccion" junto con una imagen de un planeta azul.

    scene bg orbita at pantalla_completa
    with Dissolve(2.0)

    pause(3.0)

    show logo_saga text at truecenter
    with Dissolve(2.0)
    show bg negro at pantalla_completa behind logo_saga
    show logo_seleccion text at posicion_subtitulo
    with Dissolve(0.5)

    pause

    scene bg negro

    # Solicita al jugador confirmar su nombre

    python:
        nombre_prota = renpy.input( _("Cuál es tu nombre? Escríbelo aquí si no es {b}{color=#0F52BA}[nombre_prota]{/color}{/b}") )

        nombre_prota = nombre_prota.strip() or __("Juan Salvador")    

label introduciendo_protagonista:

    scene bg negro
    presentador_capitulos "Capítulo 1\nIntroducción"
    with Dissolve(1.0)

    # El narrador introduce al protagonista, describiéndolo como un joven ingeniero graduado de la Universidad Latinoamericana de Ingeniería y Tecnología (ULIT), que aspira a trabajar en la multinacional Sterling Dynamics.

    # Muestra una imagen de fondo: Aquí se usa un marcador de posición por
    # defecto. Es posible añadir un archivo en el directorio 'images' con el
    # nombre "bg room.png" or "bg room.jpg" para que se muestre aquí.

    scene bg universidad at pantalla_completa
    with Dissolve(1.0)

    # Muestra un personaje: Se usa un marcador de posición. Es posible
    # reemplazarlo añadiendo un archivo llamado "eileen happy.png" al directorio
    # 'images'.

    show prota graduado at prota_aureo

    # Presenta las líneas del diálogo.

    prota "Bueno, estoy finalmente graduado."
    show prota graduado_aliviado:
        xalign 0.5
        yalign 0.5
    prota "Qué alivio!"
    
    show prota graduado at prota_aureo
    prota "Pero ahora, ¿qué sigue?"
    prota "Tengo que empezar a buscar empleo,\nno puedo seguir de mantenido en la casa"
    prota "pero no tengo idea de por dónde empezar."
    prota "Qué habilidades tengo que pueda enfatizar en mi currículum?\n¿Qué tipo de trabajos están disponibles?\n¿Qué empresas están contratando ingenieros recién graduados?"
    
    show prota graduado_reflexion at prota_aureo
    with Dissolve(1.0)
    prota "Debería buscar en línea, pero la cantidad de sitios web que ofrecen trabajo es abrumadora.\nCómo sé qué sitios son confiables?" 
    prota "También podría hablar con mis profesores o compañeros de clase para obtener recomendaciones,\npero ¿y si no tienen ninguna idea?"
    prota "Tal vez necesito hacer una lista de las habilidades que tengo y de lo que me interesa."
    prota "Luego, puedo buscar trabajos que se ajusten a mis habilidades e intereses."
    prota "Y también debería investigar las empresas que me interesan para ver si tienen una cultura laboral que encaje con lo que busco."
    
    scene bg habitacion at pantalla_completa
    with Dissolve(1.0)

    show prota reflexion at prota_aureo

    prota "Esto se siente un poco abrumador,"
    prota "pero también sé que tengo muchas opciones y que mi título de ingeniero es un buen punto de partida."
    
    show prota neutro at prota_aureo

    prota "Solo necesito empezar y seguir adelante con la búsqueda de un empleo."
    prota "Por ahora, descansaré. Mañana será un nuevo día."

label entrevista:

    scene bg negro
    presentador_capitulos "Capítulo 2\nLa Entrevista de Trabajo"
    with Dissolve(1.0)

    # La escena cambia a la oficina de Sterling Dynamics, donde el protagonista está siendo entrevistado por el gerente de recursos humanos, el Sr. Thompson.
    prota "Cuanto tiempo he estado buscando trabajo?"
    prota "La verdad, eso ya no importa."
    prota "Aquel par de empresas en las que estuve aplicando, aparentemente no tenían una oferta seria para mi."
    prota "Parece que el destino me estuvo encaminando todo este tiempo a aplicar a esta empresa ..."

    scene bg sterlingco_exterior at pantalla_completa
    with Dissolve(0.2)
    presentador_capitulos "Sterling Dynamics !!"

    prota "Una multinacional de consultoría de vanguardia en Tecnología Aeroespacial, con presencia en todo el mundo."
    prota "Trabajar aquí te implica que eres parte de la crema y nata en tecnología."
    prota "Y yo, tengo cita para una entrevista laboral con ellos ... HOY !!"

    scene bg sala_espera_hr at pantalla_completa
    with Dissolve(0.5)

    prota "Llegué a tiempo. eso es bueno."
    prota "De todas formas, no soy el único candidato. "
    prota "Uno de ellos me resulta conocido ... de la Universidad."

    show secretaria hr at anti_aureo
    secretaria "Señor {b}[nombre_prota]{/b}, por favor acérquese."
    
    # Durante la entrevista, el Sr. Thompson le pregunta al protagonista sobre su experiencia y habilidades, y le explica sobre el proyecto "X-Odus".

    scene bg oficina_hr at pantalla_completa
    with Dissolve(0.5)

    show mr thompson at cuarto_1
    with Dissolve(0.5)

    sr_thompson "Bienvenido, Sr. {b}[nombre_prota]{/b}.\nPuede llamarme {b}Thompson{/b}.\nTome asiento, por favor."

    show prota terno at cuarto_3
    with Dissolve(0.5)

    prota "Muchas Gracias, Sr. Thompson."

    # El protagonista se muestra muy interesado en el proyecto y hace varias preguntas sobre los detalles del mismo.

label el_fin:
    # Finaliza el juego:
    scene bg negro
    presentador_capitulos "FINAL #1\nNada en especial"

    

    return