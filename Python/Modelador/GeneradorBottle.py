import ModeladorDao
import config

def generarModelo(modelo):
    nombre_modulo = get_filename_modelo(modelo)
    resultado = { 'archivos' : [ { 'path':nombre_modulo  + '.py',     'contenido': generar_api(modelo) },
                                 { 'path':'views/' + nombre_modulo + '/main.tpl',     'contenido': generar_view_main_tpl(modelo) },
                                 { 'path':'views/' + nombre_modulo + '/encabezado.tpl',     'contenido': generar_view_encabezado_tpl(modelo) },
                                 { 'path':'views/' + nombre_modulo + '/pie.tpl',     'contenido': generar_view_pie_tpl(modelo) },
                                 ]}
    entidades = getObjetosModeloByTipo(modelo, 'ENTIDAD')
    for entidad in entidades:
        lista = generar_archivos_entidad(entidad, modelo)
        resultado['archivos'] += lista
    return resultado

def get_filename_modelo(modelo):
    return modelo['__objetoRaiz']['nombre'].lower().strip().replace(' ','_')

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

def esEntidadUsuario(modelo, idObjeto):
    cola = [x for x in modelo['__objetoRaiz']['__listas']['Entidades'] if x['__atributos']['entidadUsuario'] == "1"]
    while len(cola) > 0:
        objetoModelo = cola.pop(0)
        if objetoModelo['idObjeto'] == idObjeto:
            return True
        cola = cola + objetoModelo['__listas']['EntidadesDetalle'] 
    return False

def getEntidadesUsuario(modelo):
    cola = [x for x in modelo['__objetoRaiz']['__listas']['Entidades'] if x['__atributos']['entidadUsuario'] == "1"]
    resultado = cola.copy()
    while len(cola) > 0:
        objetoModelo = cola.pop(0)
        cola = cola + objetoModelo['__listas']['EntidadesDetalle'] 
        resultado = resultado + objetoModelo['__listas']['EntidadesDetalle'] 
    return resultado 
       
def generar_api(modelo):
    contenido = """import xpd_orm as orm
from os.path import abspath , dirname, join, exists
from os import makedirs
from os import remove as remove_file

from bottle import run, debug, route, abort, static_file, template, request, response, redirect
from bottle import Bottle
import datetime

import xpd_usr

PATH_BDD = dirname(abspath(__file__)) + "/data/{0}.db"
CONFIG = {1}

import datetime

def fecha_js_to_iso(fecha_hora):
    try:
        fecha_hora_obj = datetime.datetime.strptime(fecha_hora, '%m/%d/%Y %I:%M %p')
        fecha_hora_iso = fecha_hora_obj.strftime('%Y-%m-%d %H:%M')
        return fecha_hora_iso
    except ValueError:
        raise ValueError("Formato de fecha y hora inválido. Debe ser mm/dd/yyyy HH:MM AM/PM")

def fecha_iso_to_js(fecha_hora):
    try:
        fecha_hora_obj = datetime.datetime.strptime(fecha_hora, '%Y-%m-%d %H:%M')
        fecha_hora_js = fecha_hora_obj.strftime('%m/%d/%Y %I:%M %p')
        return fecha_hora_js
    except:
        return ""

""".format(get_filename_modelo(modelo),repr({'rutas':[]}))
    entidades = getObjetosModeloByTipo(modelo, 'ENTIDAD') 
    for entidad in entidades:
        contenido += generar_entidad_manager(entidad, modelo)
    
    contenido += generar_inicializar( entidades )

    entidades_owned = getEntidadesUsuario(modelo)
    # genera funciones utilitarias para manejar jerarquia de negocio 
    for entidad in entidades_owned:
        contenido += generar_entidad_getowner(entidad, modelo)
    
    # agrega funciones para servir la API de cada entidad y sus respectivos mapeos
    for entidad in entidades:
        maestro = getObjetoPadre(modelo, entidad['idObjeto']) if entidad['idJerarquia'] == 'EntidadesDetalle' else None
        campos_blob = [x for x in entidad['__listas']['Campos'] if x['__atributos']['tipo'] == 'BLOB']

        for campo in campos_blob:
            contenido += generar_servir_download_entidad_blob(campo, entidad, modelo)

        contenido += generar_servir_page_editar_entidad(entidad, modelo)
        contenido += generar_servir_page_insertar_entidad(entidad, modelo)
        # contenido += generar_servir_api_insertar_entidad(entidad, modelo)
        # contenido += generar_servir_api_get_entidad_lista(entidad, modelo)
        
        if maestro is None:
            contenido += generar_servir_page_get_entidad_lista(entidad, modelo)
        
        # contenido += generar_servir_api_get_entidad_byid(entidad, modelo)
        contenido += generar_servir_page_get_entidad_byid(entidad, modelo)
    #agrega funciones para servir pagina inicial y de administracion
    contenido += generar_servir_page_main(modelo)
    contenido += generar_servir_page_admin_main(modelo)

    # rutear modulo mapea todas las rutas
    contenido += """
def rutearModulo( app : Bottle, ruta_base : str ):
    CONFIG['RUTA_BASE'] = ruta_base
    for item in CONFIG['rutas']:
        app.route( ruta_base + item['ruta'], method = item['metodos'] )( item['funcion'])
"""
    return contenido

def generar_entidad_manager(entidad, modelo):
    nombre_objeto_entidad = entidad['nombre'] + 's'
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
        campos = campos + [{'nombre':'id_user' , '__atributos':{ 'nombreCampo':'ID_USER', 'tipo': 'INTEGER', 'tamano': 0, 'precision': 0, 'obligatorio':True, 'incremental':False } }]
        namedQueries = namedQueries + [{'nombre':'findByUser', '__listas':{'camposWhere':[{'nombre':'id_user'}]} }]
        if campoOrden is not None:
            namedQueries[-1]['__listas']['camposOrderBy'] = [{'nombre':'orden'}]
        findAll_generado = True

    maestro = getObjetoPadre(modelo, entidad['idObjeto']) if entidad['idJerarquia'] == 'EntidadesDetalle' else None
    if maestro is not None:
        id_maestro = "id_" + maestro['nombre'].lower()
        fk_maestro = "FK_{0}_{1}".format( nombreTabla.upper(), maestro['nombre'].upper() ) 
        campos = campos + [{'nombre':id_maestro , '__atributos':{ 'nombreCampo':id_maestro.upper(), 'tipo': 'INTEGER', 'tamano': 0, 'precision': 0, 'obligatorio':True, 'incremental':False } }]
        namedQueries = namedQueries + [{'nombre':'findBy' + maestro['nombre'] , '__listas': {'camposWhere':[{'nombre':id_maestro}]} }]
        if campoOrden is not None:
            namedQueries[-1]['__listas']['camposOrderBy'] = [{'nombre':'orden'}]
        print("Se incorpora {0} a campos de {1}".format(id_maestro, entidad['nombre'])) 
        findAll_generado = True
    
    if not findAll_generado:
        namedQueries = namedQueries + [{'nombre':'findAll' , '__listas': {} }]
        if campoOrden is not None:
            namedQueries[-1]['__listas']['camposOrderBy'] = [{'nombre':'orden'}]    
    
    contenido = """
{0} = orm.Entidad()
{0}.setMetamodelo(""".format(nombre_objeto_entidad) + "{" + """
    'nombreTabla' : '{0}',
    'propiedades' : [
""".format(nombreTabla)
    
    for campo in campos:
        contenido += "        { "
        contenido += "'nombre':'{0}', 'nombreCampo':'{1}', ".format(campo['nombre'], campo['__atributos']['nombreCampo'])
        
        if campo['__atributos']['tipo'] in ["STRING","EMAIL"]:
            contenido += "'tipo':orm.XPDSTRING, 'tamano':{0}, ".format(campo['__atributos']['tamano'])
        elif campo['__atributos']['tipo'] in ["DATE","DATETIME"]:
            contenido += "'tipo':orm.XPDDATE, "
        elif campo['__atributos']['tipo'] == "INTEGER":
            contenido += "'tipo':orm.XPDINTEGER, "
        elif campo['__atributos']['tipo'] == "LONG":
            contenido += "'tipo':orm.XPDLONG, "
        elif campo['__atributos']['tipo'] == "BOOLEAN":
            contenido += "'tipo':orm.XPDBOOLEAN, "
        elif campo['__atributos']['tipo'] == "BLOB":
            contenido += "'tipo':orm.XPDLONGBINARY, "
        elif campo['__atributos']["tipo"] in ["DECIMAL","REAL"]:
            contenido += "'tipo':orm.XPDREAL, "
            if 'tamano' in campo['__atributos'].keys():
                contenido += "'tamano': {0}, ".format(campo['__atributos']['tamano'])
            if 'precision' in campo['__atributos'].keys():
                contenido += "'precision': {0}, ".format(campo['__atributos']['precision'])
        for propiedad in ['pk','incremental','insert','update']:
            if propiedad in campo['__atributos'].keys():
                contenido += "'{0}': {1}, ".format( propiedad, 'True' if campo['__atributos'][propiedad] == '1' else 'False')
        contenido += "},\n"
    contenido += """        ],
    'namedQueries' : [
"""
    for namedQuery in namedQueries:
        contenido += "        { "
        contenido += "'nombre':'{0}', ".format(namedQuery['nombre'] )
        grupos_campos = [{'key':'camposWhere', 'grupo':'whereClause'}, {'key':'camposOrderBy', 'grupo':'orderBy'}]
        for grupo_campos in grupos_campos:
            if grupo_campos['key'] in namedQuery['__listas'].keys() and len(namedQuery['__listas'][grupo_campos['key']]) > 0:
                campos_pr = [x['nombre'] for x in namedQuery['__listas'][grupo_campos['key']]]
                contenido +="'{0}':{1}, ".format(grupo_campos['grupo'], repr(campos_pr))
        contenido += "},\n"
    contenido += """        ]
    })
"""
    return contenido

