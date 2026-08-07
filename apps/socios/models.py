from django.db import models
from django.contrib.auth.models import User


class Socio(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='socio_profile')
    nombre = models.CharField(max_length=150, verbose_name='Nombres')
    apellido = models.CharField(max_length=150, verbose_name='Apellidos')
    email = models.EmailField(verbose_name='Correo electrónico')
    telefono = models.CharField(max_length=20, blank=True, default='', verbose_name='Teléfono')
    ciudad = models.CharField(max_length=150, blank=True, default='', verbose_name='Ciudad')
    direccion = models.CharField(max_length=250, blank=True, default='', verbose_name='Dirección')
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name='Fecha de ingreso')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    recibio_souvenir = models.BooleanField(default=False, verbose_name='Recibió souvenir')
    observacion = models.TextField(blank=True, default='', verbose_name='Observación')

    class Meta:
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'
        ordering = ['-fecha_ingreso', 'apellido', 'nombre']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
