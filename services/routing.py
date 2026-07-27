from dataclasses import dataclass
from typing import Any

import requests

from services.geocoder import Location


class RoutingError(Exception):
    """Raised when OSRM cannot return a usable driving route."""


@dataclass(frozen=True)
class RouteSummary:
    """Parsed route details returned by OSRM."""

    distance_meters: float
    duration_seconds: float
    geometry: dict[str, Any]
    coordinates: list[list[float]]
    turns: list[dict[str, Any]]


def get_driving_route(
    origin: Location,
    destination: Location,
    base_url: str,
    timeout_seconds: float,
) -> RouteSummary:
    """Return the driving route between two geocoded locations."""
    if not base_url:
        raise RoutingError('Routing service is not configured.')

    coordinate_pair = (
        f'{origin.longitude},{origin.latitude};'
        f'{destination.longitude},{destination.latitude}'
    )
    route_url = f'{base_url.rstrip("/")}/route/v1/driving/{coordinate_pair}'

    try:
        response = requests.get(
            route_url,
            params={
                'overview': 'full',
                'geometries': 'geojson',
                'steps': 'true',
            },
            timeout=timeout_seconds,
        )
        response.raise_for_status()
        payload: dict[str, Any] = response.json()
    except requests.RequestException as exc:
        raise RoutingError('Unable to contact the routing service.') from exc
    except ValueError as exc:
        raise RoutingError('The routing service returned invalid data.') from exc

    routes = payload.get('routes')
    if not isinstance(routes, list) or not routes:
        raise RoutingError('No driving route was found for this journey.')

    route = routes[0]
    geometry = route.get('geometry') or {}
    coordinates = geometry.get('coordinates') or []
    if not coordinates:
        raise RoutingError('The route did not include geometry data.')

    return RouteSummary(
        distance_meters=float(route.get('distance', 0)),
        duration_seconds=float(route.get('duration', 0)),
        geometry=geometry,
        coordinates=coordinates,
        turns=_extract_turns(route),
    )


def format_distance(distance_meters: float) -> str:
    """Format a distance in meters for display."""
    if distance_meters >= 1000:
        return f'{distance_meters / 1000:.1f} km'
    return f'{distance_meters:.0f} m'


def format_duration(duration_seconds: float) -> str:
    """Format a duration in seconds for display."""
    minutes = round(duration_seconds / 60)
    if minutes < 60:
        return f'{minutes} min'

    hours = minutes // 60
    remaining_minutes = minutes % 60
    if remaining_minutes == 0:
        return f'{hours} hr'
    return f'{hours} hr {remaining_minutes} min'


def _extract_turns(route: dict[str, Any]) -> list[dict[str, Any]]:
    turns: list[dict[str, Any]] = []
    for leg in route.get('legs', []):
        for step in leg.get('steps', []):
            maneuver = step.get('maneuver', {})
            turns.append(
                {
                    'name': step.get('name', ''),
                    'distance': step.get('distance', 0),
                    'duration': step.get('duration', 0),
                    'type': maneuver.get('type', ''),
                    'modifier': maneuver.get('modifier', ''),
                    'location': maneuver.get('location', []),
                }
            )
    return turns
