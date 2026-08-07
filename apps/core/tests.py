from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase


class CrearAdministradorCommandTests(TestCase):
    def test_crea_usuario_admin_si_no_existe(self):
        User = get_user_model()
        User.objects.filter(username='admin').delete()

        call_command(
            'crear_administrador',
            username='admin',
            email='admin@example.com',
            password='Admin1234!',
        )

        user = User.objects.get(username='admin')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
