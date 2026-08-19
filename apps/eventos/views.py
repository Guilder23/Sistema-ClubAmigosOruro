from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from .models import Evento


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_eventos(request):
    q = request.GET.get('q', '').strip()
    activo = request.GET.get('activo', '').strip()
    eventos = Evento.objects.order_by('-fecha_evento')

    if q:
        eventos = eventos.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(lugar__icontains=q)
        )

    if activo == 'si':
        eventos = eventos.filter(activo=True)
    elif activo == 'no':
        eventos = eventos.filter(activo=False)

    paginator = Paginator(eventos, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'eventos/eventos.html', {'page_obj': page_obj, 'q': q, 'activo': activo})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def crear_evento(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        fecha_evento = request.POST.get('fecha_evento')
        lugar = request.POST.get('lugar', '').strip()
        activo = request.POST.get('activo') == 'on'

        if not nombre or not fecha_evento:
            messages.error(request, 'Nombre y fecha de evento son obligatorios.')
            return redirect('eventos:listar_eventos')

        Evento.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            fecha_evento=fecha_evento,
            lugar=lugar,
            activo=activo,
        )
        messages.success(request, 'Evento creado correctamente.')
        return redirect('eventos:listar_eventos')

    return redirect('eventos:listar_eventos')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        evento.nombre = request.POST.get('nombre', evento.nombre).strip()
        evento.descripcion = request.POST.get('descripcion', evento.descripcion).strip()
        fecha_evento = request.POST.get('fecha_evento')
        evento.lugar = request.POST.get('lugar', evento.lugar).strip()
        evento.activo = request.POST.get('activo') == 'on'

        if fecha_evento:
            evento.fecha_evento = fecha_evento
        evento.save()
        messages.success(request, 'Evento actualizado correctamente.')
        return redirect('eventos:listar_eventos')

    return redirect('eventos:listar_eventos')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        if evento.souvenirs.exists():
            messages.error(request, 'No se puede eliminar un evento que tiene souvenirs asignados. Puedes cambiar su estado a inactivo.')
            return redirect('eventos:listar_eventos')
        evento.delete()
        messages.success(request, 'Evento eliminado correctamente.')
    return redirect('eventos:listar_eventos')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def cambiar_estado_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        evento.activo = not evento.activo
        evento.save(update_fields=['activo'])
        estado = 'activado' if evento.activo else 'desactivado'
        messages.success(request, f'Evento {estado}.')
    return redirect('eventos:listar_eventos')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def ver_evento(request, pk):
    return redirect('eventos:listar_eventos')
