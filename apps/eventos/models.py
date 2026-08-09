from django.db import models


class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, default='')
    fecha_evento = models.DateField(verbose_name='Fecha del evento')
    lugar = models.CharField(max_length=250, blank=True, default='')
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-fecha_evento', 'nombre']

    def __str__(self):
        return self.nombre
