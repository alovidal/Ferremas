from django.shortcuts import render
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