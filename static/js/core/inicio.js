/* ================================================
   PÁGINA INICIO - JavaScript Específico
   ================================================ */

document.addEventListener('DOMContentLoaded', function() {
    initializePaginationAnimations();
    initializeFaqAccordion();
    initializeRevealAnimations();
    initializeFechaNacimientoMode();
});

function initializePaginationAnimations() {
    document.querySelectorAll('.pagination a').forEach(link => {
        link.addEventListener('click', function() {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 180);
        });
    });
}

function initializeFaqAccordion() {
    document.querySelectorAll('.faq-item').forEach(item => {
        const button = item.querySelector('.faq-question');
        if (!button) return;

        button.addEventListener('click', () => {
            const wasActive = item.classList.contains('active');

            document.querySelectorAll('.faq-item').forEach(faqItem => {
                faqItem.classList.remove('active');
                const faqButton = faqItem.querySelector('.faq-question');
                if (faqButton) {
                    faqButton.setAttribute('aria-expanded', 'false');
                }
            });

            if (!wasActive) {
                item.classList.add('active');
                button.setAttribute('aria-expanded', 'true');
            }
        });
    });
}

function initializeRevealAnimations() {
    const elements = document.querySelectorAll('.reveal');
    if (!('IntersectionObserver' in window) || elements.length === 0) {
        elements.forEach(el => el.classList.add('visible'));
        return;
    }

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                obs.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.12
    });

    elements.forEach(el => observer.observe(el));
}

function initializeFechaNacimientoMode() {
    const dateInput = document.getElementById('fecha_nacimiento');
    const manualInput = document.getElementById('fecha_nacimiento_manual');
    const calendarBtn = document.getElementById('fechaNacimientoBtn');
    const errorFeedback = document.getElementById('fechaNacimientoError');

    if (!dateInput || !manualInput || !calendarBtn) return;

    const isMobileMode = () => window.innerWidth <= 768 || 'ontouchstart' in window;

    const formatDate = date => {
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        return `${day}/${month}/${year}`;
    };

    const parseDate = value => {
        const match = value.trim().match(/^([0-3]\d)\/([0-1]\d)\/(\d{4})$/);
        if (!match) return null;
        const day = Number(match[1]);
        const month = Number(match[2]);
        const year = Number(match[3]);
        const date = new Date(year, month - 1, day);
        return date.getFullYear() === year && date.getMonth() + 1 === month && date.getDate() === day ? date : null;
    };

    const showError = message => {
        if (errorFeedback) {
            errorFeedback.textContent = message;
            errorFeedback.style.display = 'block';
        }
        manualInput.classList.add('is-invalid');
    };

    const clearError = () => {
        if (errorFeedback) {
            errorFeedback.style.display = 'none';
        }
        manualInput.classList.remove('is-invalid');
    };

    const setMobileMode = active => {
        if (active) {
            dateInput.style.position = 'absolute';
            dateInput.style.left = '-9999px';
            dateInput.style.width = '1px';
            dateInput.style.height = '1px';
            dateInput.style.opacity = '0';
            dateInput.style.pointerEvents = 'none';
            manualInput.classList.remove('d-none');
            calendarBtn.classList.remove('d-none');
            if (dateInput.value) {
                const date = new Date(dateInput.value);
                if (!Number.isNaN(date.getTime())) {
                    manualInput.value = formatDate(date);
                }
            }
        } else {
            dateInput.style.position = '';
            dateInput.style.left = '';
            dateInput.style.width = '';
            dateInput.style.height = '';
            dateInput.style.opacity = '';
            dateInput.style.pointerEvents = '';
            manualInput.classList.add('d-none');
            calendarBtn.classList.add('d-none');
            if (manualInput.value) {
                const date = parseDate(manualInput.value);
                if (date) {
                    dateInput.value = date.toISOString().slice(0, 10);
                    clearError();
                }
            }
        }
    };

    const updateMode = () => setMobileMode(isMobileMode());
    updateMode();
    window.addEventListener('resize', updateMode);

    calendarBtn.addEventListener('click', () => {
        dateInput.focus();
        dateInput.click();
    });

    dateInput.addEventListener('input', () => {
        if (!dateInput.value) {
            manualInput.value = '';
            clearError();
            return;
        }
        const date = new Date(dateInput.value);
        if (!Number.isNaN(date.getTime())) {
            manualInput.value = formatDate(date);
            clearError();
        }
    });

    manualInput.addEventListener('blur', () => {
        if (!manualInput.value.trim()) {
            dateInput.value = '';
            clearError();
            return;
        }
        const date = parseDate(manualInput.value);
        if (date) {
            dateInput.value = date.toISOString().slice(0, 10);
            clearError();
        } else {
            dateInput.value = '';
            showError('Formato dd/mm/aaaa válido.');
        }
    });
}

// Scroll suave para anclas
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const targetSelector = this.getAttribute('href');
        if (!targetSelector || targetSelector === '#') return;

        const target = document.querySelector(targetSelector);
        if (!target) return;

        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
});

