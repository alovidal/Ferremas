from django.urls import path
from . import viewsC


urlpatterns = [
    path('login/', viewsC.login_view, name='login'),
    path('register/', viewsC.register_view, name='register'),
    path('gestionarUsuarios/', viewsC.gestionarUsuarios_view, name='gestionarUsuarios'),
    path('eliminar_usuario/<int:user_id>/', viewsC.eliminar_usuario, name='eliminar_usuario'),
    path('editar_usuario/', viewsC.editar_usuario, name='editar_usuario'),
    # Otros paths
]