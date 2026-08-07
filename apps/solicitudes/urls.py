from django.urls import path
from .views import listar_solicitudes, aprobar_solicitud, rechazar_solicitud, crear_solicitud

app_name = 'solicitudes'

urlpatterns = [
    path('', listar_solicitudes, name='listar_solicitudes'),
    path('nueva/', crear_solicitud, name='crear_solicitud'),
    path('<int:solicitud_id>/aprobar/', aprobar_solicitud, name='aprobar_solicitud'),
    path('<int:solicitud_id>/rechazar/', rechazar_solicitud, name='rechazar_solicitud'),
]
