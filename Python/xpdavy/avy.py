import xpd_orm as orm
from os.path import abspath , dirname, exists
from bs4 import BeautifulSoup
from random import choice
import numpy as np

PATH_BDD = dirname(abspath(__file__)) + "/data/base.db"
PATH_INIT = dirname(abspath(__file__)) + "/data/init.sql"
PATH_IMPORT = dirname(abspath(__file__)) + "/art/fabrica.svg"

Partes = orm.Entidad()
Partes.setMetamodelo({
    "nombreTabla":"PARTE",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            },
        {
            "nombre":"nombre",
            "nombreCampo":"NOMBRE",
            "tipo":orm.XPDSTRING,
            "tamano":32,
            },
        {
            "nombre":"orden_z",
            "nombreCampo":"ORDEN_Z",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"orden_gui",
            "nombreCampo":"ORDEN_GUI",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"id_parent",
            "nombreCampo":"ID_PARENT",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"offset_x_min",
            "nombreCampo":"OFFSET_X_MIN",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"offset_x_max",
            "nombreCampo":"OFFSET_X_MAX",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"offset_x_steps",
            "nombreCampo":"OFFSET_X_STEPS",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"offset_y_min",
            "nombreCampo":"OFFSET_Y_MIN",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"offset_y_max",
            "nombreCampo":"OFFSET_Y_MAX",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"offset_y_steps",
            "nombreCampo":"OFFSET_Y_STEPS",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"scale_min",
            "nombreCampo":"SCALE_MIN",
            "tipo":orm.XPDREAL,
            "tamano": 5,
            "precision": 3,
            },
        {
            "nombre":"scale_max",
            "nombreCampo":"SCALE_MAX",
            "tipo":orm.XPDREAL,
            "tamano": 5,
            "precision": 3,
            },
        {
            "nombre":"scale_steps",
            "nombreCampo":"SCALE_STEPS",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"simetrico_x",
            "nombreCampo":"SIMETRICO_X",
            "tipo":orm.XPDSTRING,
            "tamano":1,
            },
        {
            "nombre":"opcional",
            "nombreCampo":"OPCIONAL",
            "tipo":orm.XPDSTRING,
            "tamano":1,
            },
        {
            "nombre":"tiene_color",
            "nombreCampo":"TIENE_COLOR",
            "tipo":orm.XPDSTRING,
            "tamano":1,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findall",
            "orderBy":["orden_z",]
            },
        {
            "nombre":"findById",
            "whereClause":["id",]
            }
        ]
    })

Generos = orm.Entidad()
Generos.setMetamodelo({
    "nombreTabla":"GENERO",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            },
        {
            "nombre":"nombre",
            "nombreCampo":"NOMBRE",
            "tipo":orm.XPDSTRING,
            "tamano":32,
            },
        {
            "nombre":"simbolo",
            "nombreCampo":"SIMBOLO",
            "tipo":orm.XPDSTRING,
            "tamano":8,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findall",
            "orderBy":["id",]
            },
        {
            "nombre":"findById",
            "whereClause":["id",]
            }
        ]
    })

Prendas = orm.Entidad()
Prendas.setMetamodelo({
    "nombreTabla":"PRENDA",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            "incremental":True,
            },
        {
            "nombre":"nombre",
            "nombreCampo":"NOMBRE",
            "tipo":orm.XPDSTRING,
            "tamano":32,
            },
        {
            "nombre":"id_parte",
            "nombreCampo":"ID_PARTE",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"orden",
            "nombreCampo":"ORDEN",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"svg",
            "nombreCampo":"SVG",
            "tipo":orm.XPDSTRING,
            "tamano":1024,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findByParte",
            "whereClause":["id_parte",],
            "orderBy":["orden",]
            },
        {
            "nombre":"findById",
            "whereClause":["id",]
            }
        ]
    })

PrendasGenero = orm.Entidad()
PrendasGenero.setMetamodelo({
    "nombreTabla":"PRENDA_GENERO",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            "incremental":True,
            },
        {
            "nombre":"id_prenda",
            "nombreCampo":"ID_PRENDA",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"id_genero",
            "nombreCampo":"ID_GENERO",
            "tipo":orm.XPDINTEGER,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findByGenero",
            "whereClause":["id_genero",],
            "orderBy":["id_prenda",]
            },
        {
            "nombre":"findByPrenda",
            "whereClause":["id_prenda",],
            "orderBy":["id_genero",]
            },
        {
            "nombre":"findById",
            "whereClause":["id",]
            }
        ]
    })

