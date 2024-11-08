# Eliza en Python
Chatbot elemental tipo Eliza, con Capacidad de soporte Multilenguaje.
## Lenguajes Implementados
- Espa&ntilde;ol - esEC.py
- Ingl&eacute;s - enUS.py
## Uso
- Importar la librer&iacute;a `eliza` y una de las librer&iacute;as de idiomas (`esEC` o `enUS`).
- Inicializar un objeto `eliza.eliza` especificando una de las librer&iacute;as de idioma.
- Invocar el método `respond()` especificando el texto de entrada.
Ejemplo:
```
import eliza, esEC

mi_eliza = eliza.eliza(esEC)
pregunta = input()
respuesta = mi_eliza.respond(pregunta)
print(respuesta)
``` 