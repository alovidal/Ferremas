from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Elimina el perfil cuando se elimina el usuario
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    interests = models.CharField(max_length=100)
    terms_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

