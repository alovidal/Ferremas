from datetime import date
import json
import requests
from django.shortcuts import redirect, render
from .models import *
from django.http import JsonResponse
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
from django.conf import settings
from django.contrib.auth.decorators import login_required

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

    context = {
        "productos": productos
    }
    return render(request, "pages/catalogo.html", context)

@login_required
def pago(request):
    if not request.user.is_authenticated:
        context = {}
        return render(request, "pages/login.html", context)
    else:
        context = {}
        return render(request, "pages/pago.html", context)

def load_carrito(request):
    if request.method == "POST":
        try:
            if 'carrito_data' in request.session:
                del request.session['carrito_data']
            
            data = json.loads(request.body)
            print("Data recibida", data)
            request.session['carrito_data'] = data
            
            datosObtenidos = request.session.get('carrito_data')
            print("Datos obtenidos: ", datosObtenidos)
            return JsonResponse({"message": "Productos recibidos correctamente"})
        except Exception as e:
            print("Error al recuperar el carrito", e)
    else:
        return JsonResponse({"message": "Metodo no es POST"})

def procesa_pedido(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        telefono = request.POST.get("telefono")
        direccion = request.POST.get("direccion")
        metodo_pago = request.POST.get("metodo-pago") 
        print(f"Método de pago seleccionado: {metodo_pago}")
        totalP = 0
        
        # Se recupera el carrito
        carrito_data = request.session.get('carrito_data')
        print("Carrito data recuperada:", carrito_data)
        
        if carrito_data and 'items' in carrito_data:
            # Iteramos sobre los items del carrito
            for item in carrito_data['items']:
                totalP += item['precioTotal']  # Usamos precioTotal en lugar de precio
        else:
            return JsonResponse({"error": "No hay productos en el carrito"}, status=400)

        # Guardamos los datos del usuario en la sesión
        data_usuario = {
            "correo": correo,
            "direccion": direccion,
            "telefono": telefono,
            "total": totalP
        }
        request.session['data_usuario'] = data_usuario

        if metodo_pago == "webpay":
            try:
                transaction = Transaction()
                transaction.commerce_code = settings.TRANSBANK_COMMERCE_CODE
                transaction.api_key = settings.TRANSBANK_API_KEY
                transaction.integration_type = IntegrationType.TEST 

                response = transaction.create(
                    buy_order='order12345',
                    session_id='session-'+correo,
                    amount=totalP,
                    return_url='http://127.0.0.1:8000/transaccion_completa'
                )

                print("Respuesta de WebPay:", response)
                return redirect(response['url'] + '?token_ws=' + response['token'])
            except Exception as e:
                print("Error al crear transacción WebPay:", e)
                return JsonResponse({"error": str(e)}, status=500)
        
        # Si el método de pago no es WebPay, se muestra el pago
        return render(request, 'pages/pago.html')

def transaccion_completa(request):
    token_ws = request.GET.get('token_ws')
    transaction = Transaction()
    try:
        result = transaction.commit(token_ws)
        if result['status'] == 'AUTHORIZED':
            data_usuario = request.session.get('data_usuario')
            print(f"Data_usuario: {data_usuario}")
            carrito_data = request.session.get('carrito_data')
            print(f"carrito_data: {carrito_data}")

            if not carrito_data or 'items' not in carrito_data:
                raise Exception("No se encontraron productos en el carrito")

            if request.user.is_authenticated:
                correoU = request.user.email
            
            print(f"Correo del usuario autenticado: {correoU}")
            
            # Cliente
            comprador = Usuario.objects.get(correo__email=correoU)

            # Estado del pedido
            objEstado = EstadoPedido.objects.get(idEstado = "env")
            print(f"Comprador obtenido: {comprador}")  
            print(f"Estado del pedido: {objEstado}")
            
            # Pedido
            objPedido = Pedido.objects.create(
                usuario = comprador,
                fecha = date.today(),
                direccion=data_usuario['direccion'],  
                telefono=data_usuario['telefono'],    
                correo=data_usuario['correo'],        
                total=data_usuario['total'],
                estado = objEstado,
            )
            objPedido.save()

            # Detalle
            for item in carrito_data['items']:
                objProducto = Producto.objects.get(idProducto = item["id"])

                objDetalle = DetallePedido.objects.create(
                    pedido = objPedido,
                    producto = objProducto,
                    cantidad = item["cantidad"],
                    total = item["precioTotal"]
                )
                objDetalle.save()

            # Pago
            objPago = Pagos.objects.create(
                pedido = objPedido,
                usuario = comprador
            )
            objPago.save()

            context = {
                "pedido": objPedido,
                "detalle": DetallePedido.objects.filter(pedido = objPedido.idPedido)
            }

            return render(request, 'pages/exito.html', context)
        else:
            reason = result.get('status', 'Unknown reason')
            return render(request, 'pages/error.html', {'reason': reason, 'result': result})
    except Exception as e:
        return render(request, 'pages/error.html', {'reason': str(e)})