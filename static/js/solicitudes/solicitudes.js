document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('[data-ajax-form]');
    forms.forEach(function (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
        });
    });
});
