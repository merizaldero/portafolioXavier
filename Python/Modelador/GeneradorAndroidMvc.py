def generarModelo(modelo):
    nombre_modulo = get_filename_modelo(modelo)
    resultado = { 'archivos' : [] }
    entidades = getObjetosModeloByTipo(modelo, 'ENTIDAD')
    for entidad in entidades:
        resultado['archivos'].append({"path":"src/java/{nombre_modulo}/entidad/{nombre_entidad}.kt".format(nombre_modulo = nombre_modulo, nombre_entidad = entidad['nombre']), "contenido": generar_dataclass(entidad,modelo) })
        resultado['archivos'].append({"path":"src/java/{nombre_modulo}/manager/{nombre_entidad}Manager.kt".format(nombre_modulo = nombre_modulo, nombre_entidad = entidad['nombre']), "contenido": generar_entidad_manager(entidad,modelo) })
    return resultado

def get_filename_modelo(modelo):
    return camelizar_nombre( modelo['__objetoRaiz']['nombre'].lower().strip().replace(' ','_'))

def getObjetosModeloByTipo( modelo, idTipoMetamodelo ):
    resultado = []
    cola = [modelo['__objetoRaiz']]
    while len(cola) > 0:
        objetoModelo = cola.pop(0)
        if objetoModelo['idTipoMetamodelo'] == idTipoMetamodelo:
            resultado.append(objetoModelo)
        for lista in objetoModelo['__listas'].keys():
            for hijo in objetoModelo['__listas'][lista]:
                cola.append(hijo)
    return resultado

def camelizar_nombre(nombre):
    partes_nombre = [x for x in nombre.split("_") if len(x) > 0]
    return partes_nombre[0] + "".join([ x[0].upper() + x[1:].lower() for x in partes_nombre[1:] ])

def generar_dataclass(entidad,modelo):
    nombre_modulo = get_filename_modelo(modelo)
    campos = entidad['__listas']['Campos']
    definiciones_campos = ['    val {0}:{1}'.format(camelizar_nombre(campo['nombre']), get_tipo_kotlin(campo['__atributos']['tipo'])) for campo in campos]
    contenido = """package {nombre_modulo}.entidad
data class {nombre_entidad}(
{definiciones_campos}
)
""".format(nombre_modulo = nombre_modulo, nombre_entidad = entidad['nombre'], definiciones_campos = ",\n".join(definiciones_campos) )
    return contenido

MAPA_TIPOS = {"STRING":"String", "INTEGER":"Int", "LONG":"Long", "BOOLEAN":"Boolean", "REAL":"Float", "DECIMAL":"Float", "DATE":"Date", "BLOB":"ByteArray" }
def get_tipo_kotlin(tipo):
    if tipo in MAPA_TIPOS.keys():
        return MAPA_TIPOS[tipo]
    return tipo

MAPA_TIPOS_SQL = {"STRING":"TEXT", "INTEGER":"INTEGER", "LONG":"BIGINT", "BOOLEAN":"BOOLEAN", "REAL":"REAL", "DECIMAL":"REAL", "DATE":"DATE", "BLOB":"BLOB" }
def get_tipo_sql(tipo):
    if tipo in MAPA_TIPOS_SQL.keys():
        return MAPA_TIPOS_SQL[tipo]
    return tipo

def getObjetoPadre(modelo, idObjeto):
    cola = [modelo['__objetoRaiz']]
    while len(cola) > 0:
        objetoModelo = cola.pop(0)
        for lista in objetoModelo['__listas'].keys():
            for hijo in objetoModelo['__listas'][lista]:
                if hijo['idObjeto'] == idObjeto:
                    return objetoModelo
                cola.append(hijo)
    return None