Usuarios = orm.Entidad()
Usuarios.setMetamodelo({
    "nombreTabla":"USUARIO",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            "incremental":True,
            },
        {
            "nombre":"nombre",
            "nombreCampo":"NOMBRE",
            "tipo":orm.XPDSTRING,
            "tamano":32,
            },
        {
            "nombre":"clave",
            "nombreCampo":"CLAVE",
            "tipo":orm.XPDSTRING,
            "tamano":32,
            },
        {
            "nombre":"es_admin",
            "nombreCampo":"ES_ADMIN",
            "tipo":orm.XPDSTRING,
            "tamano":1,
            },
        {
            "nombre":"activo",
            "nombreCampo":"ACTIVO",
            "tipo":orm.XPDSTRING,
            "tamano":1,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findall",
            "whereClause":["activo","es_admin"],
            "orderBy":["nombre",]
            },
        {
            "nombre":"findByNombre",
            "whereClause":["nombre",],
            },
        {
            "nombre":"findById",
            "whereClause":["id",]
            },
        {
            "nombre":"findLogin",
            "whereClause":["nombre","clave"]
            },
        ]
    })

Avatares = orm.Entidad()
Avatares.setMetamodelo({
    "nombreTabla":"AVATAR",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            "incremental":True,
            },
        {
            "nombre":"id_usuario",
            "nombreCampo":"ID_USUARIO",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"id_genero",
            "nombreCampo":"ID_GENERO",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"nombre",
            "nombreCampo":"NOMBRE",
            "tipo":orm.XPDSTRING,
            "tamano":32,
            },
        {
            "nombre":"color_piel",
            "nombreCampo":"COLOR_PIEL",
            "tipo":orm.XPDSTRING,
            "tamano":6,
            },
        {
            "nombre":"activo",
            "nombreCampo":"ACTIVO",
            "tipo":orm.XPDSTRING,
            "tamano":1,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findByUsuario",
            "whereClause":["id_usuario","activo"],
            "orderBy":["nombre",]
            },
        {
            "nombre":"findById",
            "whereClause":["id",]
            }
        ]
    })

PrendasAvatar = orm.Entidad()
PrendasAvatar.setMetamodelo({
    "nombreTabla":"PRENDA_AVATAR",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            "incremental":True,
            },
        {
            "nombre":"id_avatar",
            "nombreCampo":"ID_AVATAR",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"id_parte",
            "nombreCampo":"ID_PARTE",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"id_prenda",
            "nombreCampo":"ID_PRENDA",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"offset_x",
            "nombreCampo":"OFFSET_X",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"offset_y",
            "nombreCampo":"OFFSET_Y",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"escala",
            "nombreCampo":"ESCALA",
            "tipo":orm.XPDREAL,
            "tamano":3,
            "precision":2,
            },
        {
            "nombre":"color",
            "nombreCampo":"COLOR",
            "tipo":orm.XPDSTRING,
            "tamano":7,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findByAvatar",
            "whereClause":["id_avatar",],
            "orderBy":["id",]
            },
        {
            "nombre":"findById",
            "whereClause":["id",]
            }
        ]
    })
ColoresParte = orm.Entidad()
ColoresParte.setMetamodelo({
    "nombreTabla":"COLOR_PARTE",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            "incremental":True,
            },
        {
            "nombre":"id_parte",
            "nombreCampo":"ID_PARTE",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"color",
            "nombreCampo":"COLOR",
            "tipo":orm.XPDSTRING,
            "tamano":7,
            },
        {
            "nombre":"orden",
            "nombreCampo":"ORDEN",
            "tipo":orm.XPDINTEGER,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findall",
            "whereClause":[],
            "orderBy":["id_parte","orden"]
            },
        {
            "nombre":"findByParte",
            "whereClause":["id_parte",],
            "orderBy":["orden",]
            },
        ]
    })
ColoresPiel = orm.Entidad()
ColoresPiel.setMetamodelo({
    "nombreTabla":"COLOR_PIEL",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            "incremental":True,
            },
        {
            "nombre":"color",
            "nombreCampo":"COLOR",
            "tipo":orm.XPDSTRING,
            "tamano":7,
            },
        {
            "nombre":"orden",
            "nombreCampo":"ORDEN",
            "tipo":orm.XPDINTEGER,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findall",
            "whereClause":[],
            "orderBy":["orden",]
            },
        ]
    })

