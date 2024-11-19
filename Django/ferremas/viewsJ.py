from django.shortcuts import render
from .models import *

# Create your views here.


def verordenes(request):
    pedidos = Pedido.objects.all()
    detalles = DetallePedido.objects.all()
    ordenes = Ordenes.objects.all()
    context = {
        "pedidos":pedidos,
        "detalles":detalles,
        "ordenes":ordenes
    }
    return render(request, "pages/verordenes.html", context)