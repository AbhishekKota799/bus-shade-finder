const tripForm = document.querySelector('#trip-form');
const loadingOverlay = document.querySelector('#loading-overlay');
const loadingStatus = document.querySelector('#loading-status');
const departureDate = document.querySelector('#departure_date');
const dateChoices = document.querySelectorAll('[data-date-choice]');
const timelineToggle = document.querySelector('#timeline-toggle');
const timelineList = document.querySelector('#timeline-list');
const loadingMessages = [
    'Finding route...',
    'Calculating sun position...',
    'Analyzing shade...',
];

const submitButton = tripForm?.querySelector('button[type="submit"]');
const defaultSubmitButtonMarkup = submitButton?.innerHTML;
let loadingTimer = null;

function formatLocalDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');

    return `${year}-${month}-${day}`;
}

function getLocalDate(offsetDays = 0) {
    const date = new Date();
    date.setHours(0, 0, 0, 0);
    date.setDate(date.getDate() + offsetDays);
    return formatLocalDate(date);
}

function updateDateChoice(selectedChoice) {
    dateChoices.forEach((choice) => {
        choice.setAttribute(
            'aria-pressed',
            String(choice.dataset.dateChoice === selectedChoice),
        );
    });
}

function syncDateChoice() {
    if (!departureDate) {
        return;
    }

    const today = getLocalDate();
    const tomorrow = getLocalDate(1);
    const selectedChoice = departureDate.value === today
        ? 'today'
        : departureDate.value === tomorrow
            ? 'tomorrow'
            : 'other';

    updateDateChoice(selectedChoice);
}

function openDatePicker() {
    if (!departureDate) {
        return;
    }

    departureDate.focus();
    if (typeof departureDate.showPicker === 'function') {
        departureDate.showPicker();
        return;
    }

    departureDate.click();
}

function initializeDateSelector() {
    if (!departureDate || !dateChoices.length) {
        return;
    }

    const today = getLocalDate();
    departureDate.min = today;
    if (!departureDate.value) {
        departureDate.value = today;
    }
    syncDateChoice();

    dateChoices.forEach((choice) => {
        choice.addEventListener('click', () => {
            const selectedChoice = choice.dataset.dateChoice;

            if (selectedChoice === 'today') {
                departureDate.value = today;
                updateDateChoice(selectedChoice);
                return;
            }

            if (selectedChoice === 'tomorrow') {
                departureDate.value = getLocalDate(1);
                updateDateChoice(selectedChoice);
                return;
            }

            updateDateChoice('other');
            openDatePicker();
        });
    });

    departureDate.addEventListener('change', syncDateChoice);
}

function initializeTimelineDisclosure() {
    if (!timelineToggle || !timelineList) {
        return;
    }

    timelineToggle.addEventListener('click', () => {
        const isExpanded = timelineToggle.getAttribute('aria-expanded') === 'true';
        timelineToggle.setAttribute('aria-expanded', String(!isExpanded));
        timelineList.hidden = isExpanded;
    });
}

function stopLoadingMessages() {
    if (loadingTimer) {
        window.clearInterval(loadingTimer);
        loadingTimer = null;
    }

    if (loadingOverlay) {
        loadingOverlay.classList.remove('is-visible');
        loadingOverlay.setAttribute('aria-hidden', 'true');
    }

    if (submitButton) {
        submitButton.disabled = false;
        submitButton.removeAttribute('aria-busy');
        submitButton.innerHTML = defaultSubmitButtonMarkup;
    }
}

function startLoadingMessages() {
    if (!loadingOverlay || !loadingStatus) {
        return;
    }

    let messageIndex = 0;
    loadingOverlay.classList.add('is-visible');
    loadingOverlay.setAttribute('aria-hidden', 'false');
    loadingStatus.textContent = loadingMessages[messageIndex];

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
        if (!tripForm.checkValidity() || !submitButton) {
            return;
        }

        submitButton.disabled = true;
        submitButton.setAttribute('aria-busy', 'true');
        submitButton.textContent = 'Analyzing...';
        startLoadingMessages();
    });
}

initializeDateSelector();
initializeTimelineDisclosure();
window.addEventListener('pageshow', stopLoadingMessages);
