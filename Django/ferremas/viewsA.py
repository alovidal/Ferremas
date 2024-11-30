from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def index(request):
    context = {}
    return render(request, "pages/index.html", context)

def tienda(request):
    context = {}
    return render(request, "pages/tienda.html", context)

def login(request):
    context = {}
    return render(request, "pages/login.html", context)

def carro(request):
    context = {}
    return render(request, "pages/carro.html", context)

def seguimiento(request):
    context = {}        
    return render(request, "pages/seguimiento.html", context)

def contacto(request):
    context = {}
    return render(request, "pages/contacto.html", context)

def divisas(request):
    context = {}        
    return render(request, "pages/divisas.html", context)

def estadoPedido(request):
    pedidos = Pedido.objects.all()
    estados = EstadoPedido.objects.all()

    if request.method == "POST":
        pedido_id = request.POST.get("pedido_id")
        nuevo_estado_id = request.POST.get(f"estado_{pedido_id}")

        # Actualizar el estado del pedido
        try:
            pedido = Pedido.objects.get(idPedido=pedido_id)
            nuevo_estado = EstadoPedido.objects.get(idEstado=nuevo_estado_id)
            pedido.estado = nuevo_estado
            pedido.save()
        except Pedido.DoesNotExist:
            print("El pedido no existe.")
        except EstadoPedido.DoesNotExist:
            print("El estado no existe.")

        return redirect("estadoPedido")

    context = {
        "pedidos": pedidos,
        "estados": estados,
    }
    return render(request, "pages/estadoPedido.html", context)