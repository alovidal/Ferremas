from django.urls import path
from ferremas import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tienda", views.tienda, name="tienda"),
    path("login", views.login, name="login"),
    path("carro", views.carro, name="carro"),
    path("seguimiento", views.seguimiento, name="seguimiento"),
]
