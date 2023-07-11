from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('registrar-usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('activar-usuario/<int:user_id>/', views.activar_usuario, name='activar_usuario'),
    path('recuperar-contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path('cambiar-contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'), 

    path('dashboard/', views.listar_proyectos, name='dashboard'),

]
