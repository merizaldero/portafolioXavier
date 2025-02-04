# Coloca el código de tu juego en este archivo.

# Declara los personajes usados en el juego como en el ejemplo:

init python:
    #----------------------------------------------------------------------
    # eliza.py
    #
    # a cheezy little Eliza knock-off by Joe Strout
    # with some updates by Jeff Epler
    # hacked into a module and updated by Jez Higgins
    #----------------------------------------------------------------------

    import random
    import datetime

    acumulador = 0
    operadores = ['+', '-', 'x']
    numero_terminos = 0
    indice_operador = 0
    resultado_esperado = 0
    operador = ''
    resultado_ingresado = ''
    termino_anterior = 0
    valor_termino = 0
    hora_inicio = None
    hora_fin = None

define e = Character("Eileen")


# El juego comienza aquí.

label start:

    # Muestra una imagen de fondo: Aquí se usa un marcador de posición por
    # defecto. Es posible añadir un archivo en el directorio 'images' con el
    # nombre "bg room.png" or "bg room.jpg" para que se muestre aquí.

    scene bg room:
        size(1280, 720)
    play music "musica_fondo.ogg"
    
    # Muestra un personaje: Se usa un marcador de posición. Es posible
    # reemplazarlo añadiendo un archivo llamado "eileen happy.png" al directorio
    # 'images'.

    show eileen happy:
        zoom 0.75
        xpos 0.10
        ypos 0.15

    # Presenta las líneas del diálogo.

    e "Hola, Soy Eileen."

    e "En esta sesión vamos a entrenar tu agilidad de cálculo mental"

    label preguntar_terminos:

        show eileen responde

        e "Indícame por favor con cuantos términos vas a entrenar"

        $ numero_terminos = 0

        menu:

            "3":
                $ numero_terminos = 3
                jump inicia_prueba

            "5":
                $ numero_terminos = 5
                jump inicia_prueba
            "7":
                $ numero_terminos = 7
                jump inicia_prueba
            "9":
                $ numero_terminos = 9
                jump inicia_prueba

    label inicia_prueba:

        python:
            acumulador = random.randint(1,9)
            valor_termino = 0
            termino_anterior = 0

        show eileen happy

        e "Excelente, entonces vamos a trabajar con [numero_terminos] términos!" 
        e "Comencemos con el número [acumulador]"

        python:
            hora_inicio = datetime.datetime.now()

    label siguiente_termino:

        if numero_terminos == 0:
            jump prueba_finalizada

        python:            
            while valor_termino == termino_anterior:            
                valor_termino = random.randint(1,9)
            indice_operador = random.randint(0, len(operadores)-1)
            operador = operadores[indice_operador]
            if acumulador == 0 and operador != '+':                
                operador = '+'
            if operador == '+':
                resultado_esperado = acumulador + valor_termino
            elif operador == 'x':
                resultado_esperado = acumulador * valor_termino
            elif operador == '-':
                while valor_termino > acumulador:
                    valor_termino = random.randint(1,9)
                resultado_esperado = acumulador - valor_termino
            
    label pedir_respuesta:

        show eileen escucha

        python:
            resultado_ingresado = renpy.input("{0} {1} {2}".format(acumulador, operador, valor_termino))
            resultado_ingresado = resultado_ingresado.strip() or ""
        
        if str(resultado_esperado) == resultado_ingresado:
            show eileen happy
            e "Correcto !!"
            python:
                acumulador = resultado_esperado
                termino_anterior = valor_termino
                numero_terminos -= 1
            jump siguiente_termino
        else:
            show eileen brazos_cruzados
            e "Lo siento, no es la respuesta correcta.\nInténtalo de nuevo."
            jump pedir_respuesta

    label prueba_finalizada:

        python:
            hora_fin = datetime.datetime.now() - hora_inicio
            tiempo_segundos = hora_fin.total_seconds()

        e "Felicitaciones!! has terminado esta prueba en [tiempo_segundos] segundos !"

        e "Quieres jugar otra vez?"

        menu:
            "SI":
                jump preguntar_terminos
            "NO":
                jump fin_juego                

    label fin_juego:
        
        # Finaliza el juego:
        e "Oh! es una pena, con lo que quería seguir jugando contigo."
        e "Me ha alegrado mucho jugar."
        e "Hasta la próxima!!"

    return
