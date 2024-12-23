import xpd_orm as orm
from os.path import abspath , dirname, exists

PATH_BDD = dirname(abspath(__file__)) + "/data/base.db"
PATH_INIT = dirname(abspath(__file__)) + "/data/init.sql"

Sorteos = orm.Entidad()
Sorteos.setMetamodelo({
    "nombreTabla":"SORTEOS",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, },
        { "nombre":"fecha", "nombreCampo":"FECHA", "tipo":orm.XPDSTRING, "tamano":10, },
        ],
    "namedQueries":[
        { "nombre":"findall", "orderBy":["fecha",] },
        { "nombre":"findById", "whereClause":["id",] },
        { "nombre":"findByFecha", "whereClause":["fecha",] },
        ]
    })

Premiados = orm.Entidad()
Premiados.setMetamodelo({
    "nombreTabla":"PREMIADOS",
    "propiedades":[
        { "nombre":"id", "nombreCampo":"ID", "tipo":orm.XPDINTEGER, "pk":True, "incremental":True, },
        { "nombre":"id_sorteo", "nombreCampo":"ID_SORTEO", "tipo":orm.XPDINTEGER, },
        { "nombre":"orden", "nombreCampo":"ORDEN", "tipo":orm.XPDINTEGER, },
        { "nombre":"premiado", "nombreCampo":"PREMIADO", "tipo":orm.XPDSTRING, "tamano":6, },
        ],

    "namedQueries":[
        { "nombre":"findAll", "orderBy":["id_sorteo", "orden",] },
        { "nombre":"findBySorteo", "whereClause":["id_sorteo",], "orderBy":["orden",] },
        { "nombre":"findById", "whereClause":["id",] }
        ],
    })

Probabilidades = orm.Entidad()
Probabilidades.setMetamodelo({
    "nombreTabla":"PROBABILIDADES",
    "propiedades":[
        {
            "nombre":"id",
            "nombreCampo":"ID",
            "tipo":orm.XPDINTEGER,
            "pk":True,
            "incremental":True,
            },
        {
            "nombre":"posicion",
            "nombreCampo":"POSICION",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"digito",
            "nombreCampo":"DIGITO",
            "tipo":orm.XPDSTRING,
            "tamano":1,
            },
        {
            "nombre":"probabilidad",
            "nombreCampo":"PROBABILIDAD",
            "tipo":orm.XPDREAL,
            "tamano":5,
            "precision":4,
            },
        {
            "nombre":"ranking",
            "nombreCampo":"RANKING",
            "tipo":orm.XPDSTRING,
            "tamano":8,
            },
        ],

    "namedQueries":[
        {
            "nombre":"findAll",
            "orderBy":["posicion","digito",]
            },
        {
            "nombre":"findByRanking",
            "whereClause":["ranking",],
            "orderBy":["posicion","probabilidad"]
            },
        {
            "nombre":"findByPosicion",
            "whereClause":["posicion",],
            "orderBy":["digito",]
            },
        {
            "nombre":"findByPosicionDigito",
            "whereClause":["posicion","digito"],
            },
        ],
    })

POSICIONES = list(range(6))
DIGITOS = [str(x) for x in range(10)]

def inicializar():
    entidades = [Sorteos, Premiados, Probabilidades]
    con = orm.Conexion(PATH_BDD)
    try:
        for entidad in entidades:
            entidad.crearTabla(con)
        if exists( PATH_INIT ):
            con.ejecutarFileScript( PATH_INIT )
        # Genera la Tabla de Probabilidades
        con.commit()
    except Exception as ex:
        con.rollback()
        print(ex)
        raise Exception(str(ex))
    finally:
        con.close()
    
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

def poblar_probabilidades(con: orm.Conexion, objeto):
    con.consultar('delete from PROBABILIDADES', {}, [])
    for posicion in POSICIONES:
        for digito in DIGITOS:
            probabilidad = {}
            probabilidad['posicion'] = posicion
            probabilidad['digito'] = digito
            probabilidad['probabilidad'] = 0.0
            probabilidad['ranking'] = 'black'
            Probabilidades.insertar(con, probabilidad)

def crear_sorteo(con, sorteo):
    return transaccionar(Sorteos.insertar, sorteo)
    
def crear_premiado(con, premiado):
    return transaccionar(Premiados.insertar, premiado)
        
def find_ultimo_sorteo():
    con = orm.Conexion(PATH_BDD)
    max_id = con.consultarEscalar("select max(id) from SORTEOS", {})
    con.close()
    return max_id

def mostrar_probabilidad(numero):
    numero = numero.strip()
    if len(numero) != len(POSICIONES):
        raise Exception("Entrada no valida "+ numero)
    con = orm.Conexion(PATH_BDD)
    resultado = []
    for posicion in POSICIONES:
        probabilidad = Probabilidades.getNamedQuery(con, "findByPosicionDigito", {'posicion': posicion, 'digito': numero[posicion] }) [0]
        resultado.append(probabilidad)
    con.close()
    return [ x['ranking'] for x in resultado ]

def findProbabilidadesByRanking(ranking):
    sql = "SELECT id as id, posicion as posicion, digito as digito, probabilidad as probabilidad, ranking as ranking FROM PROBABILIDADES  WHERE RANKING = :ranking  ORDER BY POSICION, PROBABILIDAD DESC"
    #print(Probabilidades.getNamedQuerySql("findByRanking"))
    con = orm.Conexion(PATH_BDD)
    # resultado = Probabilidades.getNamedQuery(con, "findByRanking", { 'ranking': ranking })
    resultado = con.consultar(sql, { 'ranking': ranking }, ['id', 'posicion', 'digito', 'probabilidad', 'ranking'] )
    con.close()
    return resultado
