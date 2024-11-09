from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.shortcuts import get_object_or_404, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirigir a la página principal
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'pages/login.html')

def register_view(request):
    context = {}
    return render(request, "pages/register.html", context)

def gestionarUsuarios_view(request):

    users = User.objects.all()  
    user_profiles = UserProfile.objects.all()  

    context = {
        'users': users,
        'user_profiles': user_profiles
    }
    
    return render(request, "pages/gestionarUsuarios.html", context)

#Register
def register_view(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        interests = request.POST['interests']
        terms_accepted = 'terms' in request.POST

        # Verificar si las contraseñas coinciden
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('register')  # Redirigir a la página de registro

        # Verificar que el usuario no exista
        if User.objects.filter(username=email).exists():
            messages.error(request, 'El correo ya está registrado.')
            return redirect('register')  # Redirigir si el correo ya está en uso

        # Crear un nuevo usuario
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = full_name.split()[0]  # Asignar el primer nombre al campo first_name
        user.last_name = " ".join(full_name.split()[1:])  # Asignar el apellido al campo last_name
        user.save()

        # Crear un perfil de usuario
        user_profile = UserProfile.objects.create(
            user=user,
            full_name=full_name,
            phone=phone,
            interests=interests,
            terms_accepted=terms_accepted
        )

        # Mensaje de éxito
        messages.success(request, 'Usuario registrado exitosamente.')
        return redirect('login')  # Redirigir al login

    return render(request, 'pages/register.html')  # Si no es POST, simplemente renderizar el formulario de registro

#Eliminar Usuario

def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Eliminar perfil relacionado si existe
    try:
        user_profile = UserProfile.objects.get(user=user)
        user_profile.delete()
    except UserProfile.DoesNotExist:
        pass
    
    # Eliminar el usuario
    user.delete()
    return redirect('gestionarUsuarios')  # Redirigir a la lista de usuarios