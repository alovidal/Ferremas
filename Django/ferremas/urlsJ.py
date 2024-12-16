from django.urls import path
from ferremas import viewsJ
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ver-ordenes/', viewsJ.verOrdenes, name='ver-ordenes'),
    path('productos-disponibles/', viewsJ.productosDisponibles, name='productos-disponibles'),
    path('gestionar-pedidos/', viewsJ.gestionarPedidos, name='gestionar-pedidos'),
    path('aceptar',viewsJ.Aceptar, name='aceptar'),
    path('rechazar',viewsJ.Rechazar, name='rechazar'),
    path('listar-prod/', viewsJ.listar_productos, name='listar-prod'),
    path('agregar-prod/', viewsJ.agregar_producto, name='agregar-prod'),
    path('actualizar-prod/<int:idProducto>/', viewsJ.actualizar_producto, name='actualizar-prod'),
    path('eliminar-prod/<int:idProducto>/', viewsJ.eliminar_producto, name='eliminar-prod'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)