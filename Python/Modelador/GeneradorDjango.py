import ModeladorDao
import config
from random import choices

ESPACIO = ' ' * 4

TIPOS = {
    'STRING': { 'tipo':'CharField' },
    'INTEGER': { 'tipo':'IntegerField', 'req_max_length' : False },
    'LONG': { 'tipo':'BigIntegerField', 'req_max_length' : False },
    'DECIMAL': { 'tipo':'DecimalField' , 'req_precision' : True },
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

    #Ajustes para campos que se convierten en Foreign key
    if tipoCampo == 'ForeignKey':
        if campo['__atributos']['refUser'] != '1':
            pass
            named_query = data_referencia[0][1]
            entidad_destino = [x for x in entidades if x['idObjeto'] == int( named_query['__atributos']['entidadFK'] ) ][0]['nombre']
            parametros += "'{0}'".format( entidad_destino )
        else:
            parametros += "settings.AUTH_USER_MODEL"
        parametros += ", on_delete = models.CASCADE"
        if 'obligatorio' in campo['__atributos'] and campo['__atributos']['obligatorio'] == '0':
            parametros += ", blank=True"

    #Ajuste de tipo cuando es incremental
    if 'incremental' in campo['__atributos'] and campo['__atributos']['incremental'] == '1':
        if tipoCampo in ['IntegerField','PositiveIntegerField','PositiveSmallIntegerField','SmallIntegerField']:
            tipoCampo = 'AutoField'
        elif tipoCampo == 'BigIntegerField' :
            tipoCampo = 'BigAutoField'

    if not ( 'req_max_length' in tipo and tipo['req_max_length'] == False):
        parametros += 'max_length = {0}'.format( campo['__atributos']['tamano'] )

    if 'req_precision' in tipo and tipo['req_precision'] == True:
        if parametros != '':
            parametros += ', '
        parametros += 'decimal_places = {0}'.format( campo['__atributos']['precision'] )

    if 'pk' in campo['__atributos'] and campo['__atributos']['pk'] == '1':
        if parametros != '':
            parametros += ', '
        parametros += 'primary_key=True'

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


    definicion = "{0}{1} = {2}.{3}({4})".format(ESPACIO, nombreCampo, dominio, tipoCampo, parametros )
    return definicion

def declaracionIndice(indice, entidad):
    campos = [ "'{0}'".format(x['nombre']) for x in indice['__listas']['camposWhere'] ]
    resultado = ESPACIO * 3 + "models.Index( fields=[ "
    resultado += ", ".join( campos )
    resultado += "])"
    return resultado

def declaracionIndiceUnico(indice, entidad):
    campos = [ "'{0}'".format(x['nombre']) for x in indice['__listas']['camposWhere'] ]
    resultado = ESPACIO * 3 + "[ "
    resultado += ", ".join( campos )
    resultado += "]"
    return resultado

def esCampoSuelto(campo):
    es_suelto = True
    if campo['__atributos']['pk'] == '1' and campo['nombre'].lower() == 'id' and campo['__atributos']['tipo'] == 'INTEGER' and campo['__atributos']['incremental'] == '1':
        es_suelto = False
    return es_suelto

def generarModelsPy(modelo):
    contenido = "\"\"\"\nDeficion de Modelos\n\"\"\"\nfrom django.conf import settings\nfrom django.db import models\nfrom django.urls import reverse\n\n"

    #incluye catalogos
    catalogos = modelo['__objetoRaiz']['__listas']['Catalogos']
    for catalogo in catalogos:
        nombreCatalogo = catalogo["nombre"].upper()
        valoresCatalogo = catalogo['__listas']['Valores']
        constantesCatalogos = [ "{2}_{0} = '{1}'".format(valorCatalogo['nombre'].upper(), valorCatalogo['nombre'], nombreCatalogo ) for valorCatalogo in valoresCatalogo ]
        listaConstantesCatalogos = [ ESPACIO + "({2}_{0} , '{1}')".format( valorCatalogo['nombre'].upper(), valorCatalogo['nombre'], nombreCatalogo ) for valorCatalogo in valoresCatalogo ]
        contenido += "\n".join(constantesCatalogos) + "\n"
        contenido += "{0} = (\n".format(nombreCatalogo)
        contenido += ",\n".join(listaConstantesCatalogos) + "\n"
        contenido += ")\n"

    #incluye Modelos
    entidades = modelo['__objetoRaiz']['__listas']['Entidades']
    for entidad in entidades:
        nombreEntidad = entidad['nombre']
        campos = entidad['__listas']['Campos']
        definicionesCampos = [ definicionCampoModel(campo,modelo) for campo in campos if esCampoSuelto(campo) ]
        campoId = [x for x in campos if x['__atributos']['pk'] == '1' ][0]
        indices = [x for x in entidad['__listas']['NamedQuieries'] if not( x['__atributos']['entidadFK'].isnumeric() ) and x['__atributos']['indiceUnico'] != '1' ]
        indicesUnicos = [x for x in entidad['__listas']['NamedQuieries'] if x['__atributos']['indiceUnico'] == '1' ]

        contenido += "\nclass {0}(models.Model):\n".format(nombreEntidad)
        #implementa campos
        contenido += "\n".join(definicionesCampos) + "\n"

        #implementa get_absolute_url
        contenido += "{0}def get_absolute_url(self):\n{0}{0}return reverse('{1}', args=[str(self.{2})])\n".format( ESPACIO , nombreEntidad.lower(), campoId['nombre'] )

        #implementa class Meta
        contenido += ESPACIO + "class Meta:\n{0}{0}verbose_name = '{1}'\n{0}{0}verbose_name_plural = '{1}s'\n".format( ESPACIO, nombreEntidad );
        if len(indices) > 0:
            declaracionesIndices = [ declaracionIndice(x, entidad) for x in indices ]
            contenido += ESPACIO * 2 + "indexes = [\n";
            contenido += ",\n".join( declaracionesIndices ) + "\n"
            contenido += ESPACIO * 2 + "]\n";
        if len(indicesUnicos) > 0:
            declaracionesIndicesUnicos = [ declaracionIndiceUnico(x, entidad) for x in indicesUnicos ]
            contenido += ESPACIO * 2 + "unique_together = [\n";
            contenido += ",\n".join( declaracionesIndicesUnicos ) + "\n"
            contenido += ESPACIO * 2 + "]\n";
    #incluye clase de au
    return contenido

def generarFormsPy(modelo):
    return ''

def generarAdminViewsPy(modelo):
    adminPages = modelo['__objetoRaiz']['__listas']['AdminPages']

    cruce_entidades = [ ( x['nombre'] , y['nombre'] ) for x in adminPages for y in x['__listas']['Inlines']  ]
    entidades = set ( [ x['nombre'] for x in adminPages ] + [ x[1] for x in cruce_entidades ] )
    contenido = "from app.models import {0}\nfrom django.contrib import admin\n\n".format( ", ".join(entidades) )

    for adminPage in adminPages:
        nombreAdminPage = adminPage['nombre']
        inlines = adminPage['__listas']['Inlines']

        contenido += "# admin.site.register({0})\n".format(nombreAdminPage)
        for inline in inlines:
            contenido += "class {0}{1}Inline(admin.TabularInline):\n{2}model = {0}\n".format( inline['nombre'], nombreAdminPage, ESPACIO)
            list_display = [ "'{0}'".format(x['nombre']) for x in inline['__listas']['CamposDespliegue'] ]
            if len(list_display) > 0:
                contenido += "{0}list_display = ({1})\n".format( ESPACIO, ", ".join(list_display) )

        contenido += "@admin.register({0})\nclass {0}Admin(admin.ModelAdmin):\n".format( nombreAdminPage )
        list_display = [ "'{0}'".format(x['nombre']) for x in adminPage['__listas']['CamposDespliegue'] ]
        list_inlines = [ "{0}{1}Inline".format(x['nombre'], nombreAdminPage) for x in adminPage['__listas']['Inlines'] ]
        if len(list_display) == 0 and len(list_inlines) == 0:
            contenido += "{0}pass\n".format( ESPACIO )
        if len(list_display) > 0:
            contenido += "{0}list_display = ({1})\n".format( ESPACIO, ", ".join(list_display) )
        if len(list_inlines) > 0:
            contenido += "{0}inlines = [{1}]\n".format( ESPACIO, ", ".join(list_inlines) )
        contenido += "\n"

    return contenido

def generarSerializersPy(modelo):
    entidades = modelo['__objetoRaiz']['__listas']['Entidades']
    lista_entidades = [ x['nombre'] for x in entidades ]

    # importa todas las entidades
    contenido = ''
    contenido += "from rest_framework import serializers\nfrom app.models import {0}\n\n".format( ", ".join( lista_entidades ) )

    #definicion de serializadores
    for entidad in entidades:
        contenido += "class {1}Serializer(serializers.ModelSerializer):\n{0}class Meta:\n{0}{0}model = {1}\n\n".format(ESPACIO, entidad['nombre'])

    return contenido

def generarViewsPy(modelo):
    contenido = ''

    entidades = modelo['__objetoRaiz']['__listas']['Entidades']

    lista_entidades = [ x['nombre'] for x in entidades ]
    contenido += "from rest_framework import generics\n#from rest_framework import viewsets\nfrom rest_framework.authentication import SessionAuthentication, TokenAuthentication\nfrom rest_framework.permissions import IsAuthenticated\nfrom app.models import {0}\n".format( ", ".join( lista_entidades ) )

    lista_entidades = [ "{0}Serializer".format(x['nombre']) for x in entidades ]
    contenido += "from app.serializers import {0}\n\n".format( ", ".join( lista_entidades ) )

    #ViewSet para API
    #lista_entidades = [ "#class {1}ViewSet(viewsets.ModelViewSet):\n#{0}authentication_classes = [SessionAuthentication, BasicAuthentication]\n#{0}permission_classes = [IsAuthenticated]\n{0}queryset = {1}.objects.all()\n#{0}serializer_class = {1}Serializer\n".format(ESPACIO, x['nombre']) for x in entidades ]
    #contenido += "{0}\n".format( "\n".join( lista_entidades ) )
    for entidad in entidades:
        contenido += "\nclass {1}CRUD(generics.RetrieveUpdateDestroyAPIView):\n{0}authentication_classes = [SessionAuthentication, BasicAuthentication]\n{0}permission_classes = [IsAuthenticated]\n{0}queryset = {1}.objects.all()\n{0}serializer_class = {1}Serializer\n".format(ESPACIO, entidad['nombre'])
        finders = [finder for finder in entidad['__listas']['NamedQuieries'] if 'finder' in finder['__atributos'] and finder['__atributos']['finder'] is not None and len(finder['__atributos']['finder']) > 0 ]
        for finder in finders:
            parametros = [ parametro for parametro in finder['__listas']['camposWhere'] ]
            lista_lectura_parametros = [ "{0}{0}{1} = self.kwargs['{1}']".format(ESPACIO, parametro['nombre'] ) for parametro in parametros]
            lista_parametros = [ "{0} = {0}".format( parametro['nombre'] ) for parametro in parametros]
            contenido += "class {1}{2}List(generics.ListAPIView):\n{0}authentication_classes = [SessionAuthentication, BasicAuthentication]\n{0}permission_classes = [IsAuthenticated]\n{0}serializer_class = {1}Serializer\n{0}def get_queryset(self):\n{3}\n{0}{0}return {1}.objects.filter({4})\n\n".format(ESPACIO, entidad['nombre'], finder['__atributos']['finder'].capitalize(), '\n'.join(lista_lectura_parametros), ', '.join(lista_parametros))

    return contenido

def generarPryUrlsPy(modelo):
    contenido = """
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('app.urls', namespace='app')),
    url(r'^api-token-auth/', views.obtain_auth_token)
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    """
    return contenido

def generarAppUrlsPy(modelo):
    contenido = ''

    entidades = modelo['__objetoRaiz']['__listas']['Entidades']

    rutas = {}

    for entidad in entidades:
        rutas[ entidad['nombre'].lower() + '/<int:pk>/' ] = entidad['nombre'] + 'CRUD'
        finders = [finder for finder in entidad['__listas']['NamedQuieries'] if 'finder' in finder['__atributos'] and finder['__atributos']['finder'] is not None and len(finder['__atributos']['finder']) > 0 ]
        for finder in finders:
            rutas [ finder['__atributos']['endPoint'] ] = entidad['nombre'] + finder['__atributos']['finder'].capitalize() + 'List'

    contenido += "from django.conf.urls import url\nfrom django.urls import path\nfrom rest_framework import routers\nfrom rest_framework.urlpatterns import format_suffix_patterns\nfrom app.views import {0}\n\n".format( ", ".join( set(rutas.values()) ) )

    contenido += "router = routers.DefaultRouter()\n\n"

    keys_ordenados = list( rutas.keys() )
    keys_ordenados.sort( reverse = True )

    lista_entidades = [ "{0}path('{1}', {2}.as_view())".format(ESPACIO, clave, rutas[clave] ) for clave in keys_ordenados ]
    contenido += "urlpatterns = [\n{0}\n]".format(",\n".join(lista_entidades))

    contenido += "\n\nurlpatterns = format_suffix_patterns(urlpatterns)"

    return contenido

def generarInitSequence(modelo):
    contenido = """
mkdir {0}_env
cd {0}_env

rem virtualenv .env
rem pip install "Django >= 1.9, < 1.10"
rem pip install djangorestframework

django-admin startproject {0}

mkdir log
mkdir {0}\db

cd {0}
python manage.py startapp app

    """.format(modelo['nombre'].lower())
    return contenido

def generarSettingsPy(modelo):
    contenido = """
...

INSTALLED_APPS = [
...
    'app',
    'rest_framework',
    'rest_framework.authtoken',
]
...
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
...
    """
    return contenido

def generarModelo(modelo):

    resultado = { 'archivos' : [ { 'path':'Secuencia init',     'contenido': generarInitSequence(modelo) },
                                 { 'path':'project/settings.py','contenido': generarSettingsPy(modelo) },
                                 { 'path':'app/models.py',      'contenido': generarModelsPy(modelo) },
                                 { 'path':'app/admin.py',       'contenido': generarAdminViewsPy(modelo) },
                                 { 'path':'app/serializers.py', 'contenido': generarSerializersPy(modelo) },
                                 { 'path':'app/forms.py',       'contenido': generarFormsPy(modelo) },
                                 { 'path':'app/views.py',       'contenido': generarViewsPy(modelo) },
                                 { 'path':'project/urls.py',    'contenido': generarPryUrlsPy(modelo) },
                                 { 'path':'app/urls.py',        'contenido': generarAppUrlsPy(modelo) },
                                 ]}

    return resultado
