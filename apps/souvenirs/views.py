from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from apps.socios.models import Socio
from .models import SouvenirEntrega


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_entregas(request):
    entregas = SouvenirEntrega.objects.select_related('socio', 'entregado_por').order_by('-fecha_entrega')
    paginator = Paginator(entregas, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'souvenirs/listar_entregas.html', {'page_obj': page_obj})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def registrar_entrega(request):
    if request.method == 'POST':
        socio_id = request.POST.get('socio_id')
        observacion = request.POST.get('observacion', '').strip()
        socio = Socio.objects.filter(id=socio_id).first()
        if not socio:
            messages.error(request, 'Selecciona un socio válido.')
            return redirect('souvenirs:registrar_entrega')
        if SouvenirEntrega.objects.filter(socio=socio).exists():
            messages.warning(request, 'Este socio ya registró la entrega del souvenir.')
            return redirect('souvenirs:listar_entregas')
        SouvenirEntrega.objects.create(socio=socio, entregado_por=request.user, observacion=observacion)
        socio.recibio_souvenir = True
        socio.save()
        messages.success(request, 'Entrega de souvenir registrada.')
        return redirect('souvenirs:listar_entregas')

    socios = Socio.objects.filter(estado='activo').order_by('apellido', 'nombre')
    return render(request, 'souvenirs/registrar_entrega.html', {'socios': socios})
