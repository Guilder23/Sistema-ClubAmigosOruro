from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from apps.socios.models import Socio
from .models import SouvenirEntrega, Souvenir


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_entregas(request):
    entregas = SouvenirEntrega.objects.select_related('socio', 'entregado_por').order_by('-fecha_entrega')
    paginator = Paginator(entregas, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'souvenirs/entregas/entregas.html', {'page_obj': page_obj})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def registrar_entrega(request):
    if request.method == 'POST':
        socio_id = request.POST.get('socio_id')
        souvenir_id = request.POST.get('souvenir_id')
        observacion = request.POST.get('observacion', '').strip()
        socio = Socio.objects.filter(id=socio_id).first()
        if not socio:
            messages.error(request, 'Selecciona un socio válido.')
            return redirect('souvenirs:registrar_entrega')
        if SouvenirEntrega.objects.filter(socio=socio).exists():
            messages.warning(request, 'Este socio ya registró la entrega del souvenir.')
            return redirect('souvenirs:listar_entregas')
        souvenir = None
        if souvenir_id:
            souvenir = Souvenir.objects.filter(id=souvenir_id, activo=True).first()
        SouvenirEntrega.objects.create(socio=socio, souvenir=souvenir, entregado_por=request.user, observacion=observacion)
        if souvenir and souvenir.stock and souvenir.stock > 0:
            souvenir.stock = max(0, souvenir.stock - 1)
            souvenir.save()
        socio.recibio_souvenir = True
        socio.save()
        messages.success(request, 'Entrega de souvenir registrada.')
        return redirect('souvenirs:listar_entregas')

    socios = Socio.objects.filter(estado='activo').order_by('apellido', 'nombre')
    souvenirs = Souvenir.objects.filter(activo=True).order_by('-creado')
    return render(request, 'souvenirs/entregas/registrar_entrega.html', {'socios': socios, 'souvenirs': souvenirs})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_souvenirs(request):
    q = request.GET.get('q', '').strip()
    activo = request.GET.get('activo', '').strip()
    objetos = Souvenir.objects.order_by('-creado')

    if q:
        objetos = objetos.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q)
        )

    if activo == 'si':
        objetos = objetos.filter(activo=True)
    elif activo == 'no':
        objetos = objetos.filter(activo=False)

    paginator = Paginator(objetos, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'souvenirs/souvenirs.html', {'page_obj': page_obj, 'q': q, 'activo': activo})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def crear_souvenir(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        stock = int(request.POST.get('stock') or 0)
        imagen = request.FILES.get('imagen')
        if not nombre:
            messages.error(request, 'Nombre requerido.')
            return redirect('souvenirs:listar_souvenirs')
        Souvenir.objects.create(nombre=nombre, descripcion=descripcion, stock=stock, imagen=imagen)
        messages.success(request, 'Souvenir creado.')
        return redirect('souvenirs:listar_souvenirs')
    return redirect('souvenirs:listar_souvenirs')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def editar_souvenir(request, pk):
    s = get_object_or_404(Souvenir, pk=pk)
    if request.method == 'POST':
        s.nombre = request.POST.get('nombre', s.nombre).strip()
        s.descripcion = request.POST.get('descripcion', s.descripcion).strip()
        s.stock = int(request.POST.get('stock') or s.stock)
        if request.FILES.get('imagen'):
            s.imagen = request.FILES.get('imagen')
        s.save()
        messages.success(request, 'Souvenir actualizado.')
        return redirect('souvenirs:listar_souvenirs')
    return redirect('souvenirs:listar_souvenirs')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def ver_souvenir(request, pk):
    return redirect('souvenirs:listar_souvenirs')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def eliminar_souvenir(request, pk):
    s = get_object_or_404(Souvenir, pk=pk)
    if request.method == 'POST':
        s.delete()
        messages.success(request, 'Souvenir eliminado.')
        return redirect('souvenirs:listar_souvenirs')
    return redirect('souvenirs:listar_souvenirs')
