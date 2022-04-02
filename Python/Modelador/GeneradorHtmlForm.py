import config

TIPOS = {
    'STRING': { 'tipo':'CharField' },
    'INTEGER': { 'tipo':'IntegerField', 'req_max_length' : False, 'tamano' = 5},
    'LONG': { 'tipo':'BigIntegerField', 'req_max_length' : False, 'tamano' = 10 },
    'DECIMAL': { 'tipo':'DecimalField' , 'req_precision' : True },
    'FLOAT': { 'tipo':'FloatField' },
    'DOUBLE': { 'tipo':'FloatField' },
    'DATE': { 'tipo':'DateField' , 'req_max_length' : False , 'tamano' = 10 },
    'BOOLEAN': { 'tipo':'BooleanField' , 'req_max_length' : False , 'tamano' = 1},
    'CLOB': { 'tipo':'TextField' },
    'BLOB': { 'tipo':'BinaryField' },
    'DATETIME': { 'tipo':'DateTimeField' , 'req_max_length' : False , 'tamano' = 22 },
    'DURATION': { 'tipo':'DurationField' , 'req_max_length' : False , 'tamano' = 11 },
    'EMAIL': { 'tipo':'EmailField' },
    'FILE': { 'tipo':'FileField' },
    'FILEPATH': { 'tipo':'FilePathField' },
    'IMAGE': { 'tipo':'ImageField' },
    'GEN_IP_ADDRESS': { 'tipo':'GenericIpAddressField' , 'req_max_length' : False, 'tamano' = 256  },
    'NULL_BOOLEAN': { 'tipo':'NullBooleanField' , 'req_max_length' : False , 'tamano' = 1},
    'POS_INTEGER': { 'tipo':'PositiveIntegerField' , 'req_max_length' : False , 'tamano' = 5},
    'POS_SM_INTEGER': { 'tipo':'PositiveSmallIntegerField' , 'req_max_length' : False , 'tamano' = 5},
    'SLUG': { 'tipo':'SlugField' },
    'SM_INTEGER': { 'tipo':'SmallIntegerField' , 'req_max_length' : False , 'tamano' = 5},
    'TIME': { 'tipo':'TimeField' , 'req_max_length' : False , 'tamano' = 22},
    'URL': { 'tipo':'UrlField' },
    'UUID': { 'tipo':'UUIDField' , 'req_max_length' : False , 'tamano' = 32},
    'FK': { 'tipo':'ForeignKey' , 'req_max_length' : False },
    'FK_USER': { 'tipo':'ForeignKey' , 'req_max_length' : False },
}

def default_html_input_pk(campo, modelo):
    nombreCampo = campo['nombre']
    return '<input type="hidden" name="{0}", id="fld_{0}">'.format(nombreCampo)
def default_html_input_usr(campo, modelo):
    return ""

def default_html_input_sel(campo, modelo,data_referencia, estilos_adicionales = '', clases_adicionales = ''):
    nombreCampo = campo['nombre']
    entidades_referenciadas = ['lst_'+x[0]['nombre'] for x in data_referencia]
    clases_listas = ' '.join(entidades_referenciadas)
    catalogos = [ valor['nombre'] for valor in catalogo['__listas']['Valores'] for catalogo in modelo['__listas']['Catalogos'] if catalogo['id'] == campo['__atributos']['catalogo'] ]
    opciones_catalogo = "\n".join( [ '<option value="{0}">{0}</option>'.format(valor) for valor in catalogos ] )
    return """
<div class="form-group">
    <label for="fld_{0}">{0}</label>
    <select name="{0}" id="fld_{0}" class="form-control {1} {2}" style="{3}">
        <option value = "">- Elegir -</option>
{4}
    </select>
    <div class="valid-feedback">Valido.</div>
    <div class="invalid-feedback">Favor Llenar.</div>
</div>
    """.format(nombreCampo, clases_listas, clases_adicionales, estilos_adicionales, opciones_catalogo )

def default_html_input_input(campo, modelo, estilos_adicionales = '', clases_adicionales = ''):
    nombreCampo = campo['nombre']
    propiedades_adicionales = []
    if campo['__atributos']['obligatorio'] == '1':
        propiedades_adicionales.append("required")
    if campo['__atributos']['tipo'] in TIPOS.keys():
        tipo = TIPOS[ campo['__atributos']['tipo'] ]
        if tipo['req_max_length'] == False and 'tamano' in tipo.keys() :
            propiedades_adicionales.append('maxlength="{0}"'.format(tipo['tamano']))
        elif 'tamano' in campo['__atributos'] :
            propiedades_adicionales.append('maxlength="{0}"'.format(campo['__atributos']['tamano']))
    else:
        pass
    if campo['__atributos']['tipo'] in ['INTEGER', 'LONG', 'DECIMAL', 'FLOAT', 'DOUBLE', 'POS_INTEGER', 'POS_SM_INTEGER', 'SM_INTEGER'] :
        propiedades_adicionales.append('type="number"')
    elif campo['__atributos']['tipo'] in ['DATE'] :
        propiedades_adicionales.append('type="date"')
    elif campo['__atributos']['tipo'] in ['DATETIME'] :
        propiedades_adicionales.append('type="datetime-local"')
    elif campo['__atributos']['tipo'] in ['BOOLEAN'] :
        propiedades_adicionales.append('type="checkbox"')
        clases_adicionales += ' custom-control-input'
    return """
<div class="form-group">
    <label for="fld_{0}">{0}</label>
    <input name="{0}" id="fld_{0}" class="form-control {1}" style="{2}" {3}>
    <div class="valid-feedback">Valido.</div>
    <div class="invalid-feedback">Favor Llenar.</div>
</div>
    """.format(nombreCampo, clases_adicionales, estilos_adicionales, " ".join(propiedades_adicionales))

def default_html_input(campo, modelo, input_pk = default_html_input_pk, input_usr = default_html_input_usr, input_sel = default_html_input_sel , input_input = default_html_input_input ):
    nombreCampo = campo['nombre']

    # Si es un PK, solo desplega el input
    if 'pk' in campo['__atributos'] and campo['__atributos']['pk'] == '1':
        return input_pk(campo, modelo)

    entidades = None
    data_referencia = []

    tipo = campo['__atributos']['tipo']

    if campo['__atributos']['refUser'] != '1':
        entidades = modelo['__objetoRaiz']['__listas']['Entidades']
        data_referencia = [ (entidad, named_query, campo_where) for entidad in entidades for named_query in entidad['__listas']['NamedQuieries'] for campo_where in named_query['__listas']['camposWhere'] for entidad_destino in entidades if entidad['idObjeto'] == campo['idObjetoPadre'] and named_query['__atributos']['entidadFK'].isnumeric() and campo_where['nombre'] == campo['nombre'] ]
        if len(data_referencia) > 0:
            tipo = 'FK'
    else:
        tipo = 'FK_USER'

    if tipo == 'FK_USER':
        return input_usr(campo, modelo)

    if tipo == 'FK' or campo['__atributos']['catalogo'] != '' :
        return input_sel(campo, modelo,data_referencia)

    return default_html_input_input(campo, modelo)

def htmlForm(entidad , modelo, html_campo = htmlCampo):
    campos = entidad['__listas']['Campos']
    html_campos = [ html_campo(campo, modelo) for campo in campos ]
    resultado = "<div class ='form-group'>\n{0}\n<div>\n".format("\n".join(html_campos))
    return resultado