def inicializar():
    entidades = [Partes, Generos, Prendas, PrendasGenero, Usuarios, Avatares, PrendasAvatar, ColoresPiel, ColoresParte]
    con = orm.Conexion(PATH_BDD)
    try:
        for entidad in entidades:
            entidad.crearTabla(con)
        if exists( PATH_INIT ):
            con.ejecutarFileScript( PATH_INIT )
        con.commit()
    except Exception as ex:
        con.rollback()
        print(ex)
        raise Exception(str(ex))
    finally:
        con.close()

def findPrendasByGenero(conexion, id_genero):
    sql = """
select
    b.ID as id_prenda, b.NOMBRE as nombre, b.ID_PARTE as id_parte, b.SVG as svg
from PRENDA b
where exists(
select 1 from PRENDA_GENERO c
where c.ID_PRENDA = b.ID
and c.ID_GENERO = :id_genero
)
order by b.ID_PARTE, b.ORDEN
"""
    prendas = conexion.consultar( sql, {"id_genero":id_genero}, ["id_prenda", "nombre", "id_parte", "svg"] )
    return prendas

def findPrendasByGeneroParte(conexion, id_genero,id_parte):
    sql = """
select
    b.ID as id_prenda, b.NOMBRE as nombre, b.ID_PARTE as id_parte, b.SVG as svg
from PRENDA b
where exists(
select 1 from PRENDA_GENERO c
where c.ID_PRENDA = b.ID
and c.ID_GENERO = :id_genero
)
and b.ID_PARTE = :id_parte
order by b.ID_PARTE, b.ORDEN
"""
    prendas = conexion.consultar( sql, { "id_genero":id_genero, "id_parte":id_parte }, ["id_prenda", "nombre", "id_parte", "svg"] )
    return prendas

def findAvataresByUsuario(conexion, id_usuario):
    sql = """
SELECT a.id as id, a.id_usuario as id_usuario, a.id_genero as id_genero, a.nombre as nombre, a.color_piel as color_piel, a.activo as activo 
, b.SIMBOLO as simbolo
FROM AVATAR a, GENERO b
WHERE b.ID = a.ID_GENERO and a.ID_USUARIO = :id_usuario and a.ACTIVO = :activo  ORDER BY a.NOMBRE
"""
    avatares = conexion.consultar( sql, { "id_usuario":id_usuario, "activo":'1' }, ["id", "id_usuario", "id_genero", "nombre", "color_piel", "activo", "simbolo"] )
    return avatares

def trxCrearAvatar(conexion, avatar_info ):
    """
    Crea avatar y sus prendas
    """
    # print('Inicia creacion de avatar')

    # Asigna valores por defecto a campos que no tengan informacion
    valores_defecto = {'nombre':'Sin Nombre', 'activo':'1'}
    for campo in valores_defecto.keys():
        if campo in avatar_info.keys() and avatar_info[campo] is not None:
            break
        avatar_info[campo] = valores_defecto[campo]
    
    # print('Asignados valores por defecto')

    prendas = generarPrendasByGenero(conexion, avatar_info['id_genero'], verbal = True)

    # print('Seleccion de partes completada\n{0}'.format(repr(prendas)))

    avatar_info['color_piel'] = prendas['color_piel']

    print('asignacion complementaria')

    # Transacciones de insercion
    Avatares.insertar(conexion, avatar_info)
    print('avatar insertado')
    for prenda in prendas['prendas']:
        # print("asignadno id_avatar" + str(prenda))
        prenda['id_avatar'] = avatar_info['id']
        # print("asignado id_avatar")
        # print("insertando {0}".format(repr(prenda)))
        PrendasAvatar.insertar(conexion, prenda)
    
    print('proceso de insercion completado')

    return avatar_info

def ajustar_coordenadas(prendasAvatar):
    pass

def findPrendasByAvatar(conexion, id_avatar ):
    sql = """
SELECT a.id as id, a.id_avatar as id_avatar, c.id as id_parte, a.id_prenda as id_prenda, 
coalesce(a.offset_x, 0) as offset_x, coalesce(a.offset_y, 0) as offset_y, coalesce(a.escala, 1.0) as escala, coalesce(a.color, ' ') as color,
b.nombre as nombre, b.svg as svg,
c.orden_gui as orden_gui, c.id_parent as id_parent, c.simetrico_x as simetrico_x, c.opcional as opcional, c.tiene_color as tiene_color
FROM PARTE c
left join PRENDA_AVATAR a on c.ID = a.ID_PARTE and a.ID_AVATAR = :id_avatar  
left join PRENDA b on b.ID = a.ID_PRENDA   
ORDER BY c.ORDEN_GUI
    """
    prendas = conexion.consultar( sql, { "id_avatar":id_avatar }, ["id", "id_avatar", "id_parte", "id_prenda", "offset_x", "offset_y", "escala", "color", "nombre", "svg", "orden_gui", "id_parent", "simetrico_x", "opcional", "tiene_color"] )
    return prendas

