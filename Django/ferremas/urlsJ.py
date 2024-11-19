from django.urls import path
from ferremas import viewsJ

urlpatterns = [
    path('ver_ordenes/', viewsJ.verordenes, name='ver_ordenes'),
]