/* ================================================
   PÁGINA INICIO - JavaScript Específico
   ================================================ */

document.addEventListener('DOMContentLoaded', function() {
    initializePaginationAnimations();
    initializeFaqAccordion();
    initializeRevealAnimations();
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

