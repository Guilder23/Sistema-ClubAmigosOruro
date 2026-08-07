document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('[data-ajax-form]');
    forms.forEach(function (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
        });
    });

    const solicitudesForm = document.getElementById('solicitudesFiltrosForm');
    const searchInput = document.getElementById('inputSolicitudBusqueda');
    const estadoSelect = document.getElementById('selectSolicitudEstado');
    let debounceTimer = null;

    const submitFiltros = function () {
        if (solicitudesForm) {
            solicitudesForm.submit();
        }
    };

    const scheduleSubmit = function () {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(submitFiltros, 300);
    };

    if (searchInput) {
        searchInput.addEventListener('input', scheduleSubmit);
    }

    if (estadoSelect) {
        estadoSelect.addEventListener('change', scheduleSubmit);
    }
});