def generar_inicializar (entidades):
    nombres_entidades = ", ".join([ x['nombre'] + 's' for x in entidades])
    return """

def inicializar():
    entidades = [{0}]
    con = orm.Conexion(PATH_BDD)
    try:
        for entidad in entidades:
            entidad.crearTabla(con)
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
    
""".format(nombres_entidades)

def generar_entidad_getowner(entidad, modelo):
    variable_entidad = entidad['nombre'].lower()
    contenido = """
def {0}_getowner(conexion, id_{0}):
    objeto = {1}s.getNamedQuery(conexion, 'findById', {2})
    if len(objeto) == 0:
        return (None, None)
    objeto = objeto[0]
""".format(variable_entidad,entidad['nombre'], "{'id': id_"+variable_entidad+ "}" )
    if entidad['__atributos']['entidadUsuario'] == "1":
        contenido += """
    return (objeto, objeto['id_user'])
"""
    else:
        maestro = getObjetoPadre(modelo, entidad['idObjeto']) if entidad['idJerarquia'] == 'EntidadesDetalle' else None
        contenido += """
    return (objeto, {0}_getowner(conexion, objeto['id_{0}'])[1] )
""".format(maestro['nombre'].lower())
    return contenido

def generar_servir_api_get_entidad_byid(entidad, modelo):
    es_entidad_usuario = esEntidadUsuario(modelo,entidad['idObjeto'])
    campos = entidad['__listas']['Campos']
    camposPk = [x for x in campos if x['__atributos']['pk'] == '1' ]
    campos = [x for x in campos if x["__atributos"]["update"] == "1" ]
    maestro = getObjetoPadre(modelo, entidad['idObjeto']) if entidad['idJerarquia'] == 'EntidadesDetalle' else None

    contenido = """
def servir_api_get_{0}_byid(id_{0}):    
""".format(entidad['nombre'].lower())
    if es_entidad_usuario:
        contenido += """
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso denegado" )
    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = {0}_getowner(conexion, id_{0})
    conexion.close()
    if objeto is None:
        abort( 404, "No encontrado" )    
    if usuario['id'] != id_user_owner:
        abort( 403, "Acceso no autorizado" )
""".format(entidad['nombre'].lower())
    else:
        contenido += """
    conexion = orm.Conexion(PATH_BDD)
    objeto = {0}s.getNamedQuery(conexion, 'findById', {1})
    conexion.close()
    if len(objeto) == 0:
    print("Arrojado 404")
        abort( 404, "No Encontrado" )
    objeto = objeto[0]
    if request.method == "GET":
        return objeto

    # Asume envio POST
""".format(entidad['nombre'],"{'id': id_"+entidad['nombre'].lower()+"}")

    # lee cada campo y valida que su presencia si es obligatorio
    for campo in campos:
        tipo = campo["__atributos"]["tipo"]
        tamano = campo["__atributos"]["tamano"]
        # precision = campo["__atributos"]["precision"]
        obligatorio = campo["__atributos"]["obligatorio"]
        if tipo == "BLOB":
            contenido += """
    file_{0} = request.files.get("{0}")
    filename_{0} = file_{0}.filename
    temppath_{0} = join( dirname(abspath(__file__)), "upload", filename_{0} )
    if not exists( dirname(temppath_{0}) ):
        makedirs( dirname(temppath_{0}) )
    file_{0}.save(temppath_{0})
    with open( temppath_{0} , 'rb' ) as stream_{0}:
        objeto["{0}"] = stream_{0}.read()
    remove_file(temppath_{0})
""".format(campo["nombre"])    
            continue
        contenido += """
    objeto["{0}"] = request.forms.get( "{0}", "").strip()
        """.format(campo["nombre"] )
        if tipo != "BOOLEAN" and obligatorio == "1":
            contenido += """
    if len(objeto["{0}"]) == 0:
        abort(500, "{0} es requerido")
""".format(campo["nombre"] )
        if tipo == "BOOLEAN":
            contenido += """
    objeto["{0}"] = objeto["{0}"] == "1"
""".format(campo["nombre"] )
        elif tipo in ["INTEGER", "LONG"]:
            contenido+="""
    try:
        objeto["{0}"] = int( objeto["{0}"] )
    except:
        abort( 500, "El valor de {0} no es válido")
""".format( campo["nombre"] )
        elif tipo in ["REAL", "DECIMAL", "FLOAT", "DOUBLE"]:
            contenido+="""
    try:
        objeto["{0}"] = float( objeto["{0}"] )
    except:
        abort( 500, "El valor de {0} no es válido")
""".format( campo["nombre"])
        elif tipo == "STRING":
            contenido+="""
    if len(objeto["{0}"]) > {1}:
        abort( 500, "El tamaño de {1} excede el permitido")
""".format( campo["nombre"], tamano)
    contenido += """
    transaccionar({0}s.actualizar, objeto)
""".format( entidad["nombre"] )
    contenido += """
    return objeto

CONFIG['rutas'].append({0})
""".format("{'ruta':'/api/" + entidad['nombre'].lower() + "s/<id_" + entidad['nombre'].lower() + ">', 'metodos':['GET','POST'], 'funcion': servir_api_get_" + entidad['nombre'].lower() + "_byid }")
    return contenido

