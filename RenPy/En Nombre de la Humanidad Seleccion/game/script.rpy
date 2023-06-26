# Coloca el código de tu juego en este archivo.

define minimo_hito1_entrevista = 3
define minimo_hito2_entrevista = 7
define minimo_hito3_entrevista = 10
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

    hide prota
    sr_thompson "Hemos revisado su hoja de vida y nos interesaría continuar nuestro proceso de selección con Ud. Deseo hacerle algunas preguntas, si no tiene inconveniente."

    hide mr
    show prota terno at cuarto_3
    prota "Encantado, Sr. Thompson."

    # Aqui empieza la entrevista. en esta variable se registra el puntaje
    define puntaje_entrevista = 0
    define siguiente_pregunta = ""
    define feedbacks_entrevista = []

label entrevista_pregunta_1:
    $ puntaje_entrevista = 0
    $ siguiente_pregunta = "entrevista_pregunta_2"
    hide prota
    hide mr    
    menu:
        "Para comenzar, quisiera que nos cuente sus motivaciones para aplicar para este puesto."
        "Simplemente necesito un trabajo y este puesto se ajusta a mi perfil":
            $ feedbacks_entrevista.append("Necesita demostrar que sus motivaciones van más allá de conseguir un empleo. ")
            jump entrevista_pregunta_fail
        "Me motiva la oportunidad de aplicar mis habilidades y conocimientos en un entorno desafiante como el que ofrece este puesto. Además, estoy entusiasmado por la posibilidad de contribuir al crecimiento y éxito de la empresa":
            jump entrevista_pregunta_ok
        "La paga y los beneficios parecen buenos, así que por eso aplico a este puesto":
            $ feedbacks_entrevista.append("Necesita demostrar que sus motivaciones van más allá de la oferta salarial. Se percibe falta de mística en sus respuestas.")
            jump entrevista_pregunta_fail
        "Mi motivación radica en la pasión que tengo por esta industria y el deseo de seguir aprendiendo y creciendo profesionalmente. Este puesto me brinda la oportunidad de expandir mis horizontes y enfrentar nuevos desafíos":
            jump entrevista_pregunta_ok

label entrevista_pregunta_ok:
    $ puntaje_entrevista += 1
    jump expression siguiente_pregunta
label entrevista_pregunta_fail:
    jump expression siguiente_pregunta

label entrevista_pregunta_2:
    $ siguiente_pregunta = "entrevista_pregunta_3"
    menu:
        "Cuales son tus fortalezas?"
        "Soy muy responsable y comprometido con mi trabajo, siempre cumplo con mis responsabilidades y metas.":
            jump entrevista_pregunta_ok
        "No tengo mucha experiencia en este campo, así que no sé cuáles son mis fortalezas.":
            $ feedbacks_entrevista.append("Necesita poner más atención en los requisitos de la oferta laboral, y tener claro que sus fortalezas se alinean al requerimiento de la oferta laboral.")
            jump entrevista_pregunta_fail
        "Tengo una gran capacidad para trabajar en equipo y colaborar con otros para alcanzar objetivos comunes.":
            jump entrevista_pregunta_ok
        "Soy muy perfeccionista y a veces esto me impide avanzar rápidamente en el trabajo.":
            $ feedbacks_entrevista.append("A veces el perfeccionismo es el camino a la procastinación y se puede convertir en un obstáculo para alcanzar sus objetivos.")
            jump entrevista_pregunta_fail

label entrevista_pregunta_3:
    $ siguiente_pregunta = "entrevista_pregunta_4"
    menu:
        "Cuales son tus debilidades?"
        "No puedo pensar en ninguna debilidad en particular, soy bastante perfecto en lo que hago.":
            $ feedbacks_entrevista.append("El hecho que no vea debilidades en Ud, puede ser señal que no quiere reconocer debilidades o que las está ocultando.")
            jump entrevista_pregunta_fail
        "En ocasiones, me obsesiono un poco con los detalles, lo que puede ralentizar mi ritmo de trabajo.":
            jump entrevista_pregunta_ok
        "Aunque tengo habilidades técnicas sólidas, a veces me gustaría tener más experiencia en ciertas áreas específicas.":
            jump entrevista_pregunta_ok
        "A veces tengo dificultad para tomar decisiones rápidas y me gusta pensar en todas las posibilidades antes de actuar.":
            $ feedbacks_entrevista.append("Es razonable procurar tener toda la información posible para tomar una decisión, pero incluso eso puede detenerlo en alcanzar sus objetivos.\nDebe aceptar un criterio mínimo para seguir adelante con una decisión.")
            jump entrevista_pregunta_fail

