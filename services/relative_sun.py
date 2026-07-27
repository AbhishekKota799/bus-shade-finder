from dataclasses import dataclass
from typing import Any


class RelativeSunError(Exception):
    """Raised when relative sun position cannot be classified."""


@dataclass(frozen=True)
class SegmentSunPosition:
    """Relative sun position for one route segment."""

    segment_index: int
    heading: float
    sun_azimuth: float
    relative_angle: float
    sunlight_side: str


def classify_sun_position(bus_heading: float, sun_azimuth: float) -> str:
    """Classify sun position relative to the bus heading."""
    _validate_angle(bus_heading, 'Bus heading')
    _validate_angle(sun_azimuth, 'Sun azimuth')

    relative_angle = calculate_relative_angle(bus_heading, sun_azimuth)
    if relative_angle < 45 or relative_angle >= 315:
        return 'FRONT'
    if 45 <= relative_angle < 135:
        return 'RIGHT'
    if 135 <= relative_angle < 225:
        return 'REAR'
    return 'LEFT'


def calculate_relative_angle(bus_heading: float, sun_azimuth: float) -> float:
    """Return sun azimuth relative to bus heading, normalized to 0-360 degrees."""
    _validate_angle(bus_heading, 'Bus heading')
    _validate_angle(sun_azimuth, 'Sun azimuth')
    return round((sun_azimuth - bus_heading + 360) % 360, 2)


def classify_route_segments(
    segment_headings: list[dict[str, Any]],
    sun_azimuth: float,
) -> list[SegmentSunPosition]:
    """Classify relative sun position for every route segment heading."""
    _validate_angle(sun_azimuth, 'Sun azimuth')
    if not isinstance(segment_headings, list) or not segment_headings:
        raise RelativeSunError('Segment headings are required.')

    positions: list[SegmentSunPosition] = []
    for index, segment in enumerate(segment_headings):
        if not isinstance(segment, dict):
            raise RelativeSunError(f'Segment {index} must be an object.')

        heading = segment.get('heading')
        if not isinstance(heading, int | float):
            raise RelativeSunError(f'Segment {index} heading must be numeric.')

        segment_index = segment.get('segment_index', index)
        if not isinstance(segment_index, int):
            raise RelativeSunError(f'Segment {index} segment_index must be an integer.')

        relative_angle = calculate_relative_angle(float(heading), sun_azimuth)
        positions.append(
            SegmentSunPosition(
                segment_index=segment_index,
                heading=round(float(heading), 2),
                sun_azimuth=round(float(sun_azimuth), 2),
                relative_angle=relative_angle,
                sunlight_side=classify_sun_position(float(heading), sun_azimuth),
            )
        )

    return positions


def serialize_relative_positions(
    positions: list[SegmentSunPosition],
) -> list[dict[str, object]]:
    """Convert relative sun positions to JSON-serializable dictionaries."""
    return [
        {
            'segment_index': item.segment_index,
            'heading': item.heading,
            'sun_azimuth': item.sun_azimuth,
            'relative_angle': item.relative_angle,
            'sunlight_side': item.sunlight_side,
        }
        for item in positions
    ]


def _validate_angle(value: float, label: str) -> None:
    if not isinstance(value, int | float):
        raise RelativeSunError(f'{label} must be numeric.')
    if not 0 <= value < 360:
        raise RelativeSunError(f'{label} must be between 0 and 360 degrees.')
