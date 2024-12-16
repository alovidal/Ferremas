from django.urls import path
from ferremas import viewsN

urlpatterns = [
    path("catalogo", viewsN.catalogo, name="catalogo"),
    path("pago", viewsN.pago, name="pago"),
    path("procesa_pedido", viewsN.procesa_pedido, name="procesa_pedido"),
    path('transaccion_completa',viewsN.transaccion_completa ,name='transaccion_completa'),
    path("load_carrito", viewsN.load_carrito, name="load_carrito"),
]