def generar_servir_page_get_entidad_byid(entidad, modelo):
    es_entidad_usuario = esEntidadUsuario(modelo,entidad['idObjeto'])
    entidadesDetalle = entidad["__listas"]["EntidadesDetalle"]
    recuperacionDetalles = ""
    for entidadDetalle in entidadesDetalle:
        recuperacionDetalles += """
    {0}s = {1}s.getNamedQuery( conexion, "findBy{2}", {3} )
""".format(entidadDetalle["nombre"].lower(), entidadDetalle["nombre"], entidad["nombre"], "{'id_" + entidad["nombre"].lower() + "':objeto['id']}" )
    contenido = """
def servir_page_get_{0}_byid(id_{0}):    
""".format(entidad['nombre'].lower())
    if es_entidad_usuario:
        contenido += """
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    objeto, id_user_owner = {0}_getowner(conexion, id_{0})
    if objeto is None:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )    
    if usuario['id'] != id_user_owner:
        conexion.close()
        abort( 403, "Acceso no autorizado") 
    {2}
    conexion.close()
    return template("{1}/show_{0}", objeto = objeto, usuario = usuario {3})
""".format(entidad['nombre'].lower() , get_filename_modelo(modelo) , recuperacionDetalles , "".join([ ", " + x['nombre'].lower() + "s = " + x['nombre'].lower() + "s" for x in entidadesDetalle]) )
    else:
        contenido += """
    conexion = orm.Conexion(PATH_BDD)
    objeto = {0}s.getNamedQuery(conexion, 'findById', {1})
    if len(objeto) == 0:
        conexion.close()
        abort( 404, "El recurso solicitado no existe" )
    objeto = objeto[0]
    {3}
    conexion.close()
    return template("{2}/show_{0}", objeto = objeto {4})
""".format( entidad['nombre'] , "{'id': id_"+entidad['nombre'].lower()+"}", get_filename_modelo(modelo), recuperacionDetalles, "".join([ ", " + x['nombre'].lower() + "s = " + x['nombre'].lower() + "s" for x in entidadesDetalle]) )
    contenido += """
CONFIG['rutas'].append({0})
""".format("{'ruta':'/" + entidad['nombre'].lower() + "s/<id_" + entidad['nombre'].lower() + ">', 'metodos':['GET'], 'funcion': servir_page_get_" + entidad['nombre'].lower() + "_byid }")
    return contenido

def generar_servir_api_get_entidad_lista(entidad, modelo):
    es_entidad_usuario = esEntidadUsuario(modelo,entidad['idObjeto'])
    maestro = getObjetoPadre(modelo, entidad['idObjeto']) if entidad['idJerarquia'] == 'EntidadesDetalle' else None
    contenido = ""
    if maestro is None:
        contenido += """
def servir_api_get_{0}_lista():
""".format(entidad['nombre'].lower())
    else:
        contenido += """
def servir_api_get_{0}_lista( id_{1} ):
""".format(entidad['nombre'].lower(), maestro['nombre'].lower())
    contenido += "    conexion = orm.Conexion(PATH_BDD)\n"
    if es_entidad_usuario:
        contenido += """
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    
"""
    contenido += "    conexion = orm.Conexion(PATH_BDD)\n"
    if maestro is None and es_entidad_usuario :
        contenido += "\n    lista = {0}s.getNamedQuery(conexion, 'findByUser', {1})\n".format(entidad['nombre'], "{'id_user':usuario['id']}")
    elif maestro is None and not es_entidad_usuario :
        contenido += "\n    lista = {0}s.getNamedQuery(conexion, 'findAll', {1})\n".format(entidad['nombre'], repr({}))
    elif maestro is not None and es_entidad_usuario :
        contenido += """
    maestro, id_user_maestro = {0}_getowner(conexion, id_{0})
    if maestro is None:
        conexion.close()
        abort(404, "No existe registro maestro")
    if usuario['id'] != id_user_maestro:
        conexion.close()
        abort(403, "Acceso Denegado")
    lista = {1}s.getNamedQuery(conexion, 'findBy{2}', {3})
""".format(maestro['nombre'].lower(), entidad['nombre'], maestro['nombre'], "{'id_" + maestro['nombre'].lower() + "':id_" + maestro['nombre'].lower() + "}")
    elif maestro is not None and not es_entidad_usuario :
        contenido += """
    maestro = {0}s.getNamedQuery(conexion, 'findById', {1})
    if maestro is None:
        conexion.close()
        abort(404, "No existe registro maestro")
    lista = {2}s.getNamedQuery(conexion, 'findBy{0}', {3})
""".format(maestro['nombre'], "{'id':id_" + maestro['nombre'].lower() + "}", entidad['nombre'], "{'id_" + maestro['nombre'].lower() + "':id_" + maestro['nombre'].lower() + "}")
    contenido += """
    conexion.close()
    return {"lista":lista}
"""
    if maestro is None:
        contenido += """
CONFIG['rutas'].append({0})
""".format("{'ruta':'/api/" + entidad['nombre'].lower() + "s', 'metodos':['GET'], 'funcion': servir_api_get_" + entidad['nombre'].lower() + "_lista }")
    else:
        contenido += """
CONFIG['rutas'].append({0})
""".format("{'ruta':'/api/" + maestro['nombre'].lower() + "s/<id_" + maestro['nombre'].lower() + ">/" + entidad['nombre'].lower() + "s', 'metodos':['GET'], 'funcion': servir_api_get_" + entidad['nombre'].lower() + "_lista }")
    return contenido
    
def generar_servir_page_get_entidad_lista(entidad, modelo):
    es_entidad_usuario = esEntidadUsuario(modelo,entidad['idObjeto'])
    maestro = getObjetoPadre(modelo, entidad['idObjeto']) if entidad['idJerarquia'] == 'EntidadesDetalle' else None
    contenido = ""
    if maestro is None:
        contenido += """
def servir_page_get_{0}_lista():
""".format(entidad['nombre'].lower())
    else:
        contenido += """
def servir_page_get_{0}_lista( id_{1} ):
""".format(entidad['nombre'].lower(), maestro['nombre'].lower())
    contenido += "    conexion = orm.Conexion(PATH_BDD)\n"
    contenido += """
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    
"""
    contenido += "    conexion = orm.Conexion(PATH_BDD)\n"
    if maestro is None and es_entidad_usuario :
        contenido += """
    lista = {0}s.getNamedQuery(conexion, 'findByUser', {1})
""".format(entidad['nombre'], "{'id_user':usuario['id']}")
    elif maestro is None and not es_entidad_usuario :
        contenido += """
    lista = {0}s.getNamedQuery(conexion, 'findAll', {1})""".format(entidad['nombre'], repr({}))
    elif maestro is not None and es_entidad_usuario :
        contenido += """
    maestro, id_user_maestro = {0}_getowner(conexion, id_{0})
    if maestro is None:
        conexion.close()
        abort(404, "No existe registro maestro")
    if usuario['id'] != id_user_maestro:
        conexion.close()
        abort(403, "Acceso Denegado")
    lista = {1}s.getNamedQuery(conexion, 'findBy{2}', {3})
""".format(maestro['nombre'].lower(), entidad['nombre'], maestro['nombre'], "{'id_" + maestro['nombre'].lower() + "':id_" + maestro['nombre'].lower() + "}")
    elif maestro is not None and not es_entidad_usuario :
        contenido += """
    maestro = {0}s.getNamedQuery(conexion, 'findById', {1})
    if maestro is None:
        conexion.close()
        abort(404, "No existe registro maestro")
    lista = {0}s.getNamedQuery(conexion, 'findBy{1}', {2})
""".format(maestro['nombre'], "{'id':id_" + maestro['nombre'].lower() + "}", entidad['nombre'], "{'id_" + maestro['nombre'].lower() + "':id_" + maestro['nombre'].lower() + "}")
    contenido += """
    conexion.close()
"""
    if maestro is None:
        contenido += """
    return template("{1}/listar_{2}", lista = lista, usuario = usuario)
    
CONFIG['rutas'].append({0})
""".format("{'ruta':'/" + entidad['nombre'].lower() + "s', 'metodos':['GET'], 'funcion': servir_page_get_" + entidad['nombre'].lower() + "_lista }", get_filename_modelo(modelo), entidad['nombre'] )
    else:
        contenido += """
    return template("{1}/listar_{2}", maestro = maestro, lista = lista, usuario = usuario)
    
CONFIG['rutas'].append({0})
""".format("{'ruta':'/" + maestro['nombre'].lower() + "s/<id_" + maestro['nombre'].lower() + ">/" + entidad['nombre'].lower() + "s', 'metodos':['GET'], 'funcion': servir_page_get_" + entidad['nombre'].lower() + "_lista }", get_filename_modelo(modelo), entidad['nombre'])
    return contenido
    
