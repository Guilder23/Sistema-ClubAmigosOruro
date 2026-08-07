from django.contrib import admin
from .models import SolicitudSocio


@admin.register(SolicitudSocio)
class SolicitudSocioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'estado', 'fecha_solicitud')
    list_filter = ('estado',)
    search_fields = ('nombre', 'apellido', 'email')
