from django.shortcuts import render,redirect,get_object_or_404
from .models import *

# Create your views here.


def verOrdenes(request):
    pedidos = Pedido.objects.all()
    detalles = DetallePedido.objects.all()
    ordenes = Ordenes.objects.all()
    productos = Producto.objects.all()
    context = {
        "pedidos":pedidos,
        "detalles":detalles,
        "ordenes":ordenes,
        "productos":productos
    }
    return render(request, "pages/verordenes.html", context)

def productosDisponibles(request):
    productos = Producto.objects.all()
    context = {
        "productos":productos
    }
    return render(request, "pages/productosdisponibles.html", context)

def gestionarPedidos(request):
    productos = Producto.objects.all()
    solicitudes = SolicitudPedido.objects.all()
    ordenes = Ordenes.objects.all()
    pedidos = Pedido.objects.all()
    detalles = DetallePedido.objects.all()
    context = {
        "productos":productos,
        "solicitudes":solicitudes,
        "ordenes":ordenes,
        "pedidos":pedidos,
        "detalles":detalles
    }
    return render(request, "pages/gestionarPedidos.html", context)

def Aceptar(request):
    if request.method == "POST":
        try:
            # Extraer el ID del cuerpo de la solicitud
            id_soli = request.POST.get('idSolicitud', None)
            
            if id_soli:
                soli = SolicitudPedido.objects.get(idSolicitud = id_soli)
                estado_soli = EstadoSolicitudPedido.objects.get(descripcion = 'En espera')

                soli.estado = estado_soli
                soli.save()

                estado_orden = EstadoOrden.objects.get(descripcion = 'En espera')
                orden = Ordenes(
                    solicitudPedido=soli,
                    estadoOrden=estado_orden
                )
                orden.save()

                return redirect(gestionarPedidos)
            
            #segunda funcion
            id_orden = request.POST.get('idOrden', None)
            
            if id_orden:
                orden = Ordenes.objects.get(idOrden = id_orden)
                estado_orden = EstadoOrden.objects.get(descripcion = 'Entregado')

                orden.estadoOrden = estado_orden
                orden.save()

                soli = orden.solicitudPedido
                estado_soli = EstadoSolicitudPedido.objects.get(descripcion = 'Cerrado')
                soli.estado = estado_soli
                soli.save()

                return redirect(gestionarPedidos)

            #tercera funcion
            id_pedido = request.POST.get('idPedido', None)

            if id_pedido:
                pedido = Pedido.objects.get(idPedido = id_pedido)
                estado_pedido = EstadoPedido.objects.get(descripcion = 'Entregado')

                pedido.estado = estado_pedido
                pedido.save()

                return redirect(gestionarPedidos)
        except:
            productos = Producto.objects.all()
            solicitudes = SolicitudPedido.objects.all()
            context = {
                "productos":productos,
                "solicitudes":solicitudes,
                "mensaje":"Error"
            }
            return render(request, "pages/gestionarPedidos.html", context)
    else:
        productos = Producto.objects.all()
        solicitudes = SolicitudPedido.objects.all()
        context = {
            "productos":productos,
            "solicitudes":solicitudes,
            "mensaje":"Error"
        }
        return render(request, "pages/gestionarPedidos.html", context)
    
def Rechazar(request):
    if request.method == "POST":
        try:
            # Extraer el ID del cuerpo de la solicitud
            id_soli = request.POST.get('idSolicitud', None)
            
            if id_soli:
                soli = SolicitudPedido.objects.get(idSolicitud = id_soli)
                estado_soli = EstadoSolicitudPedido.objects.get(descripcion = 'Rechazado')

                soli.estado = estado_soli
                soli.save()

                orden = EstadoOrden.objects.get(solicitudPedido = soli)
                estado_orden = EstadoOrden.objects.get(descripcion = 'Rechazado')
                orden.estadoOrden = estado_orden
                orden.save()

                return redirect(gestionarPedidos)
            
            #segunda funcion
            id_orden = request.POST.get('idOrden', None)
            
            if id_orden:
                orden = Ordenes.objects.get(idOrden = id_orden)
                estado_orden = EstadoOrden.objects.get(descripcion = 'Rechazado')

                orden.estadoOrden = estado_orden
                orden.save()

                soli = orden.solicitudPedido
                estado_soli = EstadoSolicitudPedido.objects.get(descripcion = 'Rechazado')
                soli.estado = estado_soli
                soli.save()

                return redirect(gestionarPedidos)
            
            #tercera funcion
            id_pedido = request.POST.get('idPedido', None)

            if id_pedido:
                pedido = Pedido.objects.get(idPedido = id_pedido)
                estado_pedido = EstadoPedido.objects.get(descripcion = 'Rechazado')

                pedido.estado = estado_pedido
                pedido.save()

                return redirect(gestionarPedidos)

        except:
            productos = Producto.objects.all()
            solicitudes = SolicitudPedido.objects.all()
            context = {
                "productos":productos,
                "solicitudes":solicitudes,
                "mensaje":"Error"
            }
            return render(request, "pages/gestionarPedidos.html", context)
    else:
        productos = Producto.objects.all()
        solicitudes = SolicitudPedido.objects.all()
        context = {
            "productos":productos,
            "solicitudes":solicitudes,
            "mensaje":"Error"
        }
        return render(request, "pages/gestionarPedidos.html", context)

# Listar productos
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'pages/crudProductos/desplegar.html', {'productos': productos})

# Agregar producto
def agregar_producto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio = float(request.POST['precio'])
        stock = int(request.POST['stock'])
        marca = MarcaProductos.objects.get(idMarca=request.POST['marca'])
        categoria = CategoriaProductos.objects.get(idCategoria=request.POST['categoria'])
        imagen = request.FILES.get('imagen', None)

        Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            marca=marca,
            categoria=categoria,
            imagen=imagen
        )
        return redirect('listar-prod')
    marcas = MarcaProductos.objects.all()
    categorias = CategoriaProductos.objects.all()
    return render(request, 'pages/crudProductos/agregar_actualizar.html', {'marcas': marcas, 'categorias': categorias})

# Actualizar producto
def actualizar_producto(request, idProducto):
    producto = get_object_or_404(Producto, idProducto=idProducto)
    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST['descripcion']
        producto.precio = float(request.POST['precio'])
        producto.stock = int(request.POST['stock'])
        producto.marca = MarcaProductos.objects.get(idMarca=request.POST['marca'])
        producto.categoria = CategoriaProductos.objects.get(idCategoria=request.POST['categoria'])
        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']
        producto.save()
        return redirect('listar-prod')
    marcas = MarcaProductos.objects.all()
    categorias = CategoriaProductos.objects.all()
    return render(request, 'pages/crudProductos/agregar_actualizar.html', {'producto': producto, 'marcas': marcas, 'categorias': categorias})

# Eliminar producto
def eliminar_producto(request, idProducto):
    producto = get_object_or_404(Producto, idProducto=idProducto)
    producto.delete()
    return redirect('listar-prod')