def generar_archivos_entidad(entidad, modelo):
    nombreModulo = get_filename_modelo(modelo)
    maestro = getObjetoPadre(modelo, entidad['idObjeto']) if entidad['idJerarquia'] == 'EntidadesDetalle' else None
    resultado = [
        {'path' : 'views/{0}/show_{1}.tpl'.format(nombreModulo, entidad["nombre"]), "contenido": generar_view_show_entidad(entidad, modelo) },
        {'path' : 'views/{0}/editar_{1}.tpl'.format(nombreModulo,entidad["nombre"]), "contenido": generar_view_editar_entidad(entidad, modelo) },
    ]
    if maestro is None:
        resultado.append({'path' : 'views/{0}/listar_{1}.tpl'.format(nombreModulo, entidad["nombre"]), "contenido": generar_view_listar_entidad(entidad, modelo) } )
    return resultado
    
def generar_view_show_entidad(entidad, modelo):
    nombreModulo = get_filename_modelo(modelo)
    
    campos = entidad['__listas']['Campos']
    camposPk = [x for x in campos if x['__atributos']['pk'] == '1' ]
    namedQueries = entidad['__listas']['NamedQuieries']
    entidadesDetalle = entidad["__listas"]["EntidadesDetalle"]

    campoOrden = [x for x in campos if x['nombre'] == 'orden']    
    if len(campoOrden) == 0:
        campoOrden = None
    else:
        campoOrden = campoOrden[0]
    maestro = getObjetoPadre(modelo, entidad['idObjeto']) if entidad['idJerarquia'] == 'EntidadesDetalle' else None
    
    contenido = """% include('{0}/encabezado.tpl', titulo="{1}", usuario = usuario, estilo = "")
""".format(nombreModulo, entidad["nombre"])
    for campo in campos:
        contenido += """
<div class="row">
    <span class="col">
        {0}:
    </span>
    <span class="col">
        {1}
    </span>
</div>
""".format(campo["nombre"], "{{objeto['" + campo["nombre"] +"']}}")
    
    # perfila listados de entidades detalle
    listas_detalles = ""
    if len(entidadesDetalle) > 0:
        listas_detalles = """
    <ul class="mt-3 nav nav-tabs nav-justified">
"""
        for indice, entidadDetalle in enumerate(entidadesDetalle):
            listas_detalles += """
        <li class="nav-item">
            <a class="nav-link {es_active}" data-bs-toggle="tab" href="#div{nombre_entidad}s">{nombre_entidad}s</a>
        </li>
""".format(es_active = "active" if indice == 0 else "", nombre_entidad = entidadDetalle['nombre'])
        listas_detalles += """
    </ul>
    <div class="tab-content">    
"""
        for indice, entidadDetalle in enumerate(entidadesDetalle):
            camposEntidadDetalle = [ x for x in entidadDetalle['__listas']['Campos'] if x['__atributos']['tipo'] not in ['BLOB']]
            listas_detalles += """
        <div class="tab-pane container {es_active}" id="div{nombre_entidad}s">
            <table class="mt-2 table table-striped">
                <thead>
                    <tr>
""".format(es_active = "active" if indice == 0 else "fade", nombre_entidad = entidadDetalle['nombre'])
            for campoEntidadDetalle in camposEntidadDetalle:
                listas_detalles += """
                        <th>
                            {nombre_campo}
                        </th>
""".format(nombre_campo = campoEntidadDetalle['nombre'][0].upper() + campoEntidadDetalle['nombre'][1:])
            listas_detalles += """
                        <th>
                            <a class="btn btn-primary" href="{href}">Crear Nuevo</a>
                        </th>
                    </tr>
                </thead>
                <tbody>
% if len({nombre_entidad}s) == 0:
                    <tr>
                        <td colspan="{numero_campos}">
                            No hay registros disponibles
                        </td>
                    </tr>
% end
% for {nombre_entidad} in {nombre_entidad}s:
                    <tr>""".format(nombre_entidad = entidadDetalle['nombre'].lower(), numero_campos = len(camposEntidadDetalle), href = "/" + nombreModulo + "/" + entidad['nombre'].lower() + "s/{{objeto['id']}}/nuevo" + entidadDetalle['nombre'].lower() )
            for campoEntidadDetalle in camposEntidadDetalle:
                listas_detalles += """
                        <td>{expresion_campo}</td>""".format(expresion_campo = "{{" + entidadDetalle['nombre'].lower() + "['" + campoEntidadDetalle['nombre'] + "']}}")
            listas_detalles += """
                        <td>
                            <a class="btn btn-primary" href = "/{nombre_modulo}/{nombre_entidad}s/{especificacion_id}">Mostrar</a>
                        </td>
                    </tr>
% end
                </tbody>
            </table>
        </div>""".format(nombre_modulo = nombreModulo, nombre_entidad = entidadDetalle['nombre'].lower(), especificacion_id = "{{" + entidadDetalle['nombre'].lower() + "['id']}}")
        listas_detalles += """
    </div>    
"""
    contenido += """
    <div class="d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="/{nombre_modulo}/{nombre_entidad_lower}">
            Volver
        </a>
        <a class="btn btn-primary" href="/{nombre_modulo}/{parametro}/editar">
            Editar
        </a>
        <a class="btn btn-secondary" href="/{nombre_modulo}/{parametro}/eliminar" onclick="return confirm('Desea proceder con eliminación?');">
            Eliminar
        </a>
    </div>
{listas_detalles}
% include('{nombre_modulo}/pie.tpl', usuario = usuario)
""".format(nombre_modulo = nombreModulo, nombre_entidad_lower = maestro["nombre"].lower() + "s/{{objeto['id_" + maestro["nombre"].lower() + "']}}" if maestro is not None else entidad["nombre"].lower() + "s",
           parametro = entidad['nombre'].lower() + "s/{{objeto['id']}}" , listas_detalles = listas_detalles)

    return contenido
    
def generar_view_listar_entidad(entidad, modelo):
    nombreModulo = get_filename_modelo(modelo)
    campos = [x for x in entidad['__listas']['Campos'] if x['__atributos']['tipo'] not in ['BLOB'] ]
    campoNombre = [x for x in campos if x['__atributos']['displayName'] == '1']
    if len(campoNombre) == 0:
        campoNombre = campos[1]
    else:
        campoNombre = campoNombre[0]

    contenido = """% include('{nombreModulo}/encabezado.tpl', titulo="{nombre_entidad}s", usuario = usuario, estilo = "")
<table class="table table-striped">
    <thead>
    <tr>""".format(nombreModulo = nombreModulo, nombre_entidad = entidad["nombre"] )
    for campo in campos:
        contenido += "        <th>{nombre_campo}</th>\n".format(nombre_campo = campo['nombre'][0].upper() + campo['nombre'][1:] )
    contenido += """
        <th>Mover</th>
        <th>
            <a class="btn btn-primary" href=\"/""" + nombreModulo + "/" + entidad["nombre"].lower() + "s/nuevo" + """\">Crear Nuevo</a>
        </th>
    </tr>
    </thead>
    <tbody>
% if len(lista) == 0:
    <tr>
    <td colspan = \"""" + str(len(campos)) + """\">No se ha encontrado registros</td>
    </tr>
% end
% for objeto in lista:
    <tr>"""
    for campo in campos:
        contenido += """
        <td>
            {expresion_campo}
        </td>""".format(expresion_campo = "{{objeto['" + campo['nombre'] + "']}}" )
    contenido += """
        <td></td>
        <td>
            <a class="btn btn-primary" href="{href}">Mostrar</a>
        </td>
    </tr>
% end
    </tbody>
</table>
% include('{nombreModulo}/pie.tpl', usuario = usuario)
""".format(nombreModulo = nombreModulo, href = "/" + nombreModulo + "/" + entidad["nombre"].lower() + "s/{{objeto['id']}}" )
    return contenido
    
