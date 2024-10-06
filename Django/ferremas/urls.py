from django.urls import path
from ferremas import views

urlpatterns = [
    path("", views.index, name="index"),
]
