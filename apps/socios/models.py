from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction


class Socio(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='socio_profile')
    codigo_socio = models.CharField(max_length=6, unique=True, blank=True, null=True, verbose_name='Código de socio')
    nombre = models.CharField(max_length=150, verbose_name='Nombres')
    apellido_paterno = models.CharField(max_length=150, blank=True, default='', verbose_name='Apellido paterno')
    apellido_materno = models.CharField(max_length=150, blank=True, default='', verbose_name='Apellido materno')
    # Mantener campo legado para compatibilidad
    apellido = models.CharField(max_length=150, blank=True, default='', verbose_name='Apellidos')
    email = models.EmailField(verbose_name='Correo electrónico')
    carnet_ci = models.CharField(max_length=30, blank=True, default='', verbose_name='CI / Carnet')
    carnet_complemento = models.CharField(max_length=20, blank=True, default='', verbose_name='Complemento CI')
    telefono = models.CharField(max_length=20, blank=True, default='', verbose_name='Teléfono')
    ciudad = models.CharField(max_length=150, blank=True, default='', verbose_name='Ciudad')
    direccion = models.CharField(max_length=250, blank=True, default='', verbose_name='Dirección')
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    razon = models.TextField(blank=True, default='', verbose_name='Razón de ingreso')
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name='Fecha de ingreso')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    recibio_souvenir = models.BooleanField(default=False, verbose_name='Recibió souvenir')
    observacion = models.TextField(blank=True, default='', verbose_name='Observación')

    class Meta:
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'
        ordering = ['-fecha_ingreso', 'apellido', 'nombre']

    def __str__(self):
        if self.apellido_paterno or self.apellido_materno:
            return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}".strip()
        return f'{self.nombre} {self.apellido}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    foto = models.ImageField(upload_to='profiles/', null=True, blank=True)

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuario'

    def __str__(self):
        return f'Perfil {self.user.username}'


@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


def generar_codigo_socio():
    """
    Genera el siguiente código de socio incremental.
    El formato es 260001, 260002, 260003, etc.
    """
    with transaction.atomic():
        # Obtener el último código asignado
        ultimo_socio = Socio.objects.filter(codigo_socio__isnull=False).order_by('-codigo_socio').first()
        
        if ultimo_socio and ultimo_socio.codigo_socio:
            # Extraer el número del código y sumar 1
            ultimo_numero = int(ultimo_socio.codigo_socio)
            nuevo_numero = ultimo_numero + 1
        else:
            # Si no hay códigos, empezar desde 260001
            nuevo_numero = 260001
        
        return str(nuevo_numero)
