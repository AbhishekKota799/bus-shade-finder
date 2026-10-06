const tripForm = document.querySelector('#trip-form');
const loadingOverlay = document.querySelector('#loading-overlay');
const loadingStatus = document.querySelector('#loading-status');
const loadingMessages = [
    'Finding route...',
    'Calculating sun position...',
    'Analyzing shade...',
];

let loadingTimer = null;

function startLoadingMessages() {
    if (!loadingOverlay || !loadingStatus) {
        return;
    }

    let messageIndex = 0;
    loadingOverlay.classList.add('is-visible');
    loadingOverlay.setAttribute('aria-hidden', 'false');
    loadingStatus.textContent = loadingMessages[messageIndex];

    // Clear any previous timer before starting a new one (prevents stacking).
    if (loadingTimer) {
        window.clearInterval(loadingTimer);
    }
    loadingTimer = window.setInterval(() => {
        messageIndex = (messageIndex + 1) % loadingMessages.length;
        loadingStatus.textContent = loadingMessages[messageIndex];
    }, 1400);
}

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

        startLoadingMessages();
    });
}

