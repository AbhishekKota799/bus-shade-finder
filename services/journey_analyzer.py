from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable

from services.geocoder import Location, geocode_address
from services.heading import calculate_route_headings, serialize_headings
from services.recommendation import recommend_side, serialize_recommendation
from services.relative_sun import (
    classify_route_segments,
    serialize_relative_positions,
)
from services.routing import format_distance, format_duration, get_driving_route
from services.shade import (
    calculate_side_exposure,
    serialize_exposure_summary,
    serialize_segment_exposure,
)
from services.solar import calculate_solar_position
from services.timeline import build_journey_timeline, estimate_segment_timestamp


@dataclass(frozen=True)
class JourneyAnalyzer:
    """Orchestrates route, sun, exposure, and recommendation analysis."""

    geocoder_base_url: str
    geocoder_user_agent: str
    osrm_base_url: str
    request_timeout_seconds: float
    timezone_name: str = 'Asia/Kolkata'
    geocode_func: Callable[..., Location] = geocode_address  # allows caching

    def analyze(self, source: str, destination: str, departure_time: datetime) -> dict[str, Any]:
        """Return route, exposure, and recommendation for a journey."""
        origin = self.geocode_func(
            source,
            self.geocoder_base_url,
            self.geocoder_user_agent,
            self.request_timeout_seconds,
        )
        destination_location = self.geocode_func(
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
        heading_items = serialize_headings(calculate_route_headings(route.coordinates))
        analyzed_segments = self._analyze_segments(
            heading_items,
            departure_time,
            route.duration_seconds,
        )
        exposure_input = [
            {
                'segment_index': segment['segment_index'],
                'heading': segment['heading'],
                'sun_azimuth': segment['sun_azimuth'],
                'sun_elevation': segment['sun_elevation'],
                'weight': segment['weight'],
            }
            for segment in analyzed_segments
        ]
        exposure = calculate_side_exposure(exposure_input)
        recommendation = recommend_side(
            exposure.exposure_percentage['left'],
            exposure.exposure_percentage['right'],
        )
        relative_positions = [
            classify_route_segments([segment], segment['sun_azimuth'])[0]
            for segment in exposure_input
        ]

        return {
            'route': _serialize_route(origin, destination_location, route),
            'headings': heading_items,
            'solar_positions': [
                {
                    'azimuth': segment['sun_azimuth'],
                    'elevation': segment['sun_elevation'],
                }
                for segment in analyzed_segments
            ],
            'relative_sun': serialize_relative_positions(relative_positions),
            'exposure': serialize_exposure_summary(exposure),
            'recommendation': serialize_recommendation(recommendation),
            'timeline': build_journey_timeline(
                _merge_exposure_into_segments(analyzed_segments, exposure),
            ),
        }

    def _analyze_segments(
        self,
        heading_items: list[dict[str, object]],
        departure_time: datetime,
        duration_seconds: float,
    ) -> list[dict[str, Any]]:
        total_weight = sum(
            max(float(item.get('distance_meters', 0)), 0.0)
            for item in heading_items
        )
        if total_weight <= 0:
            return []

        elapsed_weight = 0.0
        analyzed_segments: list[dict[str, Any]] = []

        for item in heading_items:
            weight = max(float(item.get('distance_meters', 0)), 0.0)
            segment_duration_seconds = duration_seconds * (weight / total_weight)
            timestamp = estimate_segment_timestamp(
                departure_time,
                elapsed_weight,
                total_weight,
                duration_seconds,
            )
            longitude, latitude = item['start']
            position = calculate_solar_position(
                latitude=latitude,
                longitude=longitude,
                when=timestamp,
                timezone_name=self.timezone_name,
            )
            analyzed_segments.append(
                {
                    'segment_index': item['segment_index'],
                    'start': item['start'],
                    'end': item['end'],
                    'heading': item['heading'],
                    'weight': weight,
                    'segment_duration_seconds': segment_duration_seconds,
                    'timestamp': timestamp,
                    'sun_azimuth': position.azimuth,
                    'sun_elevation': position.elevation,
                }
            )
            elapsed_weight += weight

        return analyzed_segments


def _merge_exposure_into_segments(
    analyzed_segments: list[dict[str, Any]],
    exposure: Any,
) -> list[dict[str, Any]]:
    exposure_by_index = {
        segment.segment_index: serialize_segment_exposure(segment)
        for segment in exposure.segments
    }
    merged_segments: list[dict[str, Any]] = []

    for segment in analyzed_segments:
        exposure_item = exposure_by_index[segment['segment_index']]
        merged = dict(segment)
        merged['left_exposure'] = exposure_item['left_exposure']
        merged['right_exposure'] = exposure_item['right_exposure']
        merged_segments.append(merged)

    return merged_segments


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
