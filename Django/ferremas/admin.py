from django.contrib import admin
from .models import *

#inicio con admin y gestion de otros usuarios
# Register your models here.
admin.site.register(Usuario)
admin.site.register(MarcaProductos)
admin.site.register(CategoriaProductos)
admin.site.register(Producto)
admin.site.register(EstadoPedido)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(EstadoSolicitudPedido)
admin.site.register(SolicitudPedido)
admin.site.register(EstadoOrden)
admin.site.register(Ordenes)
admin.site.register(TipoInforme)
admin.site.register(Informe)
admin.site.register(Pagos)
admin.site.register(Factura)
admin.site.register(Divisas)  