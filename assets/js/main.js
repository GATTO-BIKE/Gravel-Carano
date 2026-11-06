// Interazioni essenziali: menu mobile e richiesta informazioni.
'use strict';

const menuButton = document.querySelector('[data-menu-button]');
const navigation = document.querySelector('[data-navigation]');

if (menuButton && navigation) {
    menuButton.addEventListener('click', () => {
        const isOpen = navigation.classList.toggle('is-open');
        menuButton.setAttribute('aria-expanded', String(isOpen));
    });
}

const registrationForm = document.querySelector('[data-registration-form]');

if (registrationForm) {
    registrationForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const status = document.querySelector('[data-form-status]');
        const submitButton = registrationForm.querySelector('button[type="submit"]');
        const data = new FormData(registrationForm);

        const payload = {
            name: String(data.get('name') || '').trim(),
            email: String(data.get('email') || '').trim(),
            phone: String(data.get('phone') || '').trim(),
            message: String(data.get('message') || '').trim(),
            privacy: data.get('privacy') === 'on',
            website: String(data.get('website') || '')
        };

        status.textContent = 'Invio della richiesta in corso…';
        submitButton.disabled = true;

        try {
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const result = await response.json();
            status.textContent = result.message || 'Risposta non disponibile.';

            if (response.ok) {
                registrationForm.reset();
            }
        } catch (error) {
            status.textContent = 'Il modulo richiede il server online. Puoi contattarci via email.';
        } finally {
            submitButton.disabled = false;
        }
    });
}
