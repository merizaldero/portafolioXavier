import ModeladorDao
import config
from random import choices

ESPACIO = ' ' * 4

TIPOS = {
    'STRING': { 'tipo':'CharField' },
    'INTEGER': { 'tipo':'IntegerField', 'req_max_length' : False },
    'LONG': { 'tipo':'BigIntegerField', 'req_max_length' : False },
    'DECIMAL': { 'tipo':'DecimalField' },
    'FLOAT': { 'tipo':'FloatField' },
    'DOUBLE': { 'tipo':'FloatField' },
    'DATE': { 'tipo':'DateField' , 'req_max_length' : False },
    'BOOLEAN': { 'tipo':'BooleanField' , 'req_max_length' : False },
    'CLOB': { 'tipo':'TextField' },
    'BLOB': { 'tipo':'BinaryField' },
    'DATETIME': { 'tipo':'DateTimeField' , 'req_max_length' : False },
    'DURATION': { 'tipo':'DurationField' , 'req_max_length' : False },
    'EMAIL': { 'tipo':'EmailField' },
    'FILE': { 'tipo':'FileField' },
    'FILEPATH': { 'tipo':'FilePathField' },
    'IMAGE': { 'tipo':'ImageField' },
    'GEN_IP_ADDRESS': { 'tipo':'GenericIpAddressField' , 'req_max_length' : False },
    'NULL_BOOLEAN': { 'tipo':'NullBooleanField' , 'req_max_length' : False },
    'POS_INTEGER': { 'tipo':'PositiveIntegerField' , 'req_max_length' : False },
    'POS_SM_INTEGER': { 'tipo':'PositiveSmallIntegerField' , 'req_max_length' : False },
    'SLUG': { 'tipo':'SlugField' },
    'SM_INTEGER': { 'tipo':'SmallIntegerField' , 'req_max_length' : False },
    'TIME': { 'tipo':'TimeField' , 'req_max_length' : False },
    'URL': { 'tipo':'UrlField' },
    'UUID': { 'tipo':'UUIDField' , 'req_max_length' : False },
    'FK': { 'tipo':'ForeignKey' , 'req_max_length' : False },
    'FK_USER': { 'tipo':'ForeignKey' , 'req_max_length' : False },
}

def definicionCampoModel(campo, modelo, dominio = 'models'):
    nombreCampo = campo['nombre']
    
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

    tipo = TIPOS[ tipo ]
    
    tipoCampo = tipo['tipo']
    
    parametros = ''
    
    if tipoCampo == 'ForeignKey':
        if campo['__atributos']['refUser'] != '1':
            pass
            named_query = data_referencia[0][1]
            entidad_destino = [x for x in entidades if x['idObjeto'] == int( named_query['__atributos']['entidadFK'] ) ][0]['nombre']
            parametros += "'{0}'".format( entidad_destino )
        else:
            parametros += "settings.AUTH_USER_MODEL"
        
        if 'obligatorio' in campo['__atributos'] and campo['__atributos']['obligatorio'] == '0':
            parametros += ", blank=True"
        else:
            parametros += ", on_delete = models.CASCADE"
    
    if not ( 'req_max_length' in tipo and tipo['req_max_length'] == False):
        parametros += 'max_length = {0}'.format( campo['__atributos']['tamano'] )
       
    if 'obligatorio' in campo['__atributos'] and campo['__atributos']['obligatorio'] == '0':
        if parametros != '':
            parametros += ', '
        parametros += 'null=True'
        
    if 'catalogo' in campo['__atributos'] and not (campo['__atributos']['catalogo'] is None) and campo['__atributos']['catalogo'] != '':
        catalogos = modelo['__objetoRaiz']['__listas']['Catalogos'] 
        choices = [ x for x in catalogos if x['idObjeto'] == int( campo['__atributos']['catalogo'] ) ]
        if len(choices) == 1:
            if parametros != '':
                parametros += ', '
            parametros += "choices = {0}".format(choices[0]['nombre'].upper())
    
    if campo['descripcion'] != '':
        if parametros != '':
            parametros += ', '
        parametros += 'help_text="{0}"'.format( campo['descripcion'] )
        
    
    definicion = ESPACIO + "{0}{1} = {2}.{3}({4})\n".format(ESPACIO, nombreCampo, dominio, tipoCampo, parametros )
    return definicion

def esCampoSuelto(campo):
    es_suelto = True
    return es_suelto

def generarModelsPy(modelo):    
    contenido = "\"\"\"\nDeficion de Modelos\n\"\"\"\nfrom django.conf import settings\nfrom django.db import models\nfrom django.urls import reverse\n\n"
    
    #incluye catalogos
    catalogos = modelo['__objetoRaiz']['__listas']['Catalogos']
    for catalogo in catalogos:
        nombreCatalogo = catalogo["nombre"].upper()
        valoresCatalogo = catalogo['__listas']['Valores']
        constantesCatalogos = [ "{2}_{0} = '{1}'\n".format(valorCatalogo['nombre'].upper(), valorCatalogo['nombre'], nombreCatalogo ) for valorCatalogo in valoresCatalogo ]
        listaConstantesCatalogos = [ ESPACIO + "({2}_{0} , '{1}'),\n".format( valorCatalogo['nombre'].upper(), valorCatalogo['nombre'], nombreCatalogo ) for valorCatalogo in valoresCatalogo ]        
        for x in constantesCatalogos:
            contenido += x
        contenido += "{0} = (\n".format(nombreCatalogo)
        for x in listaConstantesCatalogos:
            contenido += x
        contenido += ")\n"
        
    #incluye Modelos
    entidades = modelo['__objetoRaiz']['__listas']['Entidades']
    for entidad in entidades:
        nombreEntidad = entidad['nombre']
        campos = entidad['__listas']['Campos']
        definicionesCampos = [ definicionCampoModel(campo,modelo) for campo in campos if esCampoSuelto(campo) ]
        
        contenido += "\nclass {0}(models.Model):\n".format(nombreEntidad)
        for x in definicionesCampos:
            contenido += x;
    
    #incluye clase de au
    return contenido

def generarFormsPy(modelo):
    return ''

def generarAdminViewsPy(modelo):
    return ''

def generarViewsPy(modelo):
    return ''

def generarUrlsPy(modelo):
    return ''

def generarModelo(modelo):
    
    resultado = { 'archivos' : [ { 'path':'app/models.py', 'contenido': generarModelsPy(modelo) },
                                 { 'path':'app/forms.py', 'contenido':  generarFormsPy(modelo) },
                                 { 'path':'app/admin.py', 'contenido':  generarAdminViewsPy(modelo) },
                                 { 'path':'app/views.py', 'contenido':  generarViewsPy(modelo) },
                                 { 'path':'project/urls.py', 'contenido':  generarUrlsPy(modelo) },
                                 ]}
    
    return resultado
    
    
    
    


            