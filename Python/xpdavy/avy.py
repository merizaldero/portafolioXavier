import xpd_orm as orm
from os.path import abspath , dirname, exists
from bs4 import BeautifulSoup
from random import choice
from numpy import arange

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
            "nombre":"findAll",
            "whereClause":["activo",],
            "orderBy":["nombre",]
            },
        {
            "nombre":"findByNombre",
            "whereClause":["nombre",],
            },
        {
            "nombre":"findById",
            "whereClause":["id",]
            }
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
            "tamano":6,
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
            "tamano":6,
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

def trxCrearAvatar(conexion, avatar_info ):
    """
    Crea avatar y sus prendas
    """
    Avatares.insertar(conexion, avatar_info)
    avatar_info = Avatares.insertar(conexion, avatar_info)
    prendas = findPrendasByGenero( conexion, avatar_info["id_genero"] )

    avatar_info["prendas"] = []
    for prenda in prendas:
        prenda_avatar = {
            "id_avatar" : avatar_info["id"],
            "id_parte" : prenda["id_parte"],
            "id_prenda" : prenda["id_prenda"],
            "offset_x" : 0,
            "offset_y": 0,
            "escala": 1.0,
            "color": prenda["default_color"],
            }
        avatar_info["prendas"].append( PrendasAvatar.insertar(conexion, prenda_avatar) )
    return avatar_info

def ajustar_coordenadas(prendasAvatar):
    pass

def findPrendasByAvatar(conexion, id_avatar ):
    sql = """
SELECT
    """

def lista_rango(minimo, maximo, steps):
    if maximo == minimo or steps <= 1:
        return [maximo]
    return list(arange( minimo + 0.0, maximo + 0.0, (maximo - minimo + 0.0) / steps ) )

def generarPrendasByGenero(conexion, id_genero ):
    partes = Partes.getNamedQuery(conexion, 'findall',{})
    prendas = findPrendasByGenero(conexion, id_genero)
    colores_piel = ColoresPiel.getNamedQuery(conexion, 'findall',{})
    color_piel = choice(colores_piel)['color']
    colores_partes = ColoresParte.getNamedQuery(conexion, 'findall',{})
    # campos_prenda_avatar = [ "id", "id_avatar", "id_parte", "id_prenda", "offset_x", "offset_y", "escala", "color" ]
    for parte in partes:
        prendas_parte = [ prenda for prenda in prendas if prenda['id_parte'] == parte['id'] ]
        colores_parte = [ color['color'] for color in colores_partes if color['id_parte'] == parte['id'] ]
        if parte['opcional'] == '1':
            prendas_parte = [ { "id_prenda":None, "nombre":None, "id_parte":None, "svg":None } ] + prendas_parte
        prenda = choice(prendas_parte)
        parte["id_prenda"] = prenda["id_prenda"]
        parte["svg"] = prenda["svg"]
        parte["offset_x"] = choice( lista_rango( parte['offset_x_min'], parte['offset_x_max'], parte['offset_x_steps'] ))
        parte["offset_y"] = choice( lista_rango( parte['offset_y_min'], parte['offset_y_max'], parte['offset_y_steps'] ))
        parte["escala"] = choice( lista_rango( parte['scale_min'], parte['scale_max'], parte['scale_steps'] ))
        parte["color"] = choice(colores_parte) if len(colores_parte) > 0 else color_piel
    return {'color_piel': color_piel, 'prendas': partes}

def ajustarTransformaciones(data):
    return data['prendas']

def generarSvgAvatar(data):
    color_piel = data['color_piel']
    prendas = ajustarTransformaciones(data)
    resultado = """<svg>
""" + "\n".join( [ aplicar_transformaciones(prenda['svg'], 'g_{1}_{0}'.format(prenda['id'], prenda['nombre']), prenda['offset_x'], prenda['offset_y'], prenda['escala'], prenda['color'], prenda['simetrico_x'] ) for prenda in prendas ] ) + """
</svg>"""
    return resultado

def findAvatarById(id):
    resultado = None
    con = orm.Conexion(PATH_BDD)
    lista = Avatares.getNamedQuery(conexion, "findById", {"id":id})
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

def aplicar_transformaciones(nodo_svg, id, offset_x, offset_y, escala, color, simetrico_x ):
    if nodo_svg is None:
        return ''
    resultado = nodo_svg.format( id = id, offset_x = offset_x, offset_y = offset_y, escala = escala, color = color )
    if simetrico_x == '1':
        resultado += """<use xlink:href="#{id}" id="m{id}" transform="translate({offset_x} {offset_y}) scale({escala_x} {escala_y})" />""".format( id = id, offset_x = - offset_x, offset_y = offset_y, escala_x = -escala, escala_y = escala )
    return resultado

def importar_partes():
    if exists(PATH_IMPORT):
        con = orm.Conexion(PATH_BDD)
        generos = {'M':1, 'F':2}
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
            grupo['transform'] = "translate({offset_x} {offset_y}) scale({escala})"
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