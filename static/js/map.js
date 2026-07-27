const DEFAULT_CENTER = [20.5937, 78.9629];
const DEFAULT_ZOOM = 5;

function parseMapData(mapElement, key, fallback) {
    try {
        return JSON.parse(mapElement.dataset[key] || 'null') || fallback;
    } catch (error) {
        return fallback;
    }
}

function toLeafletCoordinates(routeCoordinates) {
    return routeCoordinates
        .filter((point) => Array.isArray(point) && point.length >= 2)
        .map(([longitude, latitude]) => [latitude, longitude]);
}

function addRouteMarkers(map, startMarker, destinationMarker) {
    if (startMarker) {
        L.marker([startMarker.latitude, startMarker.longitude])
            .addTo(map)
            .bindPopup('Start: ' + startMarker.label);
    }

    if (destinationMarker) {
        L.marker([destinationMarker.latitude, destinationMarker.longitude])
            .addTo(map)
            .bindPopup('Destination: ' + destinationMarker.label);
    }
}

function initializeRouteMap() {
    const mapElement = document.querySelector('#route-map');

    if (!mapElement || typeof L === 'undefined') {
        return;
    }

    const routeCoordinates = parseMapData(mapElement, 'route', []);
    const startMarker = parseMapData(mapElement, 'start', null);
    const destinationMarker = parseMapData(mapElement, 'destination', null);
    const leafletCoordinates = toLeafletCoordinates(routeCoordinates);
    const map = L.map(mapElement).setView(DEFAULT_CENTER, DEFAULT_ZOOM);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map);

    if (!leafletCoordinates.length) {
        return;
    }

    mapElement.classList.add('has-route');
    const routeLine = L.polyline(leafletCoordinates, {
        color: '#176b87',
        weight: 5,
        opacity: 0.9,
    }).addTo(map);

    addRouteMarkers(map, startMarker, destinationMarker);
    map.fitBounds(routeLine.getBounds(), { padding: [28, 28] });
}

document.addEventListener('DOMContentLoaded', initializeRouteMap);
