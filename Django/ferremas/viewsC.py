from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages



# Vista de login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirigir dependiendo si el usuario es administrador o normal
            if user.is_superuser:
                return redirect('gestionarUsuarios')  # Redirigir a gestionarUsuarios.html para admin
            else:
                return redirect('tienda')  # Redirigir a tienda.html para usuarios normales
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'pages/login.html')


# Vista de registro de usuario
def register_view(request):
    if request.method == 'POST':
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
            return redirect('register')

        # Verificar si el correo ya está registrado
        if User.objects.filter(username=email).exists():
            messages.error(request, 'El correo ya está registrado.')
            return redirect('register')

        # Crear el usuario
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = full_name.split()[0]  # Asignar el primer nombre al campo first_name
        user.last_name = " ".join(full_name.split()[1:])  # Asignar el apellido al campo last_name
        user.save()

        # Crear el perfil de usuario
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

    return render(request, 'pages/register.html')


# Vista de gestión de usuarios (solo para administradores)
@login_required
def gestionarUsuarios_view(request):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('tienda')  # Redirigir a tienda si no es administrador

    users = User.objects.all()
    user_profiles = UserProfile.objects.all()

    context = {
        'users': users,
        'user_profiles': user_profiles
    }

    return render(request, "pages/gestionarUsuarios.html", context)


# Vista para eliminar usuario (solo para administradores)
def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Verificar si el usuario está intentando eliminarse a sí mismo o eliminar a un admin
    if user == request.user:
        messages.error(request, 'No puedes eliminar tu propio usuario.')
        return redirect('gestionarUsuarios')

    if user.is_superuser:
        messages.error(request, 'No puedes eliminar a un usuario administrador.')
        return redirect('gestionarUsuarios')

    # Eliminar el perfil del usuario, si existe
    try:
        user_profile = UserProfile.objects.get(user=user)
        user_profile.delete()
    except UserProfile.DoesNotExist:
        pass

    # Eliminar el usuario
    user.delete()
    messages.success(request, '')
    return redirect('gestionarUsuarios')

#editar usuario
def editar_usuario(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        interests = request.POST.get('interests')

        # Obtener el usuario y su perfil
        user = get_object_or_404(User, id=user_id)
        user_profile = get_object_or_404(UserProfile, user=user)

        # Actualizar los datos del usuario
        user.username = email  # O mantener el username anterior si no se desea actualizar
        user.email = email

        # Descomponer el nombre completo en nombre y apellido (opcional)
        name_parts = full_name.split()
        if name_parts:
            user.first_name = name_parts[0]  # Primer nombre
            user.last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""  # Apellidos
        user.save()

        # Actualizar el nombre completo en el perfil de usuario
        user_profile.full_name = full_name
        user_profile.phone = phone
        user_profile.interests = interests
        user_profile.save()

        # Responder con los datos actualizados del usuario
        updated_user_data = {
            'user_id': user.id,
            'full_name': user_profile.full_name,
            'email': user.email,
            'phone': user_profile.phone,
            'interests': user_profile.interests,
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),  # Formato de fecha
        }

        return JsonResponse({'success': True, 'message': 'Usuario actualizado exitosamente.', 'user': updated_user_data})

    return JsonResponse({'success': False, 'message': 'Error al actualizar el usuario.'})