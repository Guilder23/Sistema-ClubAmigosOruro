document.addEventListener('DOMContentLoaded', function () {
    const modalEditar = document.getElementById('modalEditarSocio');
    if (!modalEditar) return;

    modalEditar.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const id = button.getAttribute('data-id');
        document.getElementById('editarNombre').value = button.getAttribute('data-nombre');
        document.getElementById('editarApellido').value = button.getAttribute('data-apellido');
        document.getElementById('editarEmail').value = button.getAttribute('data-email');
        document.getElementById('editarTelefono').value = button.getAttribute('data-telefono');
        document.getElementById('editarCiudad').value = button.getAttribute('data-ciudad');
        document.getElementById('editarDireccion').value = button.getAttribute('data-direccion');
        document.getElementById('editarObservacion').value = button.getAttribute('data-observacion');
        document.getElementById('formEditarSocio').action = `/socios/${id}/editar/`;
    });
});
