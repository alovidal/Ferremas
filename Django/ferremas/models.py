from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con el modelo User
    full_name = models.CharField(max_length=100)  # Nombre completo
    phone = models.CharField(max_length=20)  # Teléfono del usuario
    interests = models.CharField(max_length=100)  # Intereses del usuario
    terms_accepted = models.BooleanField(default=False)  # Aceptación de términos
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        return f"Profile of {self.user.username}"

