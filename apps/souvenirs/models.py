from django.db import models
from django.contrib.auth.models import User


class SouvenirEntrega(models.Model):
    socio = models.ForeignKey('socios.Socio', on_delete=models.CASCADE, related_name='entregas_souvenir')
    fecha_entrega = models.DateField(auto_now_add=True, verbose_name='Fecha de entrega')
    entregado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='entregas_souvenir')
    observacion = models.TextField(blank=True, default='', verbose_name='Observación')

    class Meta:
        verbose_name = 'Entrega de souvenir'
        verbose_name_plural = 'Entregas de souvenirs'
        ordering = ['-fecha_entrega']

    def __str__(self):
        return f'{self.socio} - {self.fecha_entrega}'
