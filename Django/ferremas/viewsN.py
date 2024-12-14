import requests
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from transbank.webpay.webpay_plus.transaction import Transaction

# Create your views here.
api_url = "http://127.0.0.1:8000/api/productos/"

def catalogo(request):
    try:
        # Solicitud a la api
        response = requests.get(api_url)
        response.raise_for_status()
        productos = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los productos: {e}")
        productos = []

    print("Productos: ", productos)
    context = {
        "productos": productos
    }
    return render(request, "pages/catalogo.html", context)

def pago(request): 
    context = {}
    return render(request, "pages/pago.html", context)

def iniciar_transaccion(request):
    if request.method == "POST":
        try:
            buy_order = "orden123"
            session_id = "sesion123"
            amount = 10000 
            return_url = "http://127.0.0.1:8000/webpay/completado/" 

            # Crear transacción
            response = Transaction.create(buy_order, session_id, amount, return_url)
            
            return JsonResponse({
                "url": response.get("url"),
                "token": response.get("token")
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)