from dataclasses import dataclass
from datetime import datetime
from typing import Any

from services.geocoder import Location, geocode_address
from services.heading import calculate_route_headings, serialize_headings
from services.recommendation import recommend_side, serialize_recommendation
from services.relative_sun import classify_route_segments, serialize_relative_positions
from services.routing import (
    format_distance,
    format_duration,
    get_driving_route,
)
from services.shade import calculate_side_exposure, serialize_exposure_summary
from services.solar import calculate_solar_position
from services.timeline import build_journey_timeline


@dataclass(frozen=True)
class JourneyAnalyzer:
    """Orchestrates route, sun, exposure, and recommendation analysis."""

    geocoder_base_url: str
    geocoder_user_agent: str
    osrm_base_url: str
    request_timeout_seconds: float
    timezone_name: str = 'UTC'

    def analyze(
        self,
        source: str,
        destination: str,
        departure_time: datetime,
    ) -> dict[str, Any]:
        """Return route, exposure, and recommendation for a journey."""
        origin = geocode_address(
            source,
            self.geocoder_base_url,
            self.geocoder_user_agent,
            self.request_timeout_seconds,
        )
        destination_location = geocode_address(
            destination,
            self.geocoder_base_url,
            self.geocoder_user_agent,
            self.request_timeout_seconds,
        )
        route = get_driving_route(
            origin,
            destination_location,
            self.osrm_base_url,
            self.request_timeout_seconds,
        )
        headings = calculate_route_headings(route.coordinates)
        heading_items = serialize_headings(headings)
        solar_items = self._calculate_segment_solar_positions(
            heading_items,
            departure_time,
        )
        exposure_segments = [
            {
                'segment_index': heading['segment_index'],
                'heading': heading['heading'],
                'sun_azimuth': solar['azimuth'],
            }
            for heading, solar in zip(heading_items, solar_items, strict=True)
        ]
        relative_positions = [
            classify_route_segments([segment], segment['sun_azimuth'])[0]
            for segment in exposure_segments
        ]
        exposure = calculate_side_exposure(exposure_segments)
        recommendation = recommend_side(
            exposure.exposure_percentage['left'],
            exposure.exposure_percentage['right'],
        )

        return {
            'route': _serialize_route(origin, destination_location, route),
            'headings': heading_items,
            'solar_positions': solar_items,
            'relative_sun': serialize_relative_positions(relative_positions),
            'exposure': serialize_exposure_summary(exposure),
            'recommendation': serialize_recommendation(recommendation),
            'timeline': build_journey_timeline(
                route_coordinates=route.coordinates,
                departure_time=departure_time,
                duration_seconds=route.duration_seconds,
                timezone_name=self.timezone_name,
            ),
        }

    def _calculate_segment_solar_positions(
        self,
        headings: list[dict[str, object]],
        departure_time: datetime,
    ) -> list[dict[str, float]]:
        solar_positions: list[dict[str, float]] = []
        for heading in headings:
            longitude, latitude = heading['start']
            position = calculate_solar_position(
                latitude=latitude,
                longitude=longitude,
                when=departure_time,
                timezone_name=self.timezone_name,
            )
            solar_positions.append(
                {
                    'azimuth': position.azimuth,
                    'elevation': position.elevation,
                }
            )
        return solar_positions


def _serialize_route(
    origin: Location,
    destination: Location,
    route: Any,
) -> dict[str, Any]:
    return {
        'distance_meters': route.distance_meters,
        'duration_seconds': route.duration_seconds,
        'distance': format_distance(route.distance_meters),
        'duration': format_duration(route.duration_seconds),
        'geometry': route.geometry,
        'coordinates': route.coordinates,
        'coordinate_count': len(route.coordinates),
        'turns': route.turns,
        'turn_count': len(route.turns),
        'origin': {
            'label': origin.display_name,
            'latitude': origin.latitude,
            'longitude': origin.longitude,
        },
        'destination': {
            'label': destination.display_name,
            'latitude': destination.latitude,
            'longitude': destination.longitude,
        },
    }
