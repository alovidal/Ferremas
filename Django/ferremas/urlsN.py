from django.urls import path
from ferremas import viewsN

urlpatterns = [
    path("catalogo", viewsN.catalogo, name="catalogo"),
    path("pago", viewsN.pago, name="pago"),
    
]