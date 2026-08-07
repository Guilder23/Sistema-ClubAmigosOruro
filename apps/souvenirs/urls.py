from django.urls import path
from .views import listar_entregas, registrar_entrega

app_name = 'souvenirs'

urlpatterns = [
    path('', listar_entregas, name='listar_entregas'),
    path('registrar/', registrar_entrega, name='registrar_entrega'),
]
