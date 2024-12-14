from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializer import *
from ferremas.models import *

# Create your views here.
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class MarcaProductosViewSet(viewsets.ModelViewSet):
    queryset = MarcaProductos.objects.all()
    serializer_class = MarcaProductosSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["idMarca"]

class CategoriaProductosViewSet(viewsets.ModelViewSet):
    queryset = CategoriaProductos.objects.all()
    serializer_class = CategoriaProductosSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["idCategoria"]