def generar_view_editar_entidad(entidad, modelo):
    nombreModulo = get_filename_modelo(modelo)
    
    campos = entidad['__listas']['Campos']
    camposPk = [x for x in campos if x['__atributos']['pk'] == '1' ]
    namedQueries = entidad['__listas']['NamedQuieries']
    
    campoOrden = [x for x in campos if x['nombre'] == 'orden']    
    if len(campoOrden) == 0:
        campoOrden = None
    else:
        campoOrden = campoOrden[0]
    maestro = getObjetoPadre(modelo, entidad['idObjeto']) if entidad['idJerarquia'] == 'EntidadesDetalle' else None
    
    contenido = """% include('{nombreModulo}/encabezado.tpl', titulo="Datos de {nombre_entidad}", usuario = usuario, estilo = "")
% if lvl != "" :
<div class="alert alert-{lvl}">
    {mensaje}
</div>
% end
<form method="POST" enctype="multipart/form-data">
""".format(nombreModulo = nombreModulo, nombre_entidad = entidad["nombre"], lvl="{{lvl}}", mensaje = "{{mensaje}}")

    for campo in campos:
        if campo["__atributos"]["pk"] == "1" or campoOrden is not None and campo["nombre"] == campoOrden["nombre"]:
            continue
        # mis_fk = [x for x in namedQueries if ]
        contenido +="""
<div class="row">
    <label class="col form-label" for="{0}">
    {0}{1}:
    </label>
""".format(campo["nombre"], "*" if campo["__atributos"]["obligatorio"] == "1" else "")
        if campo["__atributos"]["tipo"] == "STRING":
            contenido +="""
    <span class="col">
        <input class="form-control" type="text" name="{0}" value="{1}" maxlength="{2}">
    </span>
""".format(campo["nombre"], "{{objeto['" + campo["nombre"] + "']}}", campo["__atributos"]["tamano"])
        elif campo["__atributos"]["tipo"] == "EMAIL":
            contenido +="""
    <span class="col">
        <input class="form-control" type="email" name="{0}" value="{1}" maxlength="{2}">
    </span>
""".format(campo["nombre"], "{{objeto['" + campo["nombre"] + "']}}", campo["__atributos"]["tamano"])
        elif campo["__atributos"]["tipo"] in ["INTEGER", "LONG", "REAL", "DECIMAL"]:
            contenido += """
<span class="col">
        <input class="form-control" type="number" name="{0}" value="{1}" maxlength="{2}">
    </span>
""".format(campo["nombre"], "{{objeto['" + campo["nombre"] + "']}}", campo["__atributos"]["tamano"])
        elif campo["__atributos"]["tipo"] == "BLOB":
            contenido +="""
    <span class="col">
        <input class="form-control" type="file" name="{0}">
    </span>
""".format(campo["nombre"])
        elif campo["__atributos"]["tipo"] == "BOOLEAN":
            contenido +="""
    <span class="col">
        <input class="form-check form-switch" type="checkbox" name="{0}" value="1">
    </span>
""".format(campo["nombre"])
        elif campo["__atributos"]["tipo"] == "DATE":
            contenido +="""
    <span class="col">
        <input class="form-control" type="date" name="{0}" value="{1}" >
    </span>
""".format(campo["nombre"], "{{fecha_iso_to_js(objeto['" + campo['nombre'] + "'])}}" )
        elif campo["__atributos"]["tipo"] == "DATETIME":
            contenido +="""
    <span class="col">
        <input class="form-control" type="datetime-local" name="{0}" value="{1}" >
    </span>
""".format(campo["nombre"], "{{fecha_iso_to_js(objeto['" + campo['nombre'] + "'])}}" )
        contenido +="""
</div>
"""
    contenido += """
    <div class="mt-5 d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="{ruta_cancelar}">
            Cancelar
        </a>
        <input type="submit" value="Guardar" class="btn btn-primary">
    </div>
</form>
% include('{nombre_modulo}/pie.tpl', usuario = usuario)
""".format(nombre_modulo = nombreModulo , ruta_cancelar = "{{ruta_cancelar}}" )
    return contenido
    
def generar_servir_api_insertar_entidad( entidad, modelo):
    nombreTabla = entidad['__atributos']['nombreTabla']
    campos = entidad['__listas']['Campos']
    camposPk = [x for x in campos if x['__atributos']['pk'] == '1' ]
    namedQueries = entidad['__listas']['NamedQuieries']
    campos = [x for x in campos if x["__atributos"]["insert"] == "1" ]
    campoOrden = [x for x in campos if x['nombre'] == 'orden']    
    if len(campoOrden) == 0:
        campoOrden = None
    else:
        campoOrden = campoOrden[0]

    if len(camposPk) > 0:
        namedQueries = namedQueries + [{'nombre':'findById', '__listas':{'camposWhere':[{'nombre':x['nombre'] for x in camposPk}]} }]

    findAll_generado = False

    if 'entidadUsuario' in entidad['__atributos'].keys() and entidad['__atributos']['entidadUsuario'] == '1':
        campos = campos + [{'nombre':'id_user' , '__atributos':{ 'nombreCampo':'ID_USER', 'tipo': 'INTEGER', 'tamano': 0, 'precision': 0, 'obligatorio':True, 'incremental':False } }]
        namedQueries = namedQueries + [{'nombre':'findByUser', '__listas':{'camposWhere':[{'nombre':'id_user'}]} }]
        if campoOrden is not None:
            namedQueries[-1]['__listas']['camposOrderBy'] = [{'nombre':'orden'}]
        findAll_generado = True

    maestro = getObjetoPadre(modelo, entidad['idObjeto']) if entidad['idJerarquia'] == 'EntidadesDetalle' else None
    if maestro is not None:
        id_maestro = "id_" + maestro['nombre'].lower()
        fk_maestro = "FK_{0}_{1}".format( nombreTabla.upper(), maestro['nombre'].upper() ) 
        campos = campos + [{'nombre':id_maestro , '__atributos':{ 'nombreCampo':id_maestro.upper(), 'tipo': 'INTEGER', 'tamano': 0, 'precision': 0, 'obligatorio':True, 'incremental':False } }]
        namedQueries = namedQueries + [{'nombre':'findBy' + maestro['nombre'] , '__listas': {'camposWhere':[{'nombre':id_maestro}]} }]
        if campoOrden is not None:
            namedQueries[-1]['__listas']['camposOrderBy'] = [{'nombre':'orden'}]
        print("Se incorpora {0} a campos de {1}".format(id_maestro, entidad['nombre'])) 
        findAll_generado = True
    
    if not findAll_generado:
        namedQueries = namedQueries + [{'nombre':'findAll' , '__listas': {} }]
        if campoOrden is not None:
            namedQueries[-1]['__listas']['camposOrderBy'] = [{'nombre':'orden'}]
    contenido = """
def servir_api_insertar_{nombre_entidad_lower}():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )    
    {nombre_entidad_lower} = {parentesis}
""".format(nombre_entidad_lower = entidad["nombre"].lower(), nombre_entidad = entidad["nombre"], parentesis ="{}")
    # lee cada campo y valida que su presencia si es obligatorio
    for campo in campos:
        
        for atributo in ['tipo', 'tamano', 'obligatorio']:
            assert atributo in campo["__atributos"].keys(), "Campo {0}.{1} no tiene atributo {2}".format(entidad['nombre'], campo['nombre'], atributo)
        tipo = campo["__atributos"]["tipo"]
        tamano = campo["__atributos"]["tamano"]
        # precision = campo["__atributos"]["precision"]
        obligatorio = campo["__atributos"]["obligatorio"]
        if tipo == "BLOB":
            contenido += """
    file_{1} = request.files.get("{1}")
    filename_{1} = file_{1}.filename
    temppath_{1} = join( dirname(abspath(__file__)), "upload", filename_{1} )
    if not exists( dirname(temppath_{1}) ):
        makedirs( dirname(temppath_{1}) )
    file_{1}.save(temppath_{1})
    with open( temppath_{1} , 'rb' ) as stream_{1}:
        {0}["{1}"] = stream_{1}.read()
    remove_file(temppath_{1})
""".format(entidad["nombre"].lower(), campo["nombre"])    
            continue
        contenido += """
    {1}["{0}"] = request.forms.get( "{0}", "").strip()
        """.format(campo["nombre"], entidad["nombre"].lower() )
        if tipo != "BOOLEAN" and obligatorio == "1":
            contenido += """
    if len({1}["{0}"]) == 0:
        abort(500, "{0} es requerido")
""".format(campo["nombre"], entidad["nombre"].lower() )
        if tipo == "BOOLEAN":
            contenido += """
    {1}["{0}"] = {1}["{0}"] == "1"
""".format(campo["nombre"], entidad["nombre"].lower() )
        elif tipo in ["INTEGER", "LONG"]:
            contenido+="""
    try:
        {0}["{1}"] = int( {0}["{1}"] )
    except:
        abort( 500, "El valor de {1} no es válido")
""".format( entidad["nombre"].lower(), campo["nombre"])
        elif tipo in ["REAL", "DECIMAL", "FLOAT", "DOUBLE"]:
            contenido+="""
    try:
        {0}["{1}"] = float( {0}["{1}"] )
    except:
        abort( 500, "El valor de {1} no es válido")
""".format( entidad["nombre"].lower(), campo["nombre"])
        elif tipo == "STRING":
            contenido+="""
    if len({0}["{1}"]) > {2}:
        abort( 500, "El tamaño de {1} excede el permitido")
""".format( entidad["nombre"].lower(), campo["nombre"], tamano)
        elif tipo in ["DATE", "DATETIME"]:
            contenido+="""
    try:
        if len({0}["{1}"]) > 0:
            {0}["{1}"] = fecha_js_to_iso({0}["{1}"])
    except:
        abort( 500, "{1} no es una fecha válida")
""".format( entidad["nombre"].lower(), campo["nombre"], tamano)
    contenido += """
    transaccionar({0}s.insertar, {1})
    return {1}
""".format( entidad["nombre"], entidad["nombre"].lower() )
    contenido += """
CONFIG['rutas'].append({0})
""".format("{'ruta':'/api/" + entidad['nombre'].lower() + "s/nuevo', 'metodos':['POST'], 'funcion': servir_api_insertar_" + entidad['nombre'].lower() + " }")
    return contenido

