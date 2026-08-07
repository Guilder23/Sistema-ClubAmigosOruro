from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db.models import Q

from .models import SolicitudSocio
from apps.socios.models import Socio


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_solicitudes(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    solicitudes = SolicitudSocio.objects.all()
    if q:
        solicitudes = solicitudes.filter(
            Q(nombre__icontains=q) | Q(apellido__icontains=q) | Q(email__icontains=q)
        )
    if estado:
        solicitudes = solicitudes.filter(estado=estado)

    paginator = Paginator(solicitudes.order_by('-fecha_solicitud'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'solicitudes/listar_solicitudes.html', {'page_obj': page_obj, 'q': q, 'estado': estado})


def crear_solicitud(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        ciudad = request.POST.get('ciudad', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        fecha_nacimiento = request.POST.get('fecha_nacimiento', '').strip() or None
        razon = request.POST.get('razon', '').strip()

        if not nombre or not apellido or not email:
            messages.error(request, 'Completa los datos básicos de la solicitud.')
            return redirect('core:inicio')

        SolicitudSocio.objects.create(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            ciudad=ciudad,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,
            razon=razon,
        )
        messages.success(request, 'Tu solicitud fue registrada correctamente. Pronto nos contactaremos.')
        return redirect('core:inicio')

    return redirect('core:inicio')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudSocio, id=solicitud_id)
    if solicitud.estado != 'pendiente':
        messages.info(request, 'Esta solicitud ya fue atendida.')
        return redirect('solicitudes:listar_solicitudes')

    username = f"{solicitud.nombre.lower().replace(' ', '')}{solicitud.apellido.lower().replace(' ', '')}"[:20]
    user, created = User.objects.get_or_create(username=username, defaults={
        'first_name': solicitud.nombre,
        'last_name': solicitud.apellido,
        'email': solicitud.email,
        'is_active': True,
    })
    if created:
        user.set_password('ClubAmigos2026!')
        user.save()
    # Crear registro de Socio si no existe
    if not Socio.objects.filter(user=user).exists():
        Socio.objects.create(
            user=user,
            nombre=solicitud.nombre,
            apellido=solicitud.apellido,
            email=solicitud.email,
            telefono=solicitud.telefono or '',
            ciudad=solicitud.ciudad or '',
            direccion=solicitud.direccion or '',
        )
    solicitud.estado = 'aprobada'
    solicitud.usuario_creado = user
    solicitud.observacion = 'Solicitud aprobada y cuenta creada automáticamente.'
    solicitud.save()
    messages.success(request, 'Solicitud aprobada y cuenta creada para el socio.')
    return redirect('solicitudes:listar_solicitudes')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudSocio, id=solicitud_id)
    if solicitud.estado != 'pendiente':
        messages.info(request, 'Esta solicitud ya fue atendida.')
        return redirect('solicitudes:listar_solicitudes')

    solicitud.estado = 'rechazada'
    solicitud.observacion = request.POST.get('observacion', 'Solicitud rechazada.')
    solicitud.save()
    messages.success(request, 'Solicitud rechazada.')
    return redirect('solicitudes:listar_solicitudes')