def lista_rango(minimo, maximo, steps):
    if maximo == minimo or steps <= 1:
        return [maximo]
    return list(np.arange( minimo + 0.0, maximo + 0.0, (maximo - minimo + 0.0) / steps ) )

def generarPrendasByGenero(conexion, id_genero, verbal = False):
    partes = Partes.getNamedQuery(conexion, 'findall',{})
    prendas = findPrendasByGenero(conexion, id_genero)
    colores_piel = ColoresPiel.getNamedQuery(conexion, 'findall',{})
    color_piel = choice(colores_piel)['color']
    colores_partes = ColoresParte.getNamedQuery(conexion, 'findall',{})
    # campos_prenda_avatar = [ "id", "id_avatar", "id_parte", "id_prenda", "offset_x", "offset_y", "escala", "color" ]
    for parte in partes:
        prendas_parte = [ prenda for prenda in prendas if prenda['id_parte'] == parte['id'] ]
        colores_parte = [ color['color'] for color in colores_partes if color['id_parte'] == parte['id'] ]
        if parte['opcional'] == '1' or len(prendas_parte) == 0:
            prendas_parte = [ { "id_prenda":None, "nombre":None, "id_parte":None, "svg":None } ] + prendas_parte
        prenda = choice(prendas_parte)
        parte["id_parte"] = parte["id"]
        parte["id_prenda"] = prenda["id_prenda"]
        parte["svg"] = prenda["svg"]
        parte["offset_x"] = choice( lista_rango( parte['offset_x_min'], parte['offset_x_max'], parte['offset_x_steps'] ))
        parte["offset_y"] = choice( lista_rango( parte['offset_y_min'], parte['offset_y_max'], parte['offset_y_steps'] ))
        parte["escala"] = choice( lista_rango( parte['scale_min'], parte['scale_max'], parte['scale_steps'] ))
        parte["color"] = choice(colores_parte) if len(colores_parte) > 0 else color_piel
        if verbal:
            print("{0} : {1}".format(parte['nombre'],parte['color'] ))
    return { 'id_genero': id_genero, 'color_piel': color_piel, 'prendas': partes}

def matriz_transformacion(translate, rotate, scale):
    """
    Convierte valores de traslación, rotación y escala en una matriz de transformación SVG.
    
    :param translate: Tupla con valores de traslación en X e Y.
    :param rotate: Valor de rotación en grados.
    :param scale: Tupla con valores de escala en X e Y.
    :return: Matriz de transformación SVG.
    """
    
    # Matriz de identidad
    matrix = np.identity(3)
    
    # Traslación
    translation_matrix = np.array([[1, 0, translate[0]], [0, 1, translate[1]], [0, 0, 1]])
    matrix = np.dot(matrix, translation_matrix)
    
    # Rotación
    if rotate != 0:
        rad = np.radians(rotate)
        cos = np.cos(rad)
        sin = np.sin(rad)
        rotation_matrix = np.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
        matrix = np.dot(matrix, rotation_matrix)
    
    # Escala
    scale_matrix = np.array([[scale[0], 0, 0], [0, scale[1], 0], [0, 0, 1]])
    matrix = np.dot(matrix, scale_matrix)
    
    return matrix

def ajustarTransformaciones(data):
    cola_prendas = [ prenda for prenda in data['prendas'] if prenda['id_parent'] is None ]
    while True:
        if len(cola_prendas) == 0:
            break
        parte = cola_prendas.pop(0)
        filtro_padres = [x for x in data['prendas'] if x['id_parte'] == parte['id_parent'] ]
        if len(filtro_padres) > 0:
            padre = filtro_padres[0]
            if parte['simetrico_x'] == '1':
                parte['offset_xr'] = padre['offset_x'] - parte['offset_x']
            else:
                parte['offset_xr'] = 0
            parte['offset_x'] += padre['offset_x']
            parte['offset_y'] += padre['offset_y']
        cola_prendas += [ prenda for prenda in data['prendas'] if prenda['id_parent'] == parte['id_parte'] ]
    return data['prendas']

def generarSvgAvatar(data):
    color_piel = data['color_piel']
    prendas = ajustarTransformaciones(data)
    resultado = """<svg xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" 
   width="200" height="200">
""" + "\n".join( [ aplicar_transformaciones(prenda['svg'], 'g_{1}_{0}'.format(prenda['id'], prenda['nombre']), prenda['offset_x'], prenda['offset_y'], prenda['escala'], prenda['color'], prenda['simetrico_x'], prenda['offset_xr'] if 'offset_xr' in prenda else 0 ) for prenda in prendas ] ) + """
</svg>"""
    return resultado

