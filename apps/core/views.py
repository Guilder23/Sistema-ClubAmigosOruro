from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render


def get_home_redirect(user):
    if user.is_staff:
        return 'solicitudes:listar_solicitudes'
    return 'socios:perfil_socio'


def inicio(request):
    if request.user.is_authenticated:
        return redirect(get_home_redirect(request.user))
    return render(request, 'core/inicio.html')


def faq(request):
    return render(request, 'core/faq.html')


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect(get_home_redirect(request.user))

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Usuario o contrasena incorrectos.')
            return render(request, 'auth/login.html')

        try:
            from apps.socios.models import Socio
            socio = Socio.objects.get(user=user)
            if socio.estado == 'inactivo':
                messages.error(request, 'Socio inactivo. Comunicate con el administrador para que te active y puedas iniciar sesion.')
                return render(request, 'auth/login.html')
        except Socio.DoesNotExist:
            pass

        login(request, user)
        next_url = request.GET.get('next') or request.POST.get('next')
        if next_url:
            return redirect(next_url)
        return redirect(get_home_redirect(user))

    return render(request, 'auth/login.html')


@login_required
def cerrar_sesion(request):
	logout(request)
	return redirect('core:inicio')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def registrar_usuario(request):
	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		first_name = request.POST.get('first_name', '').strip()
		last_name = request.POST.get('last_name', '').strip()
		email = request.POST.get('email', '').strip()
		password = request.POST.get('password', '')
		password2 = request.POST.get('password2', '')
		is_admin = request.POST.get('is_admin') == 'on'

		if not username or not password:
			messages.error(request, 'Usuario y contrasena son obligatorios.')
			return redirect('core:registro')

		if password != password2:
			messages.error(request, 'Las contrasenas no coinciden.')
			return redirect('core:registro')

		if User.objects.filter(username=username).exists():
			messages.error(request, 'El nombre de usuario ya existe.')
			return redirect('core:registro')

		user = User.objects.create_user(
			username=username,
			first_name=first_name,
			last_name=last_name,
			email=email,
			password=password,
		)
		user.is_staff = is_admin
		user.save()

		messages.success(request, 'Usuario creado correctamente.')
		return redirect('core:registro')

	q = request.GET.get('q', '').strip()
	rol = request.GET.get('rol', '').strip()
	estado = request.GET.get('estado', '').strip()

	usuarios_qs = User.objects.order_by('-date_joined')
	if q:
		usuarios_qs = usuarios_qs.filter(
			Q(username__icontains=q)
			| Q(first_name__icontains=q)
			| Q(last_name__icontains=q)
			| Q(email__icontains=q)
		)

	if rol == 'admin':
		usuarios_qs = usuarios_qs.filter(is_staff=True)
	elif rol == 'usuario':
		usuarios_qs = usuarios_qs.filter(is_staff=False)

	if estado == 'activo':
		usuarios_qs = usuarios_qs.filter(is_active=True)
	elif estado == 'bloqueado':
		usuarios_qs = usuarios_qs.filter(is_active=False)

	paginator = Paginator(usuarios_qs, 10)
	page_number = request.GET.get('page')
	usuarios = paginator.get_page(page_number)

	return render(
		request,
		'auth/registro.html',
		{
			'usuarios': usuarios,
			'q': q,
			'rol': rol,
			'estado': estado,
		},
	)


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def editar_usuario(request, user_id):
	objetivo = get_object_or_404(User, id=user_id)

	if request.method == 'POST':
		if objetivo.is_superuser and not request.user.is_superuser:
			messages.error(request, 'No tienes permiso para editar este usuario.')
			return redirect('core:registro')

		username = request.POST.get('username', '').strip()
		email = request.POST.get('email', '').strip()
		first_name = request.POST.get('first_name', '').strip()
		last_name = request.POST.get('last_name', '').strip()
		is_admin = request.POST.get('is_admin') == 'on'

		if not username:
			messages.error(request, 'El usuario es obligatorio.')
			return redirect('core:registro')

		if User.objects.exclude(id=objetivo.id).filter(username=username).exists():
			messages.error(request, 'Ese nombre de usuario ya existe.')
			return redirect('core:registro')

		objetivo.username = username
		objetivo.email = email
		objetivo.first_name = first_name
		objetivo.last_name = last_name
		objetivo.is_staff = is_admin

		password = request.POST.get('password', '')
		password2 = request.POST.get('password2', '')
		if password or password2:
			if password != password2:
				messages.error(request, 'Las contrasenas no coinciden.')
				return redirect('core:registro')
			objetivo.set_password(password)

		objetivo.save()
		messages.success(request, 'Usuario actualizado correctamente.')

	return redirect('core:registro')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def toggle_bloqueo_usuario(request, user_id):
	objetivo = get_object_or_404(User, id=user_id)

	if request.method == 'POST':
		if objetivo == request.user:
			messages.error(request, 'No puedes bloquear tu propio usuario.')
			return redirect('core:registro')

		if objetivo.is_superuser and not request.user.is_superuser:
			messages.error(request, 'No tienes permiso para bloquear este usuario.')
			return redirect('core:registro')

		objetivo.is_active = not objetivo.is_active
		objetivo.save(update_fields=['is_active'])
		messages.success(
			request,
			f"Usuario {'bloqueado' if not objetivo.is_active else 'desbloqueado'} correctamente.",
		)

	return redirect('core:registro')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def eliminar_usuario(request, user_id):
	objetivo = get_object_or_404(User, id=user_id)

	if request.method == 'POST':
		if objetivo == request.user:
			messages.error(request, 'No puedes eliminar tu propio usuario.')
			return redirect('core:registro')

		if objetivo.is_superuser and not request.user.is_superuser:
			messages.error(request, 'No tienes permiso para eliminar este usuario.')
			return redirect('core:registro')

		objetivo.delete()
		messages.success(request, 'Usuario eliminado correctamente.')

	return redirect('core:registro')
