from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Socio


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_socios(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    socios = Socio.objects.select_related('user')
    if q:
        socios = socios.filter(
            Q(nombre__icontains=q)
            | Q(apellido__icontains=q)
            | Q(email__icontains=q)
            | Q(user__username__icontains=q)
        )
    if estado:
        socios = socios.filter(estado=estado)

    paginator = Paginator(socios.order_by('-fecha_ingreso'), 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'socios/socios.html', {
        'page_obj': page_obj,
        'q': q,
        'estado': estado,
        'is_admin': request.user.is_staff,
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def crear_socio(request):
    if request.method != 'POST':
        return redirect('socios:listar_socios')

    username = request.POST.get('username', '').strip()
    nombre = request.POST.get('nombre', '').strip()
    apellido = request.POST.get('apellido', '').strip()
    email = request.POST.get('email', '').strip()
    telefono = request.POST.get('telefono', '').strip()
    ciudad = request.POST.get('ciudad', '').strip()
    direccion = request.POST.get('direccion', '').strip()
    password = request.POST.get('password', '')

    if not username or not nombre or not apellido or not email or not password:
        messages.error(request, 'Completa los campos obligatorios.')
        return redirect('socios:listar_socios')

    if User.objects.filter(username=username).exists():
        messages.error(request, 'El nombre de usuario ya existe.')
        return redirect('socios:listar_socios')

    user = User.objects.create_user(username=username, email=email, password=password)
    user.first_name = nombre
    user.last_name = apellido
    user.save()
    Socio.objects.create(
        user=user,
        nombre=nombre,
        apellido=apellido,
        email=email,
        telefono=telefono,
        ciudad=ciudad,
        direccion=direccion,
    )
    messages.success(request, 'Socio registrado correctamente.')
    return redirect('socios:listar_socios')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def editar_socio(request, socio_id):
    if request.method != 'POST':
        return redirect('socios:listar_socios')

    socio = get_object_or_404(Socio, id=socio_id)
    socio.nombre = request.POST.get('nombre', '').strip()
    socio.apellido = request.POST.get('apellido', '').strip()
    socio.email = request.POST.get('email', '').strip()
    socio.telefono = request.POST.get('telefono', '').strip()
    socio.ciudad = request.POST.get('ciudad', '').strip()
    socio.direccion = request.POST.get('direccion', '').strip()
    socio.observacion = request.POST.get('observacion', '').strip()
    socio.save()
    messages.success(request, 'Datos del socio actualizados.')
    return redirect('socios:listar_socios')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def activar_socio(request, socio_id):
    socio = get_object_or_404(Socio, id=socio_id)
    socio.estado = 'activo'
    socio.save()
    messages.success(request, 'Socio activado.')
    return redirect('socios:listar_socios')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def desactivar_socio(request, socio_id):
    socio = get_object_or_404(Socio, id=socio_id)
    socio.estado = 'inactivo'
    socio.save()
    messages.success(request, 'Socio desactivado.')
    return redirect('socios:listar_socios')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def eliminar_socio(request, socio_id):
    socio = get_object_or_404(Socio, id=socio_id)
    socio.user.delete()
    socio.delete()
    messages.success(request, 'Socio eliminado definitivamente.')
    return redirect('socios:listar_socios')
