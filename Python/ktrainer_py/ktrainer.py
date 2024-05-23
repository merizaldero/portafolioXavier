import xpd_orm as orm
from os.path import join, dirname, abspath
import random

from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH


PATH_BDD = join(dirname(abspath( __file__ )), "data","kanji.db")

# Definicion de  Entidades

Kanjis = orm.Entidad()
Kanjis.setMetamodelo({ 
    "nombreTabla":"XKT_KANJI",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDSTRING, "tamano":8, "pk":True },
        { "nombre":"kanji", "nombreCampo":"KANJI", "tipo":orm.XPDSTRING, "tamano":8, },
        { "nombre":"significado", "nombreCampo":"SIGNIFICADO", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"pronunciacion", "nombreCampo":"PRONUNCIACION", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"grado", "nombreCampo":"GRADO", "tipo":orm.XPDSTRING, "tamano":32, },
        { "nombre":"orden_grado", "nombreCampo":"ORDEN_GRADO", "tipo":orm.XPDINTEGER, },
        { "nombre":"numero_trazos", "nombreCampo":"NUMERO_TRAZOS", "tipo":orm.XPDINTEGER, },
        { "nombre":"es_kyujitai", "nombreCampo":"ES_KYUJITAI", "tipo":orm.XPDINTEGER, },
        ],
    "namedQueries":[
        { "nombre":"findall", "orderBy":["grado","orden_grado"] },
        { "nombre":"findByEskyujitai", "whereClause":["es_kyujitai"], "orderByClause":["grado","orden_grado",] },
        ]
    })

Recetas = orm.Entidad()
Recetas.setMetamodelo({
    "nombreTabla":"XKT_RECETA",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True },
        { "nombre":"id_kanji", "nombreCampo":"ID_KANJI", "tipo":orm.XPDSTRING, "tamano":8, },
        ],
    "namedQueries":[
        { "nombre":"findall", "whereClause":["activo",] , "orderBy":["username",] },
        { "nombre":"findById", "whereClause":["id",] },
        ]
    })

IngredientesReceta = orm.Entidad()
IngredientesReceta.setMetamodelo({
    "nombreTabla":"XKT_INGREDIENTE_RECETA",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True },
        { "nombre":"id_receta", "nombreCampo":"ID_RECETA", "tipo":orm.XPDINTEGER },
        { "nombre":"id_kanji", "nombreCampo":"ID_KANJI", "tipo":orm.XPDSTRING, "tamano":8, },
        { "nombre":"orden", "nombreCampo":"ORDEN", "tipo":orm.XPDINTEGER },
        ],
    "namedQueries":[
        { "nombre":"findall", "whereClause":["activo",] , "orderBy":["username",] },
        { "nombre":"findById", "whereClause":["id",] },
        ]
    })

def char2hexa(texto):
    """
    Función que obtiene la representación Unicode hexadecimal del primer caracter de un texto.

    Argumentos:
    texto: El texto del cual se desea obtener el primer caracter.

    Retorno:
    La representación Unicode hexadecimal del primer caracter del texto, o 'None' si el texto está vacío.
    """
    if not texto:
        return None

    primer_caracter = texto[0]
    punto_de_codigo = ord(primer_caracter)
    representacion_hexadecimal = hex(punto_de_codigo)[2:].upper()

    while len(representacion_hexadecimal) < 4:
        representacion_hexadecimal = '0' + representacion_hexadecimal

    return representacion_hexadecimal

def servir_main():
    redirect ("/static/index.html")

def servir_grados():
    sql="""select a.GRADO grado from XKT_KANJI a group by a.GRADO order by 1"""
    con = orm.Conexion(PATH_BDD)
    resultado = con.consultar(sql,{},['grado'])
    con.close()
    return {'lista':resultado}
    
def servir_consulta():
    grado = request.forms.get('grado','S')
    es_kyujitai = int(request.forms.get('es_kyujitai','0'))
    muestra = int(request.forms.get('muestra','5'))
    con = orm.Conexion(PATH_BDD)
    sql="""select a.ID id, a.KANJI kanji, a.SIGNIFICADO significado, a.PRONUNCIACION pronunciacion, a.GRADO grado, a.ORDEN_GRADO orden_grado, a.NUMERO_TRAZOS numero_trazos, a.ES_KYUJITAI es_kyujitai
    from XKT_KANJI a 
    where a.ES_KYUJITAI = :es_kyujitai and a.GRADO <= :grado order by a.GRADO, a.ORDEN_GRADO """
    resultado = con.consultar(sql,{'es_kyujitai':es_kyujitai, 'grado':grado },['id', 'kanji', 'significado', 'pronunciacion', 'grado', 'orden_grado', 'numero_trazos', 'es_kyujitai']) 
    con.close()
    return { 'lista':random.sample(resultado, muestra) }

def rutearModulo( app : Bottle, ruta_base : str ):
    # encapsula Session Middleware

    app.route( ruta_base + '/' , method = ['GET'])(servir_main)
    app.route( ruta_base + '/consulta' , method = ['POST'])(servir_consulta)
    app.route( ruta_base + '/grados' , method = ['GET'])(servir_grados)