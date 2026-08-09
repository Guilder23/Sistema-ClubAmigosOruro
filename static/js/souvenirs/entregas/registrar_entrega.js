document.addEventListener('DOMContentLoaded', function () {
    const eventoSelect = document.getElementById('selectEvento');
    const souvenirSelect = document.getElementById('selectSouvenir');
    const souvenirOptions = souvenirSelect ? Array.from(souvenirSelect.querySelectorAll('option')).map(option => ({
        value: option.value,
        text: option.textContent,
        eventoId: option.dataset.evento || '',
        disabled: option.value === '',
    })) : [];

    const renderSouvenirs = function () {
        if (!souvenirSelect) return;
        const selectedEvento = eventoSelect ? eventoSelect.value : '';
        souvenirSelect.innerHTML = '';

        const placeholder = document.createElement('option');
        placeholder.value = '';
        placeholder.textContent = selectedEvento ? '(Seleccionar si aplica)' : 'Selecciona un evento primero';
        souvenirSelect.appendChild(placeholder);

        if (!selectedEvento) {
            souvenirSelect.disabled = true;
            return;
        }

        const filtered = souvenirOptions.filter(option => option.eventoId === selectedEvento || option.value === '');
        filtered.forEach(optionData => {
            const option = document.createElement('option');
            option.value = optionData.value;
            option.textContent = optionData.text;
            option.dataset.evento = optionData.eventoId;
            souvenirSelect.appendChild(option);
        });

        souvenirSelect.disabled = false;
    };

    if (eventoSelect) {
        eventoSelect.addEventListener('change', renderSouvenirs);
        renderSouvenirs();
    }
});
