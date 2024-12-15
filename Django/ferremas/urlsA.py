from django.urls import path
from ferremas import viewsA

urlpatterns = [
    path("", viewsA.index, name="index"),
    path("tienda", viewsA.tienda, name="tienda"),
    path("login", viewsA.login, name="login"),
    path("carro", viewsA.carro, name="carro"),
    path("seguimiento", viewsA.seguimiento, name="seguimiento"),
    path("contacto", viewsA.contacto, name="contacto"),
    path("divisas", viewsA.divisas, name="divisas"),
    path("est", viewsA.estadoPedido, name="estadoPedido")
]