label entrevista_pregunta_4:
    $ siguiente_pregunta = "entrevista_hito_1"
    menu:
        "Por qué te gustaría trabajar en nuestra empresa?"
        "No he investigado mucho sobre su empresa, pero estoy dispuesto a trabajar aquí si me ofrecen un buen salario.":
            $ feedbacks_entrevista.append("Antes de aplicar para un cargo en una empresa, es importante investigar la cultura de la empresa y la naturaleza del cargo. Se observa falta de motivación de su parte.")
            jump entrevista_pregunta_fail
        "Admiro los valores y la cultura de su empresa, y me gustaría formar parte de un equipo que comparte esos mismos principios.":
            jump entrevista_pregunta_ok
        "No tengo una razón específica para querer trabajar en su empresa, solo necesito un trabajo.":
            $ feedbacks_entrevista.append("Si bien el problema económico es importante, siempre es necesario demostrar motivación con respecto al trabajo que se está aplicando.")
            jump entrevista_pregunta_fail
        "Me gustaría trabajar en una empresa que valora el equilibrio entre el trabajo y la vida personal y ofrece programas de bienestar para sus empleados.":
            jump entrevista_pregunta_ok        

label entrevista_hito_1:
    show mr thompson at cuarto_1
    # TODO Dar retroalimentación de las preguntas no tan bien contestadas
    if puntaje_entrevista < minimo_hito1_entrevista:
        jump fin_entrevista    
    sr_thompson "Bueno, Sr. {b}[nombre_prota]{/b},\ncontinuemos con la entrevista."
    hide mr
    $ feedbacks_entrevista = []
label entrevista_pregunta_5:
    $ siguiente_pregunta = "entrevista_pregunta_6"
    menu:
        "Cuéntame más sobre su experiencia laboral en relación con este puesto."
        "He recibido retroalimentación positiva de mis supervisores y colegas sobre mi actitud, ética de trabajo y habilidades profesionales.":
            jump entrevista_pregunta_ok
        "No tengo experiencia directa en este campo, pero estoy dispuesto a aprender sobre la marcha.":
            $ feedbacks_entrevista.append("Su actitud por aprender es buena, pero su aprendizaje será visto por la compañía más como un gasto que como una inversión.")
            jump entrevista_pregunta_fail
        "Durante mi pasantía, he adquirido conocimientos y experiencia específica en esta industria, lo que me permite entender los desafíos y las oportunidades relacionadas con este puesto.":
            jump entrevista_pregunta_ok
        "Mi rendimiento se vio afectado negativamente debido a conflictos interpersonales en el lugar de trabajo.":
            $ feedbacks_entrevista.append("Tenga en cuenta que las forma de manejar las relaciones interpersonales son parte de su imagen profesional.")
            jump entrevista_pregunta_fail

label entrevista_pregunta_6:
    $ siguiente_pregunta = "entrevista_pregunta_7"
    menu:
        "Cuáles son sus principales logros profesionales?"
        "No he tenido la oportunidad de desarrollar o implementar nuevas iniciativas.":
            $ feedbacks_entrevista.append("Su actitud por aprender es buena, pero su aprendizaje será visto por la compañía más como un gasto que como una inversión.")
            jump entrevista_pregunta_fail
        "No he tenido la oportunidad de desarrollar o implementar nuevas iniciativas.":
            $ feedbacks_entrevista.append("Tenga en cuenta que las forma de manejar las relaciones interpersonales son parte de su imagen profesional.")
            jump entrevista_pregunta_fail
        "Fui reconocido por mi capacidad para liderar y motivar equipos, lo que resultó en una mejora significativa en los indicadores de desempeño del equipo.":
            jump entrevista_pregunta_ok
        "Lideré la implementación de un sistema de gestión de calidad que obtuvo la certificación ISO 9001.":
            jump entrevista_pregunta_ok

