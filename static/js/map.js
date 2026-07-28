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

function createEndpointIcon(label, className) {
    return L.divIcon({
        className: 'map-marker-shell',
        html: `<span class="map-marker ${className}">${label}</span>`,
        iconSize: [38, 38],
        iconAnchor: [19, 19],
        popupAnchor: [0, -18],
    });
}

function createTimelineIcon(number) {
    return L.divIcon({
        className: 'map-marker-shell',
        html: `<span class="timeline-map-marker">${number}</span>`,
        iconSize: [28, 28],
        iconAnchor: [14, 14],
        popupAnchor: [0, -12],
    });
}

function addRouteMarkers(map, startMarker, destinationMarker) {
    if (startMarker) {
        L.marker([startMarker.latitude, startMarker.longitude], {
            icon: createEndpointIcon('S', 'map-marker--start'),
        })
            .addTo(map)
            .bindPopup('Start: ' + startMarker.label);
    }

    if (destinationMarker) {
        L.marker([destinationMarker.latitude, destinationMarker.longitude], {
            icon: createEndpointIcon('D', 'map-marker--destination'),
        })
            .addTo(map)
            .bindPopup('Destination: ' + destinationMarker.label);
    }
}

function addTimelineMarkers(map, timelineItems) {
    timelineItems
        .filter((item) => Number.isFinite(item.latitude) && Number.isFinite(item.longitude))
        .forEach((item, index) => {
            L.marker([item.latitude, item.longitude], {
                icon: createTimelineIcon(index + 1),
            })
                .addTo(map)
                .bindPopup(
                    `Stop ${index + 1}<br>${item.time}<br>${item.recommended_side}`
                );
        });
}

function initializeRouteMap() {
    const mapElement = document.querySelector('#route-map');

    if (!mapElement || typeof L === 'undefined') {
        return;
    }

    const routeCoordinates = parseMapData(mapElement, 'route', []);
    const startMarker = parseMapData(mapElement, 'start', null);
    const destinationMarker = parseMapData(mapElement, 'destination', null);
    const timelineItems = parseMapData(mapElement, 'timeline', []);
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
    L.polyline(leafletCoordinates, {
        color: '#ffffff',
        weight: 11,
        opacity: 0.95,
    }).addTo(map);
    const routeLine = L.polyline(leafletCoordinates, {
        color: '#0f4f64',
        weight: 7,
        opacity: 1,
        lineJoin: 'round',
        lineCap: 'round',
    }).addTo(map);

    addRouteMarkers(map, startMarker, destinationMarker);
    addTimelineMarkers(map, timelineItems);
    setTimeout(() => {
        const padding = window.matchMedia('(max-width: 760px)').matches ? [36, 36] : [56, 56];

        map.invalidateSize();
        map.fitBounds(routeLine.getBounds(), { padding });
    }, 100);
}

document.addEventListener('DOMContentLoaded', initializeRouteMap);