def generar_entidad_manager(entidad,modelo):
    nombre_modulo = get_filename_modelo(modelo)
    nombreTabla = entidad['__atributos']['nombreTabla']
    campos = entidad['__listas']['Campos']
    camposPk = [x for x in campos if x['__atributos']['pk'] == '1' ]
    namedQueries = entidad['__listas']['NamedQuieries']

    campoOrden = [x for x in campos if x['nombre'] == 'orden']    
    if len(campoOrden) == 0:
        campoOrden = None
    else:
        campoOrden = campoOrden[0]

    if len(camposPk) > 0:
        namedQueries = namedQueries + [{'nombre':'findById', '__listas':{'camposWhere':[{'nombre':x['nombre'] for x in camposPk}]} }]

        findAll_generado = False

    if 'entidadUsuario' in entidad['__atributos'].keys() and entidad['__atributos']['entidadUsuario'] == '1':
        campos = campos + [{'nombre':'id_user' , '__atributos':{ 'nombreCampo':'ID_USER', 'tipo': 'INTEGER', 'obligatorio':True, 'incremental':False } }]
        namedQueries = namedQueries + [{'nombre':'findByUser', '__listas':{'camposWhere':[{'nombre':'id_user'}]} }]
        if campoOrden is not None:
            namedQueries[-1]['__listas']['camposOrderBy'] = [{'nombre':'orden'}]
        findAll_generado = True

    maestro = getObjetoPadre(modelo, entidad['idObjeto']) if entidad['idJerarquia'] == 'EntidadesDetalle' else None
    if maestro is not None:
        id_maestro = "id_" + maestro['nombre'].lower()
        fk_maestro = "FK_{0}_{1}".format( nombreTabla.upper(), maestro['nombre'].upper() ) 
        campos = campos + [{'nombre':id_maestro , '__atributos':{ 'nombreCampo':id_maestro.upper(), 'tipo': 'INTEGER', 'obligatorio':True, 'incremental':False } }]
        namedQueries = namedQueries + [{'nombre':'findBy' + maestro['nombre'] , '__listas': {'camposWhere':[{'nombre':id_maestro}]} }]
        if campoOrden is not None:
            namedQueries[-1]['__listas']['camposOrderBy'] = [{'nombre':'orden'}]
        print("Se incorpora {0} a campos de {1}".format(id_maestro, entidad['nombre'])) 
        findAll_generado = True
    
    if not findAll_generado:
        namedQueries = namedQueries + [{'nombre':'findAll' , '__listas': {} }]
        if campoOrden is not None:
            namedQueries[-1]['__listas']['camposOrderBy'] = [{'nombre':'orden'}]    
    
    contenido = "package " + nombre_modulo + """.manager
import android.content.ContentValues
import android.content.Context
import android.database.Cursor
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import """ + nombre_modulo + ".entidad." + entidad['nombre'] + """

class """ + entidad['nombre'] + """Manager(context: Context){
    companion object {
        private const val DATABASE_NAME = """ + '"' + nombre_modulo + '.db"' + """
        private const val TABLE_NAME = """ + '"' + entidad['__atributos']['nombreTabla'] + '.db"' + """
        private const val VERSION = 1
    }

    private val dbHelper = DatabaseHelper(context)

    private class DatabaseHelper(context: Context) : SQLiteOpenHelper(context, DATABASE_NAME, null, VERSION) {
        override fun onCreate(db: SQLiteDatabase?) {
            db?.execSQL("CREATE TABLE $TABLE_NAME (" +
"""
    for indice, campo in enumerate(campos):
        contenido += " " * 20 + '"' + campo['__atributos']['nombreCampo'].lower() + " " + get_tipo_sql(campo['__atributos']['tipo'])
        if campo['__atributos']['pk'] == "1":
            contenido += " PRIMARY KEY"
        if campo['__atributos']['incremental'] == "1":
            contenido += " AUTOINCREMENT"
        if campo['__atributos']['obligatorio'] == "1":
            contenido += " NOT NULL"
        if indice < len(campos) -1:
            contenido += ",\" +"
        else: 
            contenido += ")\")"
        contenido += "\n"
    contenido +="""
        }

        override fun onUpgrade(db: SQLiteDatabase?, oldVersion: Int, newVersion: Int) {
            // Implementar lógica para actualizar la base de datos si es necesario
        }
        
    }

    fun insertar(""" + entidad['nombre'].lower() + ": " + entidad['nombre'] + """): Long {
        val db = dbHelper.writableDatabase
        val contentValues = ContentValues().apply {
"""
    for campo in campos:
        if campo["__atributos"]["pk"] == "1":
            continue
        contenido += " " * 12 + "put(\"" + campo['__atributos']['nombreCampo'].lower() + "\", " + entidad['nombre'].lower() + "." + camelizar_nombre(campo['__atributos']['nombreCampo']) + ")\n"
    contenido += """
        }
        return db.insert(TABLE_NAME, null, contentValues)
    }

    fun actualizar(""" + entidad['nombre'].lower() + ": " + entidad['nombre'] + """): Int {
        val db = dbHelper.writableDatabase
        val contentValues = ContentValues().apply {
"""
    for campo in campos:
        if campo["__atributos"]["pk"] == "1":
            continue
        contenido += " " * 12 + "put(\"" + campo['__atributos']['nombreCampo'].lower() + "\", " + entidad['nombre'].lower() + "." + camelizar_nombre(campo['__atributos']['nombreCampo']) + ")\n"
    contenido += """
        }
        return db.update(TABLE_NAME, contentValues, "id = ?", arrayOf(enlace.id.toString()))
    }
    fun eliminar(id: Int): Int {
        val db = dbHelper.writableDatabase
        return db.delete(TABLE_NAME, "id = ?", arrayOf(id.toString()))
    }
"""
    for namedQuery in namedQueries:
        campos_where = [ x['nombre'] for x in namedQuery['__listas']['camposWhere'] ] if 'camposWhere' in namedQuery['__listas'].keys() else []
        campos_order = [ x['nombre'] for x in namedQuery['__listas']['camposOrderBy'] ] if 'camposOrderBy' in namedQuery['__listas'].keys() else []
        contenido += """
    fun """ + namedQuery['nombre'] + "(" + ",".join([camelizar_nombre(x) for x in campos_where]) + "): Array<" + entidad['nombre'] + """> {
        val db = dbHelper.readableDatabase
        val cursor = db.rawQuery("SELECT """ + ", ".join([ x['nombre'].lower() for x in campos]) + " FROM $TABLE_NAME "
        if len(campos_where) > 0:
            contenido += "WHERE " + " AND ".join( [ x.lower() + " = ?" for x in campos_where] )
        if len(campos_order) > 0:
            contenido += "ORDER BY " + ", ".join( [ x.lower() for x in campos_order] )
        contenido += "\", "
        if len(campos_where) > 0:
            contenido += "arrayOf("+ ", ".join([camelizar_nombre(x) + ".toString()" for x in campos_where]) +")"
        else:
            contenido += "null"
        contenido +=""")
        val """ + entidad["nombre"].lower() +"s = mutableListOf<"+ entidad["nombre"] +""">()
        while (cursor.moveToNext()) {
            """ + entidad["nombre"].lower() +"""s.add(
                """ + entidad["nombre"] +"""(
"""
        for indice, campo in enumerate(campos):
            contenido += "{0}cursor.get{1}({2})".format( " " * 20, get_tipo_kotlin(campo['__atributos']['tipo']), indice )
            if indice < len(campos) - 1:
                contenido += ","
            contenido += "\n"
        contenido += """
                )
            )
        }
        cursor.close()
        return enlaces.toTypedArray()        
    }
"""
    contenido + """
}
"""
    return contenido