label entrevista_pregunta_7:
    $ siguiente_pregunta = "entrevista_pregunta_8"
    menu:
        "Cómo maneja situaciones de presión y plazos ajustados?"
        "Me enfoco en establecer metas realistas y descomponer proyectos en tareas manejables para cumplir con los plazos.":
            jump entrevista_pregunta_ok
        "Utilizo técnicas de manejo del estrés, como la respiración profunda o la práctica de mindfulness, para mantener un estado mental tranquilo y centrado.":
            jump entrevista_pregunta_ok
        "Me cuesta adaptarme a las expectativas cambiantes o a las demandas de último momento, lo que puede generar estrés y errores.":
            $ feedbacks_entrevista.append("Necesita implementar técnicas para manejar el estrés y de organizar tareas cuando se requiera adaptación ante requerimientos cambiantes.")
            jump entrevista_pregunta_fail
        "No tengo experiencia en el manejo de proyectos complejos con múltiples plazos y tareas interdependientes.":
            $ feedbacks_entrevista.append("Necesita implementar técnicas para manejar el estrés y de organizar tareas cuando se requiera adaptación ante requerimientos cambiantes.")
            jump entrevista_pregunta_fail

label entrevista_pregunta_8:
    $ siguiente_pregunta = "entrevista_pregunta_9"
    menu:
        "Cuál es tu enfoque para resolver problemas complejos?"
        "Priorizo los problemas según su impacto y urgencia, dedicando más recursos y tiempo a los más críticos.":            
            jump entrevista_pregunta_ok
        "Utilizo un enfoque analítico y lógico para descomponer problemas complejos en componentes más manejables.":
            jump entrevista_pregunta_ok
        "Tiendo a abordar problemas complejos de manera superficial sin profundizar en las causas subyacentes.":
            $ feedbacks_entrevista.append("Necesita implementar técnicas para manejar el estrés y de organizar tareas cuando se requiera adaptación ante requerimientos cambiantes.")
            jump entrevista_pregunta_fail
        "Me distraigo fácilmente y pierdo el enfoque en la resolución de problemas complejos.":
            $ feedbacks_entrevista.append("Necesita implementar técnicas para manejar el estrés y de organizar tareas cuando se requiera adaptación ante requerimientos cambiantes.")
            jump entrevista_pregunta_fail

label entrevista_pregunta_9:
    $ siguiente_pregunta = "entrevista_hito_2"
    menu:
        "Cuál es tu enfoque para resolver problemas complejos?"
        "No tengo experiencia en el manejo de proyectos complejos con múltiples plazos y tareas interdependientes.":
            $ feedbacks_entrevista.append("Necesita implementar técnicas para manejar el estrés y de organizar tareas cuando se requiera adaptación ante requerimientos cambiantes.")
            jump entrevista_pregunta_fail
        "Me enfoco en establecer metas realistas y descomponer proyectos en tareas manejables para cumplir con los plazos.":
            jump entrevista_pregunta_ok
        "Me cuesta adaptarme a las expectativas cambiantes o a las demandas de último momento, lo que puede generar estrés y errores.":
            $ feedbacks_entrevista.append("Necesita implementar técnicas para manejar el estrés y de organizar tareas cuando se requiera adaptación ante requerimientos cambiantes.")
            jump entrevista_pregunta_fail
        "Utilizo técnicas de manejo del estrés, como la respiración profunda o la práctica de mindfulness, para mantener un estado mental tranquilo y centrado.":
            jump entrevista_pregunta_ok

label entrevista_hito_2:
    show mr thompson at cuarto_1
    # TODO Dar retroalimentación de las preguntas no tan bien contestadas
    if puntaje_entrevista < minimo_hito2_entrevista:
        jump fin_entrevista    
    sr_thompson "Bueno, Sr. {b}[nombre_prota]{/b},\ncontinuemos con la entrevista."
    $ feedbacks_entrevista = []
    hide mr
# El protagonista se muestra muy interesado en el proyecto y hace varias preguntas sobre los detalles del mismo.

label fin_entrevista:
    show mr thompson at cuarto_1
    show prota terno at cuarto_3
    
    sr_thompson "Bueno, Sr. {b}[nombre_prota]{/b},\nCreo que con esto finalizamos esta entrevista. Estaremos contactándolo una vez hayamos tomado una Decisión.\nAgradecemos su tiempo."
    prota "Muchas Gracias, Sr. Thompson.\nEstaré al pendiente.\nUna buena tarde."

    if puntaje_entrevista < minimo_hito3_entrevista:
        jump final_1

    jump final_5

label final_1:
    # Finaliza el juego:
    scene bg negro
    presentador_capitulos "FINAL #1\nFINAL SALADO\nFuiste una de los muertos durante el Apocalipsis del Planeta Tierra\ny no llegaste a imaginar que pudieras haber sobrevivido si hubieras logrado ese trabajo en Sterling Dynamics."
    return

label final_5:
    # Finaliza el juego:
    scene bg negro
    presentador_capitulos "FINAL #5\nFINAL FELIZ\nLo has Logrado!!"
    return