def findAvatarById(id):
    resultado = None
    con = orm.Conexion(PATH_BDD)
    lista = Avatares.getNamedQuery(con, "findById", {"id":id})
    if len(lista) == 1:
        resultado = lista[0]
        resultado["prendas"] = findPrendasByAvatar( con, id )
    con.close()
    return resultado

def transaccionar(llamado,objeto):
    con = orm.Conexion(PATH_BDD)
    try:
        llamado(con, objeto)
        con.commit()
    except Exception as ex:
        con.rollback()
        print(repr(ex))
        raise Exception( str(ex) )
    finally:
        con.close()
    return objeto

def aplicar_transformaciones(nodo_svg, id, offset_x, offset_y, escala, color, simetrico_x , offset_xr):
    if nodo_svg is None:
        return ''
    print('{0} {1}'.format(offset_x, offset_xr))
    resultado = nodo_svg.format( id = id, offset_x = offset_x, offset_y = offset_y , escala_x = escala, escala_y = escala , color = color )
    if simetrico_x == '1':
        #print("agrega simetrico")
        #resultado += """<svg:use height="100%" width="100%" x="0" y="0" xlink:href="#{id}" id="m{id}" transform="translate({offset_x} {offset_y}) scale({escala_x} {escala_y})" />""".format( id = id, offset_x = offset_xr, offset_y = offset_y , escala_x = -escala, escala_y = escala )
        resultado += nodo_svg.format( id = id, offset_x = offset_xr, offset_y = offset_y , escala_x = -escala, escala_y = escala, color = color ).replace('id="','id="m')
    return resultado

def importar_partes():
    if exists(PATH_IMPORT):
        con = orm.Conexion(PATH_BDD)
        generos = {'M':1, 'F':2, 'X':3 }
        partes_list = Partes.getNamedQuery(con, 'findall', {})
        partes = { parte['nombre'] : parte['id'] for parte in partes_list }
        sopa = None
        with open(PATH_IMPORT, 'rt') as archivo:
            sopa = BeautifulSoup(archivo , 'xml')
        sqlFindPrenda = """
select a.ID as id, a.NOMBRE as nombre, a.ID_PARTE as id_parte, a.ORDEN as orden, a.SVG as svg
from PRENDA a
where a.ID_PARTE = :id_parte
and a.NOMBRE = :nombre
and exists (select 1 from PRENDA_GENERO b where b.ID_PRENDA = a.ID and b.ID_GENERO = :id_genero )
"""
        lista_campos = ['id','nombre','id_parte','orden','svg']
        for grupo in sopa.svg.find('g', id= 'layer2').find_all('g'):
            lista_nombre = grupo['id'].split('_')
            if len(lista_nombre) != 3 or lista_nombre[0] not in partes or lista_nombre[1] not in generos:
                print( grupo['id'] + ' no procesado' )
                continue
            registros_exitentes = con.consultar( sqlFindPrenda , {'id_parte' : partes[ lista_nombre[0] ], 'nombre' : lista_nombre[2], 'id_genero' : generos[ lista_nombre[1] ] }, lista_campos )
            grupo_id = grupo['id']
            grupo['id']='{id}'
            grupo['transform'] = "translate({offset_x} {offset_y}) scale({escala_x} {escala_y})"
            try:
                if len(registros_exitentes) == 0:
                    # insertando Parte y Parte Genero
                    registro = Prendas.nuevoDiccionario()
                    registro['nombre'] = lista_nombre[2]
                    registro['id_parte'] = partes[ lista_nombre[0] ]
                    registro['orden'] = 1
                    registro['svg'] = str(grupo).replace('#888888','{color}')
                    Prendas.insertar(con, registro)
                    registro_genero = PrendasGenero.nuevoDiccionario()
                    registro_genero['id_prenda'] = registro['id']
                    registro_genero['id_genero'] = generos[ lista_nombre[1] ]
                    PrendasGenero.insertar(con, registro_genero)
                    print( grupo_id + ' ingresado' )
                else:
                    # actualizando Parte
                    registro = registros_exitentes[0]
                    registro['svg'] = str(grupo).replace('#888888','{color}')
                    Prendas.actualizar(con, registro)
                    print( grupo_id + ' actualizado' )
                con.commit()
            except Exception as ex:
                con.rollback()
        con.close()

