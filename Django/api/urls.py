from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()

router.register(r'productos', views.ProductoViewSet)
router.register(r'marcas', views.MarcaProductosViewSet)
router.register(r'categorias', views.CategoriaProductosViewSet)

urlpatterns = [
    path("", include(router.urls))
]
