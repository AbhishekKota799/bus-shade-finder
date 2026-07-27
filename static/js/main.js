const tripForm = document.querySelector('#trip-form');

if (tripForm) {
    tripForm.addEventListener('submit', () => {
        const submitButton = tripForm.querySelector('button[type="submit"]');

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = 'Finding Route...';
        }
    });
}
