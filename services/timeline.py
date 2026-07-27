from dataclasses import dataclass
from datetime import datetime, timedelta

from services.heading import HeadingCalculationError, calculate_heading
from services.recommendation import recommend_side
from services.shade import ShadeExposureError, calculate_side_exposure
from services.solar import SolarCalculationError, calculate_solar_position

DEFAULT_TIMELINE_SEGMENTS = 12


class TimelineError(Exception):
    """Raised when a journey timeline cannot be generated."""


@dataclass(frozen=True)
class TimelineEntry:
    """Sunlight exposure snapshot for one journey segment."""

    time: str
    latitude: float
    longitude: float
    recommended_side: str
    left_exposure: bool
    right_exposure: bool


def build_journey_timeline(
    route_coordinates: list[list[float]],
    departure_time: datetime,
    duration_seconds: float,
    timezone_name: str = 'UTC',
    segment_count: int = DEFAULT_TIMELINE_SEGMENTS,
) -> list[dict[str, object]]:
    """Build ordered sunlight exposure snapshots across a route."""
    _validate_timeline_inputs(route_coordinates, duration_seconds, segment_count)
    coordinate_pairs = _build_evenly_spaced_pairs(route_coordinates, segment_count)
    total_pairs = len(coordinate_pairs)
    timeline: list[dict[str, object]] = []

    for index, (start, end) in enumerate(coordinate_pairs):
        timestamp = departure_time + timedelta(
            seconds=(duration_seconds * index) / total_pairs,
        )
        longitude, latitude = start
        heading = _calculate_heading(start, end)
        solar_position = _calculate_solar_position(
            latitude,
            longitude,
            timestamp,
            timezone_name,
        )
        exposure = _calculate_exposure(heading, solar_position.azimuth)
        recommendation = recommend_side(
            exposure.exposure_percentage['left'],
            exposure.exposure_percentage['right'],
        )
        segment_exposure = exposure.segments[0]

        timeline.append(
            {
                'time': timestamp.isoformat(timespec='minutes'),
                'latitude': round(latitude, 6),
                'longitude': round(longitude, 6),
                'recommended_side': recommendation.recommended_side,
                'left_exposure': segment_exposure.left_exposed,
                'right_exposure': segment_exposure.right_exposed,
            }
        )

    return timeline


def _build_evenly_spaced_pairs(
    route_coordinates: list[list[float]],
    requested_segments: int,
) -> list[tuple[list[float], list[float]]]:
    available_segments = len(route_coordinates) - 1
    segment_count = min(requested_segments, available_segments)
    pairs: list[tuple[list[float], list[float]]] = []

    for index in range(segment_count):
        start_index = int((index * available_segments) / segment_count)
        end_index = int(((index + 1) * available_segments) / segment_count)
        if end_index <= start_index:
            end_index = start_index + 1
        pairs.append((route_coordinates[start_index], route_coordinates[end_index]))

    return pairs


def _calculate_heading(start: list[float], end: list[float]) -> float:
    try:
        return calculate_heading(start, end)
    except HeadingCalculationError as exc:
        raise TimelineError(str(exc)) from exc


def _calculate_solar_position(
    latitude: float,
    longitude: float,
    timestamp: datetime,
    timezone_name: str,
):
    try:
        return calculate_solar_position(
            latitude=latitude,
            longitude=longitude,
            when=timestamp,
            timezone_name=timezone_name,
        )
    except SolarCalculationError as exc:
        raise TimelineError(str(exc)) from exc


def _calculate_exposure(heading: float, sun_azimuth: float):
    try:
        return calculate_side_exposure(
            [
                {
                    'segment_index': 0,
                    'heading': heading,
                    'sun_azimuth': sun_azimuth,
                }
            ]
        )
    except ShadeExposureError as exc:
        raise TimelineError(str(exc)) from exc


def _validate_timeline_inputs(
    route_coordinates: list[list[float]],
    duration_seconds: float,
    segment_count: int,
) -> None:
    if not isinstance(route_coordinates, list) or len(route_coordinates) < 2:
        raise TimelineError('At least two route coordinates are required.')
    if not isinstance(duration_seconds, int | float) or duration_seconds < 0:
        raise TimelineError('Route duration must be a non-negative number.')
    if not isinstance(segment_count, int) or segment_count < 1:
        raise TimelineError('Timeline segment count must be at least 1.')
