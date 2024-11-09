from django.urls import path
from . import viewsC


urlpatterns = [
    path('login/', viewsC.login_view, name='login'),
    path('register/', viewsC.register_view, name='register'),
    path('gestionarUsuarios/', viewsC.gestionarUsuarios_view, name='gestionarUsuarios'),
    # Otros paths
]