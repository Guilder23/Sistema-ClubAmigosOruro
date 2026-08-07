from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from apps.socios.models import Socio
from apps.souvenirs.models import SouvenirEntrega
from apps.solicitudes.models import SolicitudSocio


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def dashboard(request):
    total_socios = Socio.objects.count()
    activos = Socio.objects.filter(estado='activo').count()
    inactivos = Socio.objects.filter(estado='inactivo').count()
    solicitudes_pendientes = SolicitudSocio.objects.filter(estado='pendiente').count()
    souvenirs_entregados = SouvenirEntrega.objects.count()
    souvenirs_pendientes = total_socios - souvenirs_entregados

    return render(request, 'dashboard/dashboard.html', {
        'total_socios': total_socios,
        'socios_activos': activos,
        'socios_inactivos': inactivos,
        'solicitudes_pendientes': solicitudes_pendientes,
        'souvenirs_entregados': souvenirs_entregados,
        'souvenirs_pendientes': souvenirs_pendientes,
    })