def generar_servir_page_insertar_entidad(entidad, modelo):
    nombre_modelo = get_filename_modelo(modelo)
    campos = entidad['__listas']['Campos']
    camposPk = [x for x in campos if x['__atributos']['pk'] == '1' ]
    namedQueries = entidad['__listas']['NamedQuieries']
    campos = [x for x in campos if x["__atributos"]["insert"] == "1" ]
    campoOrden = [x for x in campos if x['nombre'] == 'orden']    
    entidadUsuario = esEntidadUsuario(modelo, entidad['idObjeto'])
    if len(campoOrden) == 0:
        campoOrden = None
    else:
        campoOrden = campoOrden[0]
    maestro = getObjetoPadre(modelo, entidad['idObjeto']) if entidad['idJerarquia'] == 'EntidadesDetalle' else None
    
    ruta_cancelar = "\"/{nombre_modelo}/{nombre_entidad_lower}s\"".format(nombre_modelo = nombre_modelo, nombre_entidad_lower = entidad['nombre'].lower() )
    if maestro is not None:
        ruta_cancelar = "\"/{nombre_modelo}/{nombre_maestro_lower}s/\" + str(id_{nombre_maestro_lower})".format(nombre_modelo = nombre_modelo, nombre_maestro_lower = maestro['nombre'].lower() )
    
    contenido = ""
    if maestro is None:
        contenido = """
def servir_page_insertar_{nombre_entidad}():
""".format(nombre_entidad = entidad['nombre'].lower() )
    else:
        contenido = """
def servir_page_insertar_{nombre_entidad}(id_{nombre_maestro}):
""".format(nombre_entidad = entidad['nombre'].lower(), nombre_maestro = maestro['nombre'].lower() )
    
    contenido +="""
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )
"""
    if maestro is not None and entidadUsuario:
        contenido += """
    conexion = orm.Conexion(PATH_BDD)
    {nombre_maestro}, id_usuario_owner = {nombre_maestro}_getowner( conexion , id_{nombre_maestro})
    conexion.close()
    if {nombre_maestro} is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
""".format(nombre_maestro = maestro['nombre'].lower() )
    contenido += """
    {nombre_entidad_lower} = {nombre_entidad}s.nuevoDiccionario()
    if request.method == "GET":        
        return template("{nombre_modelo}/editar_{nombre_entidad}", objeto = {nombre_entidad_lower}, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = {ruta_cancelar}, fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []
""".format(nombre_entidad = entidad['nombre'], nombre_entidad_lower = entidad['nombre'].lower(),nombre_modelo = nombre_modelo, id_objeto = "{{" + entidad['nombre'].lower() + "['id']}}", ruta_cancelar = ruta_cancelar)
    if maestro is not None:
        contenido += """
    {nombre_entidad_lower}['id_{nombre_maestro_lower}'] = id_{nombre_maestro_lower}
""".format( nombre_entidad_lower = entidad['nombre'].lower(), nombre_maestro_lower = maestro['nombre'].lower() )
    if entidad['__atributos']['entidadUsuario'] == "1":
        contenido += """
    {nombre_entidad_lower}['id_user'] = usuario['id']
""".format( nombre_entidad_lower = entidad['nombre'].lower() )
    for campo in campos:
        if campo['__atributos']['pk'] == "1" or campo['nombre'] == 'orden':
            continue
        tipo = campo["__atributos"]["tipo"]
        tamano = campo["__atributos"]["tamano"]
        # precision = campo["__atributos"]["precision"]
        obligatorio = campo["__atributos"]["obligatorio"]

        if tipo == "BLOB":
            contenido += """
    file_{1} = request.files.get("{1}")
    filename_{1} = file_{1}.filename
    temppath_{1} = join( dirname(abspath(__file__)), "upload", filename_{1} )
    if not exists( dirname(temppath_{1}) ):
        makedirs( dirname(temppath_{1}) )
    file_{1}.save(temppath_{1})
    with open( temppath_{1} , 'rb' ) as stream_{1}:
        {0}["{1}"] = stream_{1}.read()
    remove_file(temppath_{1})
""".format(entidad["nombre"].lower(), campo["nombre"])    
            continue
        contenido += """
    {1}["{0}"] = request.forms.get( "{0}", "").strip()
        """.format(campo["nombre"], entidad["nombre"].lower() )
        if tipo != "BOOLEAN" and obligatorio == "1":
            contenido += """
    if len({1}["{0}"]) == 0:
        mensajes_error.append("{0} es requerido")
""".format(campo["nombre"], entidad["nombre"].lower() )
        if tipo == "BOOLEAN":
            contenido += """
    {1}["{0}"] = {1}["{0}"] == "1"
""".format(campo["nombre"], entidad["nombre"].lower() )
        elif tipo in ["INTEGER", "LONG"]:
            contenido+="""
    try:
        {0}["{1}"] = int( {0}["{1}"] )
    except:
        mensajes_error.append("El valor de {1} no es válido")
""".format( entidad["nombre"].lower(), campo["nombre"])
        elif tipo in ["REAL", "DECIMAL", "FLOAT", "DOUBLE"]:
            contenido+="""
    try:
        {0}["{1}"] = float( {0}["{1}"] )
    except:
        mensajes_error.append("El valor de {1} no es válido")
""".format( entidad["nombre"].lower(), campo["nombre"])
        elif tipo == "STRING":
            contenido+="""
    if len({0}["{1}"]) > {2}:
        mensajes_error.append("El tamaño de {1} excede el permitido")
""".format( entidad["nombre"].lower(), campo["nombre"], tamano)
    contenido += """
    if len(mensajes_error) > 0:
        return template("{nombre_modelo}/editar_{nombre_entidad}", objeto = {nombre_entidad_lower}, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = {ruta_cancelar}, fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar({nombre_entidad}s.insertar, {nombre_entidad_lower})
    except:
        return template("{nombre_modelo}/editar_{nombre_entidad}", objeto = {nombre_entidad_lower}, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = {ruta_cancelar}, fecha_iso_to_js = fecha_iso_to_js )
    return template("xpd_usr/mensaje", lvl = "success", mensaje = "Operación realizada Exitosamente.", href ="/{nombre_modelo}/{nombre_entidad_lower}s/" + str({nombre_entidad_lower}['id']) )
""".format( nombre_entidad = entidad["nombre"], nombre_entidad_lower = entidad["nombre"].lower(), nombre_modelo = nombre_modelo, id_objeto = "{{" + entidad['nombre'].lower() + "['id']}}", ruta_cancelar = ruta_cancelar )
    if maestro is None:
        contenido += """
CONFIG['rutas'].append({0})
""".format("{'ruta':'/" + entidad['nombre'].lower() + "s/nuevo', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_" + entidad['nombre'].lower() + " }")
    else:
        contenido += """
CONFIG['rutas'].append({0})
""".format("{'ruta':'/" + maestro['nombre'].lower() + "s/<id_" + maestro['nombre'].lower() + ">/nuevo" + entidad['nombre'].lower() + "', 'metodos':['GET','POST'], 'funcion': servir_page_insertar_" + entidad['nombre'].lower() + " }")
    return contenido

