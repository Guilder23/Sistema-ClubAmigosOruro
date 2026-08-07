from django.urls import path
from .views import listar_socios, crear_socio, editar_socio, activar_socio, desactivar_socio, eliminar_socio

app_name = 'socios'

urlpatterns = [
    path('', listar_socios, name='listar_socios'),
    path('nuevo/', crear_socio, name='crear_socio'),
    path('<int:socio_id>/editar/', editar_socio, name='editar_socio'),
    path('<int:socio_id>/activar/', activar_socio, name='activar_socio'),
    path('<int:socio_id>/desactivar/', desactivar_socio, name='desactivar_socio'),
    path('<int:socio_id>/eliminar/', eliminar_socio, name='eliminar_socio'),
]
