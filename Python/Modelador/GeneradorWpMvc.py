import GeneradorERScriptSql
from email._header_value_parser import get_display_name

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

INPUT_MAPPINGS = {
    'STRING': { 'type':'text' , 'maxlenght':'$tamano' },
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

def generarSecuenciaGen(modelo,generacion):
    nombrePlugin = modelo['__objetoRaiz']['nombre']
    entidades = modelo['__objetoRaiz']['__listas']['Entidades']
    lista_entidades = ["sudo ./wpmvc generate {2} {1} {0}".format(entidad['nombre'], nombrePlugin, generacion) for entidad in entidades]
    return "\n".join( lista_entidades )

def generarInitSequence(modelo):
    contenido = ''
    nombrePlugin = modelo['__objetoRaiz']['nombre']
    entidades = modelo['__objetoRaiz']['__listas']['Entidades']    
    contenido = """
cd /var/www/html/wp-content/plugins/wp-mvc
sudo ./wpmvc generate plugin {0}

{1}
    """.format(nombrePlugin, generarSecuenciaGen(modelo, 'model') )
    return contenido

def tableNamer(entidad,modelo):
    nombreTabla = entidad['nombre'].lower()
    prefijo = modelo['__objetoRaiz']['__atributos']['prefijo']
    if entidad['idTipoMetamodelo'] == 'ENTIDAD':
        nombreTabla = entidad['__atributos']['nombreTabla']
        return "' . $wpdb->prefix . '" + prefijo + nombreTabla 
    elif entidad['idTipoMetamodelo'] == 'NAMED_QUERY':
        prefijo = modelo['__objetoRaiz']['__atributos']['prefijo'].lower()
        nombreTabla = entidad['__atributos']['nombreIndice'].lower()
        return "{0}{1}".format(prefijo,nombreTabla)
    return nombreTabla

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
    
    global $wpdb;
    
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

def obtenerCamposPksFks(entidad,entidades):
    campos = entidad['__listas']['Campos']
    pk = [ campo for campo in campos if campo['__atributos']['pk'] == '1' ][0]
    fks = [ (named_query, entidad_fk) 
           for named_query in entidad['__listas']['NamedQuieries'] 
           for entidad_fk in entidades 
           if named_query['__atributos']['entidadFK'].isnumeric() 
           and entidad_fk['idObjeto'] == int(named_query['__atributos']['entidadFK']) ]
    display_name = [ campo for campo in campos if campo['__atributos']['displayName'] == '1' ][0]
    return campos, pk, fks, display_name

def anexarModelClases(modelo):
    resultado = []
    nombrePlugin = modelo['__objetoRaiz']['nombre']
    prefijo = modelo['__objetoRaiz']['__atributos']['prefijo']
    entidades = modelo['__objetoRaiz']['__listas']['Entidades']
    for entidad in entidades:
        nombreTabla = "{prefix}" + prefijo + entidad['__atributos']['nombreTabla']
        
        campos, pk, fks , display_name  = obtenerCamposPksFks(entidad,entidades)        
        
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
        lista_fks = []
        for fkdef in fks:
            named_query = fkdef[0]
            entidad_fk = fkdef[1]
            campos_fk = [campo for campo_fk in named_query['__listas']['camposWhere'] for campo in campos 
                         if campo['nombre'] == campo_fk['nombre']]
            lista_campos_fk = [ campo['__atributos']['nombreCampo'].lower() for campo in campos_fk ]
            lista_fks.append("'{0}' => [ 'foreign_key' => '{1}' ]".format( entidad_fk['nombre'], ",".join(lista_campos_fk) ) )
        path = "sudo nano ../{0}/app/models/{1}.php".format( nombrePlugin, entidad['nombre'].lower() )
        contenido ="""<?php
class """+entidad['nombre']+""" extends MvcModel {
    var $table = '""" + nombreTabla + """';    
    var $primary_key = '""" + pk['__atributos']['nombreCampo'].lower() + """';
    var $selects = [""" + ", ".join(lista_campos) + """];
    var $validate = [
        """ + ",\n        ".join(validaciones_campos) + """
    ];
    var $belongs_to = [
        """ + ",\n        ".join(lista_fks) + """
    ];
    var $per_page = 7;
    var $display_field = '"""+ display_name['__atributos']['nombreCampo'].lower() +"""';
}
?>"""
        resultado.append( { "path" : path , "contenido" : contenido } )
    return resultado

def anexarControllerClases(modelo):
    resultado = []
    nombrePlugin = modelo['__objetoRaiz']['nombre']
    prefijo = modelo['__objetoRaiz']['__atributos']['prefijo']
    entidades = modelo['__objetoRaiz']['__listas']['Entidades']
    for entidad in entidades:
        nombreTabla = "{prefix}" + prefijo + entidad['__atributos']['nombreTabla']
        
        campos, pk, fks, display_name = obtenerCamposPksFks(entidad,entidades) 
        
        lista_campos = ["'{0}'".format( campo['__atributos']['nombreCampo'].lower() ) for campo in campos]
        default_columns = []
        default_column_methods = []
        for campo in campos:
            nombreCampo = campo['__atributos']['nombreCampo'].lower()
            default_columns.append("'{0}' => [\n            'label'=>'{2}',\n            'value_method'=>'print_{1}'\n        ]".format( nombreCampo, campo['nombre'], campo['nombre'].capitalize() ))
            if campo['__atributos']['tipo'] == 'BOOLEAN':
                default_column_methods.append("public function print_" + campo['nombre'] + " ($object) {\n        return ($object->"+nombreCampo+" == '1') ? 'SI' : 'NO' ; \n    }\n")
            else:
                default_column_methods.append("public function print_" + campo['nombre'] + " ($object) {\n        return empty($object->"+nombreCampo+") ? null : $object->"+nombreCampo+" ; \n    }\n")

        lista_fk_methods = []
        lista_fk_method_calls = []
        for fkdef in fks:
            #named_query = fkdef[0]
            entidad_fk = fkdef[1]
            campos_fk, pk_fk, fks_fk, display_name_fk = obtenerCamposPksFks(entidad_fk,entidades)
            campos_nombre = [ "'{0}'".format(pk_fk['__atributos']['nombreCampo'].lower()) , "'{0}'".format(display_name_fk['__atributos']['nombreCampo'].lower()) ]
            lista_fk_methods.append("""private function set_""" + entidad_fk['nombre'].lower() + """s() {
        $this->load_model('""" + entidad_fk['nombre'] + """');
        $"""+ entidad_fk['nombre'].lower() +"""s = $this->""" + entidad_fk['nombre'] + """->find( ['selects' => ["""+", ".join(campos_nombre)+"""] ] );
        $this->set('"""+ entidad_fk['nombre'].lower() +"""s', $"""+ entidad_fk['nombre'].lower() +"""s );
    }
""" )
            lista_fk_method_calls.append("$this->set_{0}s();".format( entidad_fk['nombre'].lower() ))
        # Admin Controller
        path = "sudo nano ../{0}/app/controllers/admin/admin_{1}s_controller.php".format( nombrePlugin, entidad['nombre'].lower() )
        contenido ="""<?php
class Admin"""+entidad['nombre']+"""sController extends MvcAdminController {
    var $default_columns = [
        """ + ",\n        ".join(default_columns) + """
    ];
"""+ "\n        ".join(default_column_methods) +"""
""" + "\n".join(lista_fk_methods) + """

    public function add(){
        """+ "\n".join(lista_fk_method_calls) +"""
        parent::add();
    }
    
    public function edit(){
        """+ "\n".join(lista_fk_method_calls) +"""
        parent::edit();
    }
}
?>"""
        resultado.append( { "path" : path , "contenido" : contenido } )
        
        # Public Controller
        path = "sudo nano ../{0}/app/controllers/{1}s_controller.php".format( nombrePlugin, entidad['nombre'].lower() )
        contenido ="""<?php
class """+entidad['nombre']+"""sController extends MvcPublicController {
    var $default_columns = [
        """ + ",\n        ".join(default_columns) + """
    ];
"""+ "\n        ".join(default_column_methods) +"""
""" + "\n".join(lista_fk_methods) + """   
}
?>"""
        resultado.append( { "path" : path , "contenido" : contenido } )

    return resultado

def contenidoShowView( entidad, entidades ):
    
    campos, pk, fks, display_name = obtenerCamposPksFks(entidad,entidades)
    
    lista_campos = []
    for campo in campos:
        if campo['nombre'] == pk['nombre'] or campo['__atributos']['displayName'] == '1' :
            continue
        nombreCampo = campo['__atributos']['nombreCampo']
        lista_campos.append( """<?php
if(!empty($object->""" + nombreCampo.lower() + """)){
    echo '<div><span>"""+ campo['nombre'] +"""</span><span>' . $object->""" + nombreCampo.lower() + """ . '</span></div>';
} 
?>""" )   
    
    contenido = """

<h2><?php echo $object->"""+ display_name['__atributos']['nombreCampo'].lower() +"""; ?></h2>

"""+ "\n".join(lista_campos)+"""

<p>
  <?php echo $this->html->link('Todos los """ + entidad['nombre'] + """s', array('controller' => '""" + entidad['nombre'].lower() + """s')); ?>
</p>
    
    """
    return contenido

def obtenerEntidadFK(campo, fks):
    for fk in fks:
        named_query = fk[0]
        entidad = fk[1]
        camposfk = [ campofk for campofk in named_query['__listas']['camposWhere'] if campofk['nombre'] == campo['nombre'] ]
        if len(camposfk) > 0:
            return entidad
    return None

def contenidoAdminAddView( entidad, entidades ):
    campos, pk, fks, display_name = obtenerCamposPksFks(entidad,entidades)
    lista_campos = []
    for campo in campos:
        if campo['nombre'] == pk['nombre'] :
            continue
        nombreCampo = campo['__atributos']['nombreCampo']
        entidad_fk = obtenerEntidadFK(campo, fks)
        if not(entidad_fk is None):
            lista_campos.append( "<?php echo $this->form->belongs_to_dropdown('{0}', ${1}s, ['label' => '{2}', 'type' => 'checkbox', 'empty' => true ]); ?>".format( nombreCampo.lower()[:-3], entidad_fk['nombre'].lower() ,campo['nombre'].capitalize() ) )
        elif campo['__atributos']['tipo'] == 'BOOLEAN':
            lista_campos.append( "<?php echo $this->form->input('{0}', ['label' => '{1}', 'type' => 'checkbox', 'value' => '1']); ?>".format( nombreCampo.lower(), campo['nombre'].capitalize() ) )
        elif campo['__atributos']['tipo'] == 'DATE':
            lista_campos.append( "<?php echo $this->form->input('{0}', ['label' => '{1}', 'type' => 'date']); ?>".format( nombreCampo.lower(), campo['nombre'].capitalize() ) )
        elif campo['__atributos']['tipo'] == 'DATETIME':
            lista_campos.append( "<?php echo $this->form->input('{0}', ['label' => '{1}', 'type' => 'datetime-local']); ?>".format( nombreCampo.lower(), campo['nombre'].capitalize() ) )
        elif campo['__atributos']['tipo'] == 'EMAIL':
            lista_campos.append( "<?php echo $this->form->input('{0}', ['label' => '{1}', 'type' => 'email']); ?>".format( nombreCampo.lower(), campo['nombre'].capitalize() ) )
        elif campo['__atributos']['tipo'] in ['FILE','IMAGE']:
            lista_campos.append( "<?php echo $this->form->input('{0}', ['label' => '{1}', 'type' => 'file']); ?>".format( nombreCampo.lower(), campo['nombre'].capitalize() ) )            
        elif campo['__atributos']['tipo'] in ['INTEGER','LONG','DECIMAL','FLOAT','POS_INTEGER','POS_LONG','POS_SM_INTEGER','SM_INTEGER']:
            lista_campos.append( "<?php echo $this->form->input('{0}', ['label' => '{1}', 'type' => 'number']); ?>".format( nombreCampo.lower(), campo['nombre'].capitalize() ) )            
        else:
            lista_campos.append( "<?php echo $this->form->input('{0}', ['label' => '{1}']); ?>".format( nombreCampo.lower(), campo['nombre'].capitalize() ) )        
    contenido = """<h2>Nuevo """ + entidad['nombre'] + """</h2>

<?php echo $this->form->create($model->name, array('is_admin' => $this->is_admin)); ?>
<?php echo $this->form->open_admin_table(); ?>

""" + "\n".join(lista_campos) + """

<?php echo $this->form->close_admin_table(); ?>
<?php echo $this->form->end('Guardar'); ?>
"""

    return contenido

def contenidoAdminEditView( entidad, entidades ):
    campos, pk, fks, display_name = obtenerCamposPksFks(entidad,entidades)
    lista_campos = []
    for campo in campos:
        if campo['nombre'] == pk['nombre']:
            continue
        nombreCampo = campo['__atributos']['nombreCampo']       
        entidad_fk = obtenerEntidadFK(campo, fks)
        if not(entidad_fk is None):
            lista_campos.append( "<?php echo $this->form->belongs_to_dropdown('{0}', ${1}s, ['label' => '{2}', 'type' => 'checkbox', 'empty' => true ]); ?>".format( nombreCampo.lower()[:-3], entidad_fk['nombre'].lower() ,campo['nombre'].capitalize() ) )
        elif campo['__atributos']['tipo'] == 'BOOLEAN':
            lista_campos.append( "<?php echo $this->form->input('{0}', ['label' => '{1}', 'type' => 'checkbox', 'value' => '1']); ?>".format( nombreCampo.lower(), campo['nombre'].capitalize() ) )
        elif campo['__atributos']['tipo'] == 'DATE':
            lista_campos.append( "<?php echo $this->form->input('{0}', ['label' => '{1}', 'type' => 'date']); ?>".format( nombreCampo.lower(), campo['nombre'].capitalize() ) )
        elif campo['__atributos']['tipo'] == 'DATETIME':
            lista_campos.append( "<?php echo $this->form->input('{0}', ['label' => '{1}', 'type' => 'datetime-local']); ?>".format( nombreCampo.lower(), campo['nombre'].capitalize() ) )
        elif campo['__atributos']['tipo'] == 'EMAIL':
            lista_campos.append( "<?php echo $this->form->input('{0}', ['label' => '{1}', 'type' => 'email']); ?>".format( nombreCampo.lower(), campo['nombre'].capitalize() ) )
        elif campo['__atributos']['tipo'] in ['FILE','IMAGE']:
            lista_campos.append( "<?php echo $this->form->input('{0}', ['label' => '{1}', 'type' => 'file']); ?>".format( nombreCampo.lower(), campo['nombre'].capitalize() ) )            
        elif campo['__atributos']['tipo'] in ['INTEGER','LONG','DECIMAL','FLOAT','POS_INTEGER','POS_LONG','POS_SM_INTEGER','SM_INTEGER']:
            lista_campos.append( "<?php echo $this->form->input('{0}', ['label' => '{1}', 'type' => 'number']); ?>".format( nombreCampo.lower(), campo['nombre'].capitalize() ) )            
        else:
            lista_campos.append( "<?php echo $this->form->input('{0}', ['label' => '{1}']); ?>".format( nombreCampo.lower(), campo['nombre'].capitalize() ) )                
    contenido = """<h2>Editar """ + entidad['nombre'] + """</h2>

<?php echo $this->form->create($model->name, array('is_admin' => $this->is_admin)); ?>
<?php echo $this->form->open_admin_table(); ?>

""" + "\n".join(lista_campos) + """

<?php echo $this->form->close_admin_table(); ?>
<?php echo $this->form->end('Actualizar'); ?>
"""

    return contenido

def contenidoAdminIndexView( entidad, entidades ):
    nombreEntidad = entidad['nombre']    
    contenido = """<h2>""" + nombreEntidad + """s</h2>
<div>
<a class="button button-primary" href="<?php echo mvc_admin_url([ 'controller' => '""" + nombreEntidad.lower() + """s', 'action' => 'add' ]) ?>">Agregar</a>
</div>
<table class="widefat post fixed striped" cellspacing="0">
    <thead>
        <?php 
        echo $this->html->admin_header_cells($this);
        ?>
    </thead>
    <tfoot>
        <?php 
        echo $this->html->admin_header_cells($this);
        ?>
    </tfoot>
    <tbody>
        <?php 
        echo $this->html->admin_table_cells($this, $objects, []);
        ?>
    </tbody>
    <?php // echo $this->pagination(); ?>
    
</table>
"""

    return contenido


def anexarPages(modelo):
    resultado = []
    nombrePlugin = modelo['__objetoRaiz']['nombre']
    prefijo = modelo['__objetoRaiz']['__atributos']['prefijo']
    entidades = modelo['__objetoRaiz']['__listas']['Entidades']
    
    resultado += [ { "path": "sudo vim ../{0}/app/views/{1}s/show.php".format( nombrePlugin, entidad['nombre'].lower() ) , 
                    "contenido": contenidoShowView( entidad, entidades ) }
        for entidad in entidades
        ]
    
    resultado += [ { "path": "sudo vim ../{0}/app/views/admin/{1}s/add.php".format( nombrePlugin, entidad['nombre'].lower() ) , 
                    "contenido": contenidoAdminAddView( entidad, entidades ) }
        for entidad in entidades
        ]

    resultado += [ { "path": "sudo vim ../{0}/app/views/admin/{1}s/edit.php".format( nombrePlugin, entidad['nombre'].lower() ) , 
                    "contenido": contenidoAdminEditView( entidad, entidades ) }
        for entidad in entidades
        ]
    
    resultado += [ { "path": "sudo vim ../{0}/app/views/admin/{1}s/index.php".format( nombrePlugin, entidad['nombre'].lower() ) , 
                    "contenido": contenidoAdminIndexView( entidad, entidades ) }
        for entidad in entidades
        ]

    return resultado

def generarBootstrap(modelo):
    prefijo = modelo['__objetoRaiz']['__atributos']['prefijo'].lower()
    entidades = modelo['__objetoRaiz']['__listas']['Entidades']
    adminPages = modelo['__objetoRaiz']['__listas']['AdminPages']
    lista_entidades = ["""'ver_{0}s' => ['label' => '{1}s']""".format(entidad['nombre'].lower() , entidad['nombre']) for entidad in adminPages] 
    lista_entidades = [ """    '{0}mains' => [ 'label' => '{1}' , 
            {2}
            ]""".format( prefijo , modelo['nombre'], ",\n                ".join(lista_entidades) ) ]
    lista_entidades += [ """        '{0}s' => [ 'label' => '{1}s', 'parent_slug' => 'admin.php?page=mvc_{2}mains',
            'add' , 'edit', 'delete'
        ]""".format(entidad['nombre'].lower() , entidad['nombre'], prefijo) for entidad in entidades ]
    contenido = """
<?php

MvcConfiguration::set(array(
    'Debug' => false
));

MvcConfiguration::append(array(
    'AdminPages' => array(
        """ + ",\n".join(lista_entidades) + """
    )
));    
    """
    return contenido

def anexarMainAdminControllers(modelo):
    nombrePlugin = modelo['__objetoRaiz']['nombre']
    prefijo = modelo['__objetoRaiz']['__atributos']['prefijo']
    adminPages = modelo['__objetoRaiz']['__listas']['AdminPages']
    path = 'nano vim ../{0}/app/controllers/admin/admin_{1}mains_controller.php'.format(nombrePlugin, prefijo.lower() )
    lista_metodos = [ """    public function ver_"""+ entidad['nombre'].lower() +"""s(){
        $url = MvcRouter::admin_url(array('controller' => '"""+ entidad['nombre'].lower() +"""s', 'action' => 'index'));
        $this->redirect($url);
    }""" for entidad in adminPages]
    contenido = """<?php

class Admin"""+ prefijo.capitalize().replace('_','') +"""MainsController extends MvcAdminController {

    var $default_columns = array('id', 'name');
    public function index(){
        
    }
    
"""+ "\n".join(lista_metodos) +"""

}
    """
    lista = [ {'path': path, 'contenido': contenido} ]
    return lista

def anexarMainAdminViews(modelo):
    nombrePlugin = modelo['__objetoRaiz']['nombre']
    prefijo = modelo['__objetoRaiz']['__atributos']['prefijo'].lower()
    adminPages = modelo['__objetoRaiz']['__listas']['AdminPages']
    lista_modulos = [ """<div class="card" style="display:flex; flex-direction: row; align-items: center ; justify-content: space-between;align-content:flex-start"  >
    <h3>""" + entidad['nombre'] + """</h3>
    <a href="<?php echo MvcRouter::admin_url(array('controller' => '""" + entidad['nombre'].lower() + """s', 'action' => 'index')); ?>">Detalles</a>
</div>""" for entidad in adminPages ]
    path = 'nano vim ../{0}/app/views/admin/{1}mains/index.php'.format(nombrePlugin, prefijo)
    contenido = """
<h2>"""+ nombrePlugin +"""</h2>    
    """ + "\n".join(lista_modulos)
    lista = [ {'path': path, 'contenido': contenido} ]
    return lista

def generarModelo(modelo):
    nombrePlugin = modelo['__objetoRaiz']['nombre']
    prefijo = modelo['__objetoRaiz']['__atributos']['prefijo'].capitalize().replace('_','')
    resultado = { 'archivos' : [ 
                                 { 'path':'SECUENCIA INICIAL',     'contenido': generarInitSequence(modelo) },
                                 { 'path':'sudo nano ../{0}/{0}_loader.php'.format( nombrePlugin ), 'contenido': generarPluginLoader(modelo) },
                                 ]}
    resultado['archivos'] +=  anexarModelClases(modelo)
    resultado['archivos'].append( {'path' : 'SECUENCIA GENERACION CONTROLLERS', 
                                   'contenido' : "sudo ./wpmvc generate controllers micondominio {0}Main\n".format(prefijo) + generarSecuenciaGen(modelo,'controllers') } )
    resultado['archivos'] +=  anexarMainAdminControllers(modelo)
    resultado['archivos'] +=  anexarControllerClases(modelo)
    resultado['archivos'].append( {'path' : 'SECUENCIA GENERACION VIEWS', 
                                   'contenido' : "sudo ./wpmvc generate views micondominio {0}Main\n".format(prefijo) + generarSecuenciaGen(modelo,'views') } )
    resultado['archivos'] +=  anexarMainAdminViews(modelo)
    resultado['archivos'] +=  anexarPages(modelo)    
    resultado['archivos'].append( { 'path':'sudo nano ../{0}/app/config/bootstrap.php'.format( nombrePlugin ), 'contenido': generarBootstrap(modelo) } )
    return resultado
    