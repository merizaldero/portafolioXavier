# XPD Asistente
Esta aplicación muestra en pantalla dos avatares de apariencia customizable.
## Ambiente
- Python para PC o servidor
- QPython para Android (incluye interface con __qpy__ para habilitar __Text 2 Speech__)
## Pantallas.
### Avatar Miku. 
![Asistente Basada en demo de Three.JS](img/miku1.png)
- Es direccionado desde el root de la app. 
- Es una ensayo basado en el demo [loader / mmd / pose](https://threejs.org/examples/#webgl_loader_mmd_pose) de la librer&iacute;a [Three.JS](https://threejs.org/). 
- Este ensayo ha sustituido la GUI basada en el addon de Three.JS por una GUI basada en Bootstrap 5. 
- La aparienciencia del Avatar es cargada desde modelos MMD (archivo .pmd para el avatar y archivos .vpd para las poses).
- Incluye interface a Pseudo Chatbot basado en Eliza, implementado en [eliza](../eliza/README.md).
- Soporta:
  - 9 Poses.
  - Más de 70 Variaciones Faciales.
### Avatar "La Otra Miku": Avatar Personalizable
![Asistente Customizable](img/miku2.png)
- La aparienciencia del Avatar es cargada desde modelos FBX, tanto para el avatar, como para las poses.
- Controles basados en bootstrap 5.
- Incluye interface a Pseudo Chatbot basado en Eliza.
- Soporta: 
  - 10 Poses.
  - Más de 70 Variaciones Faciales.
  - Más de 20 "Accesorios" entre Peinados y Atuendos
## Controles de Avatar.
### Interface ChatBot
![Barra de Chatbot](img/barra_chatbot.png)

Por defecto, el Chatbot se encuentra en modo "Loro", es decir, repite lo que el usuario escribe en la barra de texto cuando se presiona el botón ">".
Para habilitar el Modo Conversaci&oacute;n (Pseudo Eliza), puede plegar las acciones presionando el botón &equiv; y habilitando la opción "Modo Conversaci&oacute;n".
![Barra de Chatbot](img/barra_chatbot_1.png)
> [!NOTE]
> Cuando es ejecutado desde QPython, se habilita un endpoint que es invocado desde la p&aacute;gina para usar el mecanismo __Text to Speech__ nativo de Android. Esta caracer&iacute;stica puede ser desabilitada en QPython con la opci&oacute;n "Habilitar Locuci&oacute;n"
### Cambio de Pose
Es posible cambiar la pose del Avatar. El procedimiento es el siguiente:
1. Desplegar las opciones hacia abajo con el bot&oacute;n &equiv; .
2. ( Opcional ) Habilitar o deshabilitar si la pose va a revertirse en 5 segundos o si va a permanecer hasta el siguiente cambio de pose.
3. Elegir una de las poses de las opciones.
![Barra de Chatbot](img/poses.png)
### Variaciones Faciales
Cada modelo de Avatar incluye informaci&oacute;n para aplicar variaciones faciales.
Dichas variaciones son habilitadas desplegando la sección &equiv;Variaciones Faciales&equiv;. Cada Variaci&oacute;n facial es desplegada como una barra de desplizamiento aplicando valores entre 0.0 y 1.0.
![Barra de Chatbot](img/faciales.png)
Adicionalmente, el procesamiento de las respuestas del chatbot, ya sea en Modo Repetici&oacute;n o Modo Conversaci&oacute;n, refleja combinaciones de variaciones faciales para ciertos patrones, logrando as que el avatar var&iacute;e su expresi&oacute;n para "hablar" o mostrar emociones. El &uacute;ltimo patr&oacute;n detectado queda aplicado en el rostro del avatar.
![Barra de Chatbot](img/faciales_chat.png)