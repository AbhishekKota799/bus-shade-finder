from dataclasses import dataclass
from typing import Any

import requests


class GeocodingError(Exception):
    """Raised when a location cannot be converted to coordinates."""


@dataclass(frozen=True)
class Location:
    """A geocoded location returned by the geocoding provider."""

    query: str
    display_name: str
    latitude: float
    longitude: float


def geocode_address(
    address: str,
    base_url: str,
    user_agent: str,
    timeout_seconds: float,
) -> Location:
    """Return coordinates for a human-readable address."""
    if not base_url:
        raise GeocodingError('Geocoding service is not configured.')

    try:
        response = requests.get(
            base_url.rstrip('/'),
            params={
                'q': address,
                'format': 'json',
                'limit': 1,
            },
            headers={'User-Agent': user_agent},
            timeout=timeout_seconds,
        )
        response.raise_for_status()
        payload: Any = response.json()
    except requests.RequestException as exc:
        raise GeocodingError('Unable to contact the geocoding service.') from exc
    except ValueError as exc:
        raise GeocodingError('The geocoding service returned invalid data.') from exc

    if not isinstance(payload, list) or not payload:
        raise GeocodingError(f'No location found for "{address}".')

    first_match = payload[0]
    try:
        return Location(
            query=address,
            display_name=str(first_match.get('display_name', address)),
            latitude=float(first_match['lat']),
            longitude=float(first_match['lon']),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise GeocodingError('The geocoding result was incomplete.') from exc
