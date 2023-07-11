from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.

ESTADOS_ACTIVO = 'ACTIVO'
ESTADOS_INACTIVO = 'INACTIVO'
ESTADOS = (
    (ESTADOS_ACTIVO , 'ACTIVO'),
    (ESTADOS_INACTIVO , 'INACTIVO')
)
TIPO_FODA_FORTALEZA = 'FORTALEZA'
TIPO_FODA_OPORTUNIDAD = 'OPORTUNIDAD'
TIPO_FODA_DEBILIDAD = 'DEBILIDAD'
TIPO_FODA_AMENAZA = 'AMENAZA'
TIPO_FODA = (
    (TIPO_FODA_FORTALEZA , 'FORTALEZA'),
    (TIPO_FODA_OPORTUNIDAD , 'OPORTUNIDAD'),
    (TIPO_FODA_DEBILIDAD , 'DEBILIDAD'),
    (TIPO_FODA_AMENAZA , 'AMENAZA')
)
TIPO_OBJETIVO_LARGO_PLAZO = 'LARGO_PLAZO'
TIPO_OBJETIVO_CORTO_PLAZO = 'CORTO_PLAZO'
TIPO_OBJETIVO = (
    (TIPO_OBJETIVO_LARGO_PLAZO , 'LARGO_PLAZO'),
    (TIPO_OBJETIVO_CORTO_PLAZO , 'CORTO_PLAZO')
)

class CoreValueTemplate(models.Model):
    descripcion = models.CharField(max_length = 16, help_text="null", db_column="DESCRIPCION")
    def get_absolute_url(self):
        return reverse('corevaluetemplate', args=[str(self.id)])
    class Meta:
        db_table = 'CRVLTMPLT'
        verbose_name = 'CoreValueTemplate'
        verbose_name_plural = 'CoreValueTemplates'

class Proyecto(models.Model):
    userPropietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, help_text="null", db_column="USER_PROPIETARIO")
    nombreProyecto = models.CharField(max_length = 32, help_text="Nombre de Proyecto de Plan de Negocio", db_column="NOMBRE_PROYECTO")
    fechaInicio = models.DateField(null=True, help_text="null", db_column="FECHA_INICIO")
    fechaInicioReal = models.DateField(null=True, help_text="null", db_column="FECHA_INICIO_REAL")
    estado = models.CharField(max_length = 16, choices = ESTADOS, help_text="null", db_column="ESTADO")
    def get_absolute_url(self):
        return reverse('proyecto', args=[str(self.id)])
    class Meta:
        db_table = 'PRYCT'
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        indexes = [
            models.Index( fields=[ 'userPropietario', 'estado'])
        ]

class Delegacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank=True, null=True, help_text="null", db_column="ID_USUARIO")
    emailDelegado = models.EmailField(max_length = 32, help_text="null", db_column="EMAIL_DELEGADO")
    puedeVer = models.BooleanField(help_text="null", db_column="PUEDE_VER")
    puedeModificar = models.BooleanField(help_text="null", db_column="PUEDE_MODIFICAR")
    def get_absolute_url(self):
        return reverse('delegacion', args=[str(self.id)])
    class Meta:
        db_table = 'DLGCN'
        verbose_name = 'Delegacion'
        verbose_name_plural = 'Delegacions'
        indexes = [
            models.Index( fields=[ 'usuario']),
            models.Index( fields=[ 'emailDelegado'])
        ]
class CicloProyecto(models.Model):
    proyecto = models.ForeignKey('Proyecto', on_delete = models.CASCADE, help_text="null", db_column="ID_PROYECTO")
    nombreCiclo = models.CharField(max_length = 16, help_text="null", db_column="NOMBRE_CICLO")
    estado = models.CharField(max_length = 16, choices = ESTADOS, help_text="null", db_column="ESTADO")
    fechaVision = models.DateField(help_text="null", db_column="FECHA_VISION")
    vision = models.TextField(max_length = 2048, null=True, help_text="null", db_column="VISION")
    mision = models.TextField(max_length = 2048, null=True, help_text="null", db_column="MISION")
    def get_absolute_url(self):
        return reverse('cicloproyecto', args=[str(self.id)])
    class Meta:
        db_table = 'CCLPRYCT'
        verbose_name = 'CicloProyecto'
        verbose_name_plural = 'CicloProyectos'
        indexes = [
            models.Index( fields=[ 'proyecto', 'estado'])
        ]

class ItemFoda(models.Model):
    ciclo = models.ForeignKey('CicloProyecto', on_delete = models.CASCADE, help_text="null", db_column="ID_CICLO")
    tipoFoda = models.CharField(max_length = 16, choices = TIPO_FODA, help_text="null", db_column="TIPO_FODA")
    enunciado = models.TextField(max_length = 512, help_text="null", db_column="ENUNCIADO")
    orden = models.IntegerField(help_text="null", db_column="ORDEN")
    def get_absolute_url(self):
        return reverse('itemfoda', args=[str(self.id)])
    class Meta:
        db_table = 'ITEM_FODA'
        verbose_name = 'ItemFoda'
        verbose_name_plural = 'ItemFodas'

class CoreValue(models.Model):
    ciclo = models.ForeignKey('CicloProyecto', on_delete = models.CASCADE, help_text="null", db_column="ID_CICLO")
    descripcion = models.CharField(max_length = 16, help_text="null", db_column="DESCRIPCION")
    orden = models.IntegerField(help_text="null", db_column="ORDEN")
    def get_absolute_url(self):
        return reverse('corevalue', args=[str(self.id)])
    class Meta:
        db_table = 'CRVL'
        verbose_name = 'CoreValue'
        verbose_name_plural = 'CoreValues'

class Objetivo(models.Model):
    ciclo = models.ForeignKey('CicloProyecto', on_delete = models.CASCADE, help_text="null", db_column="ID_CICLO")
    tipoObjetivo = models.CharField(max_length = 16, choices = TIPO_OBJETIVO, help_text="null", db_column="TIPO_OBJETIVO")
    target = models.CharField(max_length = 64, help_text="null", db_column="TARGET")
    cantidad = models.DecimalField(max_digits = 8, decimal_places = 2, help_text="null", db_column="CANTIDAD")
    unidadCantidad = models.CharField(max_length = 32, help_text="null", db_column="UNIDAD_CANTIDAD")
    orden = models.IntegerField(help_text="null", db_column="ORDEN")
    fechaValidacion = models.DateField(null=True, help_text="null", db_column="FECHA_VALIDACION")
    def get_absolute_url(self):
        return reverse('objetivo', args=[str(self.id)])
    class Meta:
        db_table = 'OBJTIV'
        verbose_name = 'Objetivo'
        verbose_name_plural = 'Objetivos'
        indexes = [
            models.Index( fields=[ 'ciclo', 'tipoObjetivo'])
        ]
