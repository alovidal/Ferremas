from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile

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
    return render(request, 'login.html')

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
        terms_accepted = 'terms' in request.POST  # Verificar si el usuario aceptó los términos

        # Validar si las contraseñas coinciden
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('register')

        # Validar si se aceptaron los términos
        if not terms_accepted:
            messages.error(request, 'Debes aceptar los términos y condiciones.')
            return redirect('register')

        try:
            # Crear el usuario
            user = User.objects.create_user(username=email, password=password, email=email)
            user.first_name = full_name  # Guardar el nombre completo
            user.save()

            # Crear el perfil del usuario
            user_profile = UserProfile.objects.create(
                user=user,
                full_name=full_name,
                phone=phone,
                interests=interests,
                terms_accepted=terms_accepted
            )
            user_profile.save()

            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Ocurrió un error: {e}')
            return redirect('register')

    return render(request, "pages/register.html")