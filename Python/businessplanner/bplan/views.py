from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm as UserCreationForm
from .forms import CustomPasswordChangeForm as PasswordChangeForm
from .forms import CustomLoginForm as LoginForm

from .models import Proyecto

# Create your views here.

User = get_user_model()

def index(request):
    return render(request, 'bplan/index.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirige a la página del panel de control
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'bplan/iniciar_sesion.html', {'form': form})

def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            
            user = form.save(commit=False)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            
            messages.success(request, f'¡Registro exitoso! Ahora puedes iniciar sesión como {user.username}.')
            return redirect('iniciar_sesion')
    else:
        form = UserCreationForm()
    return render(request, 'bplan/registrar_usuario.html', {'form': form})

def activar_usuario(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, 'Su cuenta ha sido activada. Ahora puede iniciar sesión.')
    return redirect('iniciar_sesion')

def recuperar_contrasena(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            # Código para enviar correo con enlace de cambio de contraseña con una clave temporal
            messages.success(request, 'Se ha enviado un correo con instrucciones para cambiar su contraseña.')
            return redirect('iniciar_sesion')
        except User.DoesNotExist:
            messages.error(request, 'No se encontró ningún usuario asociado a este correo electrónico.')
    return render(request, 'bplan/recuperar_contrasena.html')

@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Su contraseña ha sido cambiada exitosamente.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'bplan/cambiar_contrasena.html', {'form': form})

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('index')

@login_required
def listar_proyectos(request):
    proyectos = Proyecto.objects.filter(userPropietario=request.user)
    return render(request, 'bplan/listar_proyectos.html', {'proyectos': proyectos})