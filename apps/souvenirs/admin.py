from django.contrib import admin
from .models import SouvenirEntrega


@admin.register(SouvenirEntrega)
class SouvenirEntregaAdmin(admin.ModelAdmin):
    list_display = ('socio', 'fecha_entrega', 'entregado_por')
    search_fields = ('socio__nombre', 'socio__apellido')
