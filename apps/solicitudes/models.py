from django.db import models
from django.contrib.auth.models import User


class SolicitudSocio(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    nombre = models.CharField(max_length=150, verbose_name='Nombres')
    apellido_paterno = models.CharField(max_length=150, blank=True, default='', verbose_name='Apellido paterno')
    apellido_materno = models.CharField(max_length=150, blank=True, default='', verbose_name='Apellido materno')
    # Campo legado
    apellido = models.CharField(max_length=150, blank=True, default='', verbose_name='Apellidos')
    email = models.EmailField(verbose_name='Correo electrónico')
    telefono = models.CharField(max_length=20, blank=True, default='', verbose_name='Teléfono')
    ciudad = models.CharField(max_length=150, blank=True, default='', verbose_name='Ciudad')
    direccion = models.CharField(max_length=250, blank=True, default='', verbose_name='Dirección')
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    carnet_ci = models.CharField(max_length=30, blank=True, default='', verbose_name='CI / Carnet')
    carnet_complemento = models.CharField(max_length=10, blank=True, default='', verbose_name='Complemento CI')
    razon = models.TextField(blank=True, default='', verbose_name='Razón de unirse al club')
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de solicitud')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observacion = models.TextField(blank=True, default='', verbose_name='Observación')
    usuario_creado = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='solicitudes_creadas')

    class Meta:
        verbose_name = 'Solicitud de socio'
        verbose_name_plural = 'Solicitudes de socios'
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
