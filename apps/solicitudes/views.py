from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from urllib.parse import quote

from .models import SolicitudSocio
from apps.socios.models import Socio
from apps.socios.models import generar_codigo_socio


def construir_enlace_whatsapp(solicitud):
    telefono = ''.join(caracter for caracter in (solicitud.telefono or '') if caracter.isdigit())
    if not telefono:
        return ''
    if len(telefono) == 8:
        telefono = f'591{telefono}'

    apellido = solicitud.apellido_paterno or solicitud.apellido
    nombre_completo = f'{solicitud.nombre} {apellido}'.strip()
    if solicitud.estado == 'rechazada':
        mensaje = (
            f'Hola {nombre_completo}. Gracias por tu interés en formar parte del Club carnaval Oruro.\n\n'
            'Lamentamos informarte que tu solicitud de ingreso fue rechazada en esta ocasión. '
            'Si deseas recibir más información, puedes responder a este mensaje.\n\n'
            'Saludos cordiales.'
        )
    elif solicitud.usuario_creado:
        contrasena = solicitud.carnet_ci or 'ClubAmigos2026!'
        mensaje = (
            f'Hola {nombre_completo}, gracias por registrarte para entrar a tu cuenta de Club carnaval Oruro.\n\n'
            f'Estos son los datos de acceso:\n'
            f'Usuario: {solicitud.usuario_creado.username}\n'
            f'Contraseña: {contrasena}\n\n'
            '¡Te damos la bienvenida al club!'
        )
    else:
        mensaje = (
            f'Hola {nombre_completo}, tu solicitud para formar parte del Club carnaval Oruro fue aprobada. '
            'Nos comunicaremos contigo para brindarte los siguientes pasos.\n\n'
            '¡Bienvenido al club!'
        )
    return f'https://wa.me/{telefono}?text={quote(mensaje)}'


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_solicitudes(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    solicitudes = SolicitudSocio.objects.all()
    if q:
        solicitudes = solicitudes.filter(
            Q(nombre__icontains=q) | Q(apellido__icontains=q) | Q(apellido_paterno__icontains=q) | Q(apellido_materno__icontains=q) | Q(email__icontains=q)
        )
    if estado:
        solicitudes = solicitudes.filter(estado=estado)

    paginator = Paginator(solicitudes.order_by('-fecha_solicitud'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    for solicitud in page_obj.object_list:
        solicitud.whatsapp_url = construir_enlace_whatsapp(solicitud) if solicitud.estado in ('aprobada', 'rechazada') else ''
    return render(request, 'solicitudes/listar_solicitudes.html', {'page_obj': page_obj, 'q': q, 'estado': estado})


def crear_solicitud(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido_paterno = request.POST.get('apellido_paterno', '').strip()
        apellido_materno = request.POST.get('apellido_materno', '').strip()
        apellido = request.POST.get('apellido', '').strip() or f"{apellido_paterno} {apellido_materno}".strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        ciudad = request.POST.get('ciudad', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        fecha_nacimiento = request.POST.get('fecha_nacimiento', '').strip() or None
        razon = request.POST.get('razon', '').strip()
        carnet_ci = request.POST.get('carnet_ci', '').strip()
        carnet_complemento = request.POST.get('carnet_complemento', '').strip()

        if not nombre or not (apellido_paterno or apellido) or not email:
            messages.error(request, 'Completa los datos básicos de la solicitud.')
            return redirect('core:inicio')

        SolicitudSocio.objects.create(
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            apellido=apellido,
            email=email,
            telefono=telefono,
            ciudad=ciudad,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,
            razon=razon,
            carnet_ci=carnet_ci,
            carnet_complemento=carnet_complemento,
        )
        messages.success(request, 'CONFETTI_SHOW:Tu solicitud fue registrada correctamente. Pronto nos contactaremos.')
        return redirect('core:inicio')

    return redirect('core:inicio')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudSocio, id=solicitud_id)
    if solicitud.estado != 'pendiente':
        messages.info(request, 'Esta solicitud ya fue atendida.')
        return redirect('solicitudes:listar_solicitudes')

    # Usar apellido paterno como usuario (sin espacios), acortar a 20
    username = (solicitud.apellido_paterno or solicitud.apellido).lower().replace(' ', '')[:20]
    user, created = User.objects.get_or_create(username=username, defaults={
        'first_name': solicitud.nombre,
        'last_name': (solicitud.apellido_paterno or solicitud.apellido),
        'email': solicitud.email,
        'is_active': True,
    })
    if created:
        # La contraseña inicial será el número de carnet (sin complemento) si está disponible
        default_pass = solicitud.carnet_ci or 'ClubAmigos2026!'
        user.set_password(default_pass)
        user.save()
    # Crear registro de Socio si no existe
    if not Socio.objects.filter(user=user).exists():
        Socio.objects.create(
            user=user,
            codigo_socio=generar_codigo_socio(),
            nombre=solicitud.nombre,
            apellido_paterno=solicitud.apellido_paterno or '',
            apellido_materno=solicitud.apellido_materno or '',
            apellido=solicitud.apellido or '',
            email=solicitud.email,
            telefono=solicitud.telefono or '',
            ciudad=solicitud.ciudad or '',
            direccion=solicitud.direccion or '',
            carnet_ci=solicitud.carnet_ci or '',
            carnet_complemento=solicitud.carnet_complemento or '',
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
