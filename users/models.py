from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Saldo")
    fecha_nacimiento = models.DateField(null=False, blank=False, verbose_name="Fecha de Nacimiento")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Foto de Perfil")

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username