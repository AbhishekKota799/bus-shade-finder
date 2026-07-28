const tripForm = document.querySelector('#trip-form');
const loadingOverlay = document.querySelector('#loading-overlay');
const loadingStatus = document.querySelector('#loading-status');
const loadingMessages = [
    'Finding route...',
    'Calculating sun position...',
    'Analyzing shade...',
];

if (tripForm) {
    tripForm.addEventListener('submit', () => {
        if (!tripForm.checkValidity()) {
            return;
        }

        const submitButton = tripForm.querySelector('button[type="submit"]');

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = 'Analyzing...';
        }

        if (loadingOverlay && loadingStatus) {
            let messageIndex = 0;
            loadingOverlay.classList.add('is-visible');
            loadingOverlay.setAttribute('aria-hidden', 'false');
            loadingStatus.textContent = loadingMessages[messageIndex];

            window.setInterval(() => {
                messageIndex = (messageIndex + 1) % loadingMessages.length;
                loadingStatus.textContent = loadingMessages[messageIndex];
            }, 1400);
        }
    });
}
