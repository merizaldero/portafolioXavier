import xpd_orm as orm
from os.path import abspath , dirname, exists

PATH_BDD = dirname(abspath(__file__)) + "/data/base.db"
PATH_INIT = dirname(abspath(__file__)) + "/data/init.sql"
PATH_72 = dirname(abspath(__file__)) + "/data/72.txt"
PATH_95 = dirname(abspath(__file__)) + "/data/95.txt"
PATH_96 = dirname(abspath(__file__)) + "/data/96.txt"
PATH_97 = dirname(abspath(__file__)) + "/data/97.txt"

Promociones = orm.Entidad()
Promociones.setMetamodelo({
    "nombreTabla":"PROMOCION",
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
        ],
    "namedQueries":[
        {
            "nombre":"findall",
            "orderBy":["nombre",]
            },
        {
            "nombre":"findById",
            "whereClause":["id",]
            }
        ]
    })

Asistentes = orm.Entidad()
Asistentes.setMetamodelo({
    "nombreTabla":"ASISTENTE",
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
            "tamano":64,
            },
        {
            "nombre":"id_promocion",
            "nombreCampo":"ID_PROMOCION",
            "tipo":orm.XPDINTEGER,
            },
        {
            "nombre":"chequeo",
            "nombreCampo":"CHEQUEO",
            "tipo":orm.XPDSTRING,
            "tamano":8,
            },
        ],
    "namedQueries":[
        {
            "nombre":"findall",
            "orderBy":["nombre",]
            },
        {
            "nombre":"findById",
            "whereClause":["id",]
            }
        ]
    })

def inicializar():
  entidades = [Promociones, Asistentes]
  con = orm.Conexion(PATH_BDD)
  try:
      for entidad in entidades:
          entidad.crearTabla(con)
      if exists( PATH_INIT ):
          con.ejecutarFileScript( PATH_INIT )
      for par in [ (PATH_72,72), (PATH_95,95) , (PATH_96,96), (PATH_97,97) ]:
          if exists( par[0] ):
              file = open( par[0], 'rt')
              while True:
                  linea = file.readline()
                  if linea is None or linea == '':
                      break
                  registro = Asistentes.insertar(con, {"nombre": linea.strip().upper(),"id_promocion": par[1], "chequeo":"1"})
                  print( linea.strip().upper() + repr(registro) )
              file.close()
      con.commit()
  except Exception as ex:
      con.rollback()
      print(ex)
      raise Exception(str(ex))
  finally:
      con.close()

def findPromociones():
    con = orm.Conexion(PATH_BDD)
    promociones = Promociones.getNamedQuery(con, "findall", {})
    con.close()
    return promociones

def findAsistentes():
    con = orm.Conexion(PATH_BDD)
    asistentes = Asistentes.getNamedQuery(con, "findall", {})
    con.close()
    for x in asistentes:
        x['chequeo'] = "true" == str(x['chequeo']).lower()
    return asistentes

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

def findAsistenteById(id):
    resultado = None
    con = orm.Conexion(PATH_BDD)
    lista = Asistentes.getNamedQuery( con, "findById", {"id":id} )
    con.close()
    if len(lista) == 1:
        resultado = lista[0]
    return resultado

def actualizarAsistente(asistente):
    transaccionar(Asistentes.actualizar, asistente)
