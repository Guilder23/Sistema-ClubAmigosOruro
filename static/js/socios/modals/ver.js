document.addEventListener('DOMContentLoaded', function () {
    const modalVer = document.getElementById('modalVerSocio');
    if (!modalVer) return;

    modalVer.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        document.getElementById('verNombre').textContent = button.getAttribute('data-nombre');
        document.getElementById('verApellido').textContent = button.getAttribute('data-apellido');
        document.getElementById('verEmail').textContent = button.getAttribute('data-email');
        document.getElementById('verTelefono').textContent = button.getAttribute('data-telefono');
        document.getElementById('verCiudad').textContent = button.getAttribute('data-ciudad');
        document.getElementById('verDireccion').textContent = button.getAttribute('data-direccion');
        document.getElementById('verEstado').textContent = button.getAttribute('data-estado');
        document.getElementById('verSouvenir').textContent = button.getAttribute('data-souvenir');
        document.getElementById('verFechaIngreso').textContent = button.getAttribute('data-fecha-ingreso');
    });
});
