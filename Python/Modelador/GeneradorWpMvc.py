import GeneradorERScriptSql

ESPACIO = ' '*4

TIPOS = {
    'STRING': { 'rule':'alphanumeric' },
    'INTEGER': { 'pattern': r'/^(\+|-)?\d+$/' },
    'LONG': { 'pattern': r'/^(\+|-)?\d+$/' },
    'DECIMAL': { 'rule':'numeric' },
    'FLOAT': { 'rule':'numeric' },
    'DOUBLE': { 'rule':'numeric' },
    'DATE': { 'pattern': r'/^([1-9][0-9]{3})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])?$/' },
    'BOOLEAN': { 'pattern': r'/^1|0$/' },
    'CLOB': {  },
    'BLOB': {  },
    'DATETIME': { 'pattern': r'/^(?:[\+-]?\d{4}(?!\d{2}\b))(?:(-?)(?:(?:0[1-9]|1[0-2])(?:\1(?:[12]\d|0[1-9]|3[01]))?|W(?:[0-4]\d|5[0-2])(?:-?[1-7])?|(?:00[1-9]|0[1-9]\d|[12]\d{2}|3(?:[0-5]\d|6[1-6])))(?:[T\s](?:(?:(?:[01]\d|2[0-3])(?:(:?)[0-5]\d)?|24\:?00)(?:[\.,]\d+(?!:))?)?(?:\2[0-5]\d(?:[\.,]\d+)?)?(?:[zZ]|(?:[\+-])(?:[01]\d|2[0-3]):?(?:[0-5]\d)?)?)?)?$/' },
    'DURATION': { 'pattern': r'/^(-?)P(?=\d|T\d)(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)([DW]))?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?)?$/' },
    'EMAIL': { 'rule':'email' },
    'FILE': {  },
    'FILEPATH': { 'pattern': r'/(\\\\?([^\\/]*[\\/])*)([^\\/]+)$/' },
    'IMAGE': {  },
    'GEN_IP_ADDRESS': { 'pattern': r'/^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/' },
    'NULL_BOOLEAN': { 'pattern': r'/^1|0$/' },
    'POS_INTEGER': { 'pattern': r'/^\d+$/' },
    'POS_SM_INTEGER': { 'pattern': r'/^\d+$/' },
    'SLUG': { 'rule':'not_empty' },
    'SM_INTEGER': { 'pattern': r'/^(\+|-)?\d+$/' },
    'TIME': { 'pattern': r'/^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$/' },
    'URL': { 'rule':'url' },
    'UUID': { 'pattern': r'/^[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}$/' },
    'FK': {  },
    'FK_USER': { 'pattern': r'/^(\+|-)?\d+$/' },
}

def generarInitSequence(modelo):
    contenido = ''
    nombrePlugin = modelo['__objetoRaiz']['nombre']
    entidades = modelo['__objetoRaiz']['__listas']['Entidades']
    lista_entidades = ["sudo ./wpmvc generate model {1} {0}".format(entidad['nombre'], nombrePlugin) for entidad in entidades]
    contenido = """
cd /var/www/html/wp-content/plugins/wp-mvc
sudo ./wpmvc generate plugin {0}

{1}
    """.format(nombrePlugin, "\n".join(lista_entidades))
    return contenido

def tableNamer(entidad,modelo):    
    nombreTabla = entidad['nombre'].lower()
    return "' . $this->tables['" + nombreTabla + "s'] . '"

def generarPluginLoader(modelo):
    scriptbdd = GeneradorERScriptSql.generarModelo(modelo)
    entidades = modelo['__objetoRaiz']['__listas']['Entidades']
    createSqls = [ GeneradorERScriptSql.obtenerCreateTable(entidad, modelo, table_namer = tableNamer ) for entidad in entidades ]
    createSqls = [ "'"+ sql+"'" for sql in createSqls ]
    contenido = """
<?php
function activate() {

    // The $this->activate_app(__FILE__) call needs to be made to
    // activate this app within WP MVC
    
    $this->activate_app(__FILE__);
    
    require_once ABSPATH.'wp-admin/includes/upgrade.php';
    
    add_option('my_plugin_db_version', $this->db_version);
    
    $sqls = [
    """ + ",\n".join(createSqls) + """
    ];
    foreach( $sqls as $sql){
        dbDelta($sql);
    }
}
?>
    """
    return contenido

def anexarModelClases(modelo):
    resultado = []
    nombrePlugin = modelo['__objetoRaiz']['nombre']
    prefijo = modelo['__objetoRaiz']['__atributos']['prefijo']
    entidades = modelo['__objetoRaiz']['__listas']['Entidades']
    for entidad in entidades:
        nombreTabla = "{prefix}" + prefijo + entidad['__atributos']['nombreTabla']
        campos = entidad['__listas']['Campos']
        pk = [ campo for campo in campos if campo['__atributos']['pk'] == '1' ][0]
        lista_campos = ["'{0}'".format( campo['__atributos']['nombreCampo'].lower() ) for campo in campos]
        validaciones_campos = []
        for campo in campos:
            if campo['nombre'] == pk['nombre']:
                continue
            nombreCampo = campo['__atributos']['nombreCampo'].lower()
            atributos_validacion = [ "'message' => '{0} no v&aacute;lido'".format( campo['nombre'] ) ]
            if campo['__atributos']['obligatorio'] == '1':
                atributos_validacion.append( "'required' => true" )
            else:
                atributos_validacion.append( "'required' => false" )
            tipo = TIPOS[ campo['__atributos']['tipo'] ]
            atributos_validacion += [ "'{0}' => '{1}'".format( clave, tipo[clave] ) for clave in list(tipo.keys()) ]
            validaciones_campos.append("'{0}' => [\n            {1}\n        ]".format( nombreCampo, ",\n            ".join(atributos_validacion) ))
        path = "plugins/{0}/app/models/{1}.php".format( nombrePlugin, entidad['nombre'].lower() )
        contenido ="""<?php
class """+entidad['nombre']+""" extends MvcModel {
    var $table = '""" + nombreTabla + """';    
    var $primary_key = '""" + pk['__atributos']['nombreCampo'].lower() + """';
    var $selects = [""" + ", ".join(lista_campos) + """];
    var $validate = [
        """ + ",\n        ".join(validaciones_campos) + """
    ];
    var $per_page = 7;
}
?>"""
        resultado.append( { "path" : path , "contenido" : contenido } )
    return resultado
    
def generarModelo(modelo):
    nombrePlugin = modelo['__objetoRaiz']['nombre']
    resultado = { 'archivos' : [ 
                                 { 'path':'Secuencia init',     'contenido': generarInitSequence(modelo) },
                                 { 'path':'plugins/{0}/{0}_loader.php'.format( nombrePlugin ), 'contenido': generarPluginLoader(modelo) },
                                 ]}
    resultado['archivos'] +=  anexarModelClases(modelo) ;
    return resultado
    