def generar_servir_page_editar_entidad(entidad, modelo):
    nombre_modelo = get_filename_modelo(modelo)
    campos = entidad['__listas']['Campos']
    camposPk = [x for x in campos if x['__atributos']['pk'] == '1' ]
    namedQueries = entidad['__listas']['NamedQuieries']
    campos_update = [x for x in campos if x["__atributos"]["update"] == "1" ]
    campoOrden = [x for x in campos if x['nombre'] == 'orden']    
    entidadUsuario = esEntidadUsuario(modelo, entidad['idObjeto'])
    if len(campoOrden) == 0:
        campoOrden = None
    else:
        campoOrden = campoOrden[0]
    maestro = getObjetoPadre(modelo, entidad['idObjeto']) if entidad['idJerarquia'] == 'EntidadesDetalle' else None
    
    ruta_cancelar = "\"/{nombre_modelo}/{nombre_entidad_lower}s/\" + str({nombre_entidad_lower}['id'])".format(nombre_modelo = nombre_modelo, nombre_entidad_lower = entidad['nombre'].lower() )
    
    contenido = """
def servir_page_editar_{nombre_entidad}(id):
    usuario = xpd_usr.getCurrentUser(request)
""".format(nombre_entidad = entidad['nombre'].lower() )
    if esEntidadUsuario:
        contenido += """
    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    conexion = orm.Conexion(PATH_BDD)
    {nombre_entidad_lower}, id_usuario_owner = {nombre_entidad_lower}_getowner( conexion , id)
    conexion.close()
    if {nombre_entidad_lower} is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado" )
""".format(nombre_entidad_lower = entidad['nombre'].lower() )
    else:
        contenido += """
    if 'Administrador' not in usuario['roles']:
        abort(403,"Acceso Denegado")
    conexion = orm.Conexion(PATH_BDD)
    {nombre_entidad_lower} = {nombre_entidad}s.getNamedQuery( conexion, 'findById', {expresion_id})
    conexion.close()
    if len({nombre_entidad_lower}) == 0:
        abort(403, "Objeto no encontrado")
    {nombre_entidad_lower} = {nombre_entidad_lower}[0]
""".format( nombre_entidad_lower = entidad['nombre'].lower(), nombre_entidad = entidad['nombre'], expresion_id = "{ 'id' : id }" )
    contenido += """    
    if request.method == "GET":        
        return template("{nombre_modelo}/editar_{nombre_entidad}", objeto = {nombre_entidad_lower}, usuario = usuario, lvl = "", mensaje = "", ruta_cancelar = {ruta_cancelar}, fecha_iso_to_js = fecha_iso_to_js)
    # A partir de este punto se asume POST
    mensajes_error = []
""".format(nombre_entidad = entidad['nombre'], nombre_entidad_lower = entidad['nombre'].lower(),nombre_modelo = nombre_modelo, id_objeto = "{{" + entidad['nombre'].lower() + "['id']}}", ruta_cancelar = ruta_cancelar)
    for campo in campos:
        if campo['__atributos']['pk'] == "1" or campo['nombre'] == 'orden':
            continue
        tipo = campo["__atributos"]["tipo"]
        tamano = campo["__atributos"]["tamano"]
        # precision = campo["__atributos"]["precision"]
        obligatorio = campo["__atributos"]["obligatorio"]

        if tipo == "BLOB":
            contenido += """
    file_{1} = request.files.get("{1}")
    filename_{1} = file_{1}.filename
    temppath_{1} = join( dirname(abspath(__file__)), "upload", filename_{1} )
    if not exists( dirname(temppath_{1}) ):
        makedirs( dirname(temppath_{1}) )
    file_{1}.save(temppath_{1})
    with open( temppath_{1} , 'rb' ) as stream_{1}:
        {0}["{1}"] = stream_{1}.read()
    remove_file(temppath_{1})
""".format(entidad["nombre"].lower(), campo["nombre"])    
            continue
        contenido += """
    {1}["{0}"] = request.forms.get( "{0}", "").strip()
        """.format(campo["nombre"], entidad["nombre"].lower() )
        if tipo != "BOOLEAN" and obligatorio == "1":
            contenido += """
    if len({1}["{0}"]) == 0:
        mensajes_error.append("{0} es requerido")
""".format(campo["nombre"], entidad["nombre"].lower() )
        if tipo == "BOOLEAN":
            contenido += """
    {1}["{0}"] = {1}["{0}"] == "1"
""".format(campo["nombre"], entidad["nombre"].lower() )
        elif tipo in ["INTEGER", "LONG"]:
            contenido+="""
    try:
        {0}["{1}"] = int( {0}["{1}"] )
    except:
        mensajes_error.append("El valor de {1} no es válido")
""".format( entidad["nombre"].lower(), campo["nombre"])
        elif tipo in ["REAL", "DECIMAL", "FLOAT", "DOUBLE"]:
            contenido+="""
    try:
        {0}["{1}"] = float( {0}["{1}"] )
    except:
        mensajes_error.append("El valor de {1} no es válido")
""".format( entidad["nombre"].lower(), campo["nombre"])
        elif tipo == "STRING":
            contenido+="""
    if len({0}["{1}"]) > {2}:
        mensajes_error.append("El tamaño de {1} excede el permitido")
""".format( entidad["nombre"].lower(), campo["nombre"], tamano)
        elif tipo in ["DATE", "DATETIME"]:
            contenido+="""
    try:
        if len({0}["{1}"]) > 0:
            {0}["{1}"] = fecha_js_to_iso({0}["{1}"])
    except:
        mensajes_error.append("{1} no es una fecha válida")
""".format( entidad["nombre"].lower(), campo["nombre"], tamano)
    contenido += """
    if len(mensajes_error) > 0:
        return template("{nombre_modelo}/editar_{nombre_entidad}", objeto = {nombre_entidad_lower}, usuario = usuario, lvl = "danger", mensaje = " / ".join(mensajes_error), ruta_cancelar = {ruta_cancelar}, fecha_iso_to_js = fecha_iso_to_js )    
    try:
        transaccionar({nombre_entidad}s.actualizar, {nombre_entidad_lower})
    except:
        return template("{nombre_modelo}/editar_{nombre_entidad}", objeto = {nombre_entidad_lower}, usuario = usuario, lvl = "danger", mensaje = "Se ha producido un error al guardar la información", ruta_cancelar = {ruta_cancelar}, fecha_iso_to_js = fecha_iso_to_js )
    return template("{nombre_modelo}/editar_{nombre_entidad}", objeto = {nombre_entidad_lower}, usuario = usuario, lvl = "success", mensaje = "Actualizacion ha sido exitosa", ruta_cancelar = {ruta_cancelar}, fecha_iso_to_js = fecha_iso_to_js )
""".format( nombre_entidad = entidad["nombre"], nombre_entidad_lower = entidad["nombre"].lower(), nombre_modelo = nombre_modelo, id_objeto = "{{" + entidad['nombre'].lower() + "['id']}}", ruta_cancelar = ruta_cancelar )
    contenido += """
CONFIG['rutas'].append({0})
""".format("{'ruta':'/" + entidad['nombre'].lower() + "s/<id>/editar', 'metodos':['GET','POST'], 'funcion': servir_page_editar_" + entidad['nombre'].lower() + " }")
    return contenido

def generar_servir_page_main(modelo):
    nombre_modelo = get_filename_modelo(modelo)
    contenido ="""
def servir_page_main():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )
"""
    entidades = [x for x in modelo['__objetoRaiz']['__listas']['Entidades'] if x['__atributos']['entidadUsuario'] == "1" ]
    if len(entidades) == 1:
        contenido += """
    redirect('/{nombre_modelo}/{nombre_entidad}s')    
""".format(nombre_modelo = nombre_modelo, nombre_entidad = entidades[0]['nombre'].lower())
    else:
        contenido += """
    entidades = [
"""
        for entidad in entidades:
            contenido += "         { 'nombre': '" + entidad['nombre'] + "s', 'path':'/"+ nombre_modelo +"/"+ entidad['nombre'].lower() +"s'  },\n"
        contenido += """
    ]
    return template("{nombre_modelo}/main", usuario = usuario, titulo = "{nombre_modelo}", entidades = entidades)
""".format(nombre_modelo=nombre_modelo, nombre_entidad = entidad['nombre'])
    contenido += """
CONFIG['rutas'].append({0})
""".format("{'ruta':'/main', 'metodos':['GET'], 'funcion': servir_page_main }")
    
    return contenido

def generar_servir_page_admin_main(modelo):
    nombre_modelo = get_filename_modelo(modelo)
    contenido ="""
def servir_page_admin_main():
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    if 'Administrador' not in usuario['roles']:
        abort(403,"Acceso Denegado")  
"""
    entidades = [x for x in modelo['__objetoRaiz']['__listas']['Entidades'] if x['__atributos']['entidadUsuario'] != "1" ]
    if len(entidades) == 1:
        contenido += """
    redirect('/{nombre_modelo}/{nombre_entidad}s')    
""".format(nombre_modelo = nombre_modelo, nombre_entidad = entidades[0]['nombre'].lower())
    else:
        contenido += """
    entidades = [
"""
        for entidad in entidades:
            contenido += "         { 'nombre': '" + entidad['nombre'] + "s', 'path':'/"+ nombre_modelo +"/"+ entidad['nombre'].lower() +"s'  },\n"
        contenido += """
    ]
    return template("{nombre_modelo}/main", usuario = usuario, titulo = "Administración", entidades = entidades)
""".format(nombre_modelo=nombre_modelo)
    contenido += """
CONFIG['rutas'].append({0})
""".format("{'ruta':'/admin', 'metodos':['GET'], 'funcion': servir_page_admin_main }")

    return contenido

def generar_view_main_tpl(modelo):
    nombre_modelo = get_filename_modelo(modelo)
    contenido = """% include('{nombre_modelo}/encabezado.tpl', titulo="titulo", usuario = usuario, estilo = "")
<ul class="list-group">
% for entidad in entidades:
<li class="list-group-item">
""".format(nombre_modelo = nombre_modelo)
    contenido += """<a href="{{entidad['path']}}">{{entidad["nombre"]}}</a>
</li>
% end
</ul>
"""
    contenido +="% include('{nombre_modelo}/pie.tpl', usuario = usuario)".format(nombre_modelo = nombre_modelo)
    return contenido

def generar_view_encabezado_tpl(modelo):
    nombre_modelo = get_filename_modelo(modelo)
    entidades = [x for x in modelo['__objetoRaiz']['__listas']['Entidades'] if x['__atributos']['entidadUsuario'] == "1" ]
    contenido = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{titulo}}</title>
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    <script src="/static/js/bootstrap.bundle.min.js"></script>
% if estilo != "" :
    <style>
        {{estilo}}
    </style>
% end
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand fixed-top border-bottom justify-content-between w-100 p-0">
        <a class="navbar-brand ml-5" href="/">{{titulo}}</a>
        <div class="collapse navbar-collapse justify-content-end" id="collapsibleNavbar">
% if usuario:
            <ul class="navbar-nav w-25">"""
    for entidad in entidades:
        contenido += """
                <li class="nav-item">
                    <a class="nav-link" href="/""" + nombre_modelo + "/" + entidad['nombre'].lower() +"""s">
                        """+ entidad['nombre'] + """s
                    </a>    
                </li>
"""
    contenido += """
% if usuario and 'roles' in usuario.keys() and 'Administrador' in usuario['roles']:
                <li class="nav-item">
                    <a class="nav-link" href="/""" + nombre_modelo + """/admin">
                         |Administrar|
                    </a>
                </li>
% end
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        {{usuario['username']}}
                    </a>
                    <ul class="dropdown-menu" id="user_menu">
                        <li><a class="dropdown-item" href="/cambiar_clave">Cambiar Clave</a></li>
                        <li><a class="dropdown-item" href="/logout">Cerrar Sesion</a></li>
                    </ul>
                </li>
            </ul>
% end            
        </div>
    </nav>
    <div class="container">
        <div class="mt-3 mb-4">&nbsp;</div>
"""
    return contenido

def generar_view_pie_tpl(modelo):
    nombre_modelo = get_filename_modelo(modelo)
    contenido = """
    <div class="mt-3 mb-4">&nbsp;</div>
</div>
</body>
</html>
"""
    return contenido

def generar_servir_download_entidad_blob(campo, entidad, modelo):
    contenido = """
def servir_download_{nombre_entidad_lower}_{nombre_campo}(id, extension):    
""".format( nombre_entidad_lower = entidad['nombre'].lower(), nombre_campo = campo['nombre'].lower() )
    if esEntidadUsuario(modelo, entidad['idObjeto']):
        contenido += """
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        abort( 401, "Acceso no autorizado" )
    con = orm.Conexion(PATH_BDD)
    {nombre_entidad_lower}, id_usuario_owner = {nombre_entidad_lower}_getowner(con, id)
    con.close()
    if {nombre_entidad_lower} is None or usuario['id'] != id_usuario_owner:
        abort( 403, "Acceso no autorizado")
""".format( nombre_entidad_lower = entidad['nombre'].lower() )
    else:
        contenido += """
    con = orm.Conexion(PATH_BDD)
    {nombre_entidad_lower} = {nombre_entidad}s.getNamedQuery(con, 'findById', {id_search_definition} )
    con.close()
    if len({nombre_entidad_lower}) == 0:
        abort(404, "No existe")
    {nombre_entidad_lower} = {nombre_entidad_lower}[0]
""".format( nombre_entidad_lower = entidad['nombre'].lower(), nombre_entidad = entidad['nombre'], id_search_definition = "{ 'id' : id }" )
    contenido += """    
    contenido = {nombre_entidad_lower}['{nombre_campo}']
    if len(contenido) == 0:
        abort(404, "No se dispone de contenido")
    response.add_header('Content-Type',"application/" + extension)
    return contenido

CONFIG['rutas'].append({ruta_definition})
""".format( nombre_entidad_lower = entidad['nombre'].lower(), nombre_campo = campo['nombre'], ruta_definition = "{'ruta':'/" + entidad['nombre'].lower() + "s/<id>/" + campo['nombre'].lower() + ".<extension>', 'metodos':['GET'], 'funcion': servir_download_" + entidad['nombre'].lower() + "_" + campo['nombre'].lower() + " }" )
    return contenido