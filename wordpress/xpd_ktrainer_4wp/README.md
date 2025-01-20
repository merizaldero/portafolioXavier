# XPD Kanji Trainer para Wordpress
Funcionalidad de XPD Kanji Trainer implementado como Plugin para Wordpress.

Kanji Trainer tiene como prop&oacute;sito permitir el aprendizaje de idiomas mediante ejercicios de vocabulario de car&aacute;cter l&uacute;dico.

La funcionalidad original del presente plugin fue implementada originalmente en [Python](../../Python/ktrainer_py/).

Esta funcionalidad cambia el concepto agrupando los Kanjis en Niveles, y los Niveles son agrupados por Cursos, de forma que se puede soportar varias temáticas de traducción.

Incluye las siguientes GUIs Administrativas:

- Listar Cursos.
- Crear / Editar Curso.
- Listar Niveles por curso.
- Crear / Editar Nivel.
- Listar T&eacute;rminos (Kanjis) por Nivel.
- Importar T&eacute;rminos por nivel desde archivo CSV.
- Crear Editar T&eacute;rmino.

Se registra las siguientes p&aacute;ginas p&uacute;blicas:

- _/xkt-cursos/_: Despliega el listado de Cursos registrados y los enlaces para el despliegue de cada uno.
- _/xkt-curso/_: Despliega los niveles del curso, y realiza la actividad de aprendizaje l&uacute;dica.

Se habilita la siguiente el siguiente endpoint para recuperar informaci&oacute;m:

- _/wp-json/xkt-api/v1/kanjis/_: retorna una muestra de _n_ t&eacute;rminos correspondiente a uno o m&aacute;s niveles correspondientes a un curso. 