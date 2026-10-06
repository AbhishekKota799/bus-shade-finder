import math
from dataclasses import dataclass
from typing import Any

from services.relative_sun import (
    calculate_signed_relative_angle,
    classify_sun_position,
)

NIGHT_ELEVATION_DEGREES = -0.833
DEFAULT_DAYLIGHT_ELEVATION_DEGREES = 45.0


class ShadeExposureError(Exception):
    """Raised when side exposure cannot be calculated."""


@dataclass(frozen=True)
class SegmentExposure:
    """Continuous sunlight exposure for one route segment."""

    segment_index: int
    heading: float
    sun_azimuth: float
    sun_elevation: float
    relative_angle: float
    sunlight_side: str
    left_exposure: float
    right_exposure: float
    left_exposed: bool
    right_exposed: bool
    weight: float


@dataclass(frozen=True)
class ShadeExposureSummary:
    """Weighted left and right side exposure for a route."""

    left_exposure: float
    right_exposure: float
    exposure_percentage: dict[str, float]
    segments: list[SegmentExposure]


def calculate_side_exposure(
    segments: list[dict[str, Any]],
) -> ShadeExposureSummary:
    """Calculate weighted continuous side exposure across route segments."""
    if not isinstance(segments, list) or not segments:
        raise ShadeExposureError('At least one route segment is required.')

    segment_exposures = [
        calculate_segment_exposure(segment, index)
        for index, segment in enumerate(segments)
    ]
    total_weight = sum(item.weight for item in segment_exposures)
    if total_weight <= 0:
        raise ShadeExposureError('Total segment weight must be greater than zero.')

    left_exposure = sum(
        item.left_exposure * item.weight
        for item in segment_exposures
    )
    right_exposure = sum(
        item.right_exposure * item.weight
        for item in segment_exposures
    )

    return ShadeExposureSummary(
        left_exposure=round(left_exposure, 4),
        right_exposure=round(right_exposure, 4),
        exposure_percentage={
            'left': round((left_exposure / total_weight) * 100, 2),
            'right': round((right_exposure / total_weight) * 100, 2),
        },
        segments=segment_exposures,
    )


def calculate_segment_exposure(
    segment: dict[str, Any],
    fallback_index: int = 0,
) -> SegmentExposure:
    """Calculate continuous side exposure for one route segment."""
    heading, sun_azimuth, sun_elevation, weight, segment_index = _parse_segment(
        segment,
        fallback_index,
    )
    relative_angle = calculate_signed_relative_angle(heading, sun_azimuth)
    left_exposure, right_exposure = _side_exposure_from_angles(
        relative_angle,
        sun_elevation,
    )

    return SegmentExposure(
        segment_index=segment_index,
        heading=round(heading, 2),
        sun_azimuth=round(sun_azimuth, 2),
        sun_elevation=round(sun_elevation, 2),
        relative_angle=relative_angle,
        sunlight_side=classify_sun_position(heading, sun_azimuth),
        left_exposure=round(left_exposure, 4),
        right_exposure=round(right_exposure, 4),
        left_exposed=left_exposure > right_exposure,
        right_exposed=right_exposure > left_exposure,
        weight=round(weight, 4),
    )


def serialize_exposure_summary(
    summary: ShadeExposureSummary,
) -> dict[str, object]:
    """Convert a shade exposure summary to a JSON-serializable dictionary."""
    return {
        'left_exposure': summary.left_exposure,
        'right_exposure': summary.right_exposure,
        'exposure_percentage': summary.exposure_percentage,
        'segments': [
            serialize_segment_exposure(segment)
            for segment in summary.segments
        ],
    }


def serialize_segment_exposure(segment: SegmentExposure) -> dict[str, object]:
    """Convert one segment exposure to a JSON-serializable dictionary."""
    return {
        'segment_index': segment.segment_index,
        'heading': segment.heading,
        'sun_azimuth': segment.sun_azimuth,
        'sun_elevation': segment.sun_elevation,
        'relative_angle': segment.relative_angle,
        'sunlight_side': segment.sunlight_side,
        'left_exposure': segment.left_exposure,
        'right_exposure': segment.right_exposure,
        'left_exposed': segment.left_exposed,
        'right_exposed': segment.right_exposed,
        'weight': segment.weight,
    }


def _side_exposure_from_angles(
    relative_angle: float,
    sun_elevation: float,
) -> tuple[float, float]:
    if sun_elevation <= NIGHT_ELEVATION_DEGREES:
        return 0.0, 0.0

    relative_radians = math.radians(relative_angle)
    elevation_factor = max(0.0, math.sin(math.radians(max(sun_elevation, 0.0))))
    lateral_component = math.sin(relative_radians) * elevation_factor

    return max(0.0, -lateral_component), max(0.0, lateral_component)


def _parse_segment(
    segment: dict[str, Any],
    fallback_index: int,
) -> tuple[float, float, float, float, int]:
    if not isinstance(segment, dict):
        raise ShadeExposureError(f'Segment {fallback_index} must be an object.')

    heading = _read_number(segment, 'heading', fallback_index)
    sun_azimuth = _read_number(segment, 'sun_azimuth', fallback_index)
    sun_elevation = _read_number(
        segment,
        'sun_elevation',
        fallback_index,
        default=DEFAULT_DAYLIGHT_ELEVATION_DEGREES,
    )
    weight = _read_number(
        segment,
        'weight',
        fallback_index,
        default=segment.get('distance_meters', 1.0),
    )
    segment_index = segment.get('segment_index', fallback_index)

    if not isinstance(segment_index, int) or isinstance(segment_index, bool):
        raise ShadeExposureError(
            f'Segment {fallback_index} segment_index must be an integer.'
        )
    if not 0 <= heading < 360:
        raise ShadeExposureError(f'Segment {fallback_index} heading must be 0-360.')
    if not 0 <= sun_azimuth < 360:
        raise ShadeExposureError(f'Segment {fallback_index} sun_azimuth must be 0-360.')
    if not -90 <= sun_elevation <= 90:
        raise ShadeExposureError(
            f'Segment {fallback_index} sun_elevation must be between -90 and 90.'
        )
    if weight <= 0:
        raise ShadeExposureError(f'Segment {fallback_index} weight must be positive.')

    return heading, sun_azimuth, sun_elevation, weight, segment_index


def _read_number(
    segment: dict[str, Any],
    key: str,
    fallback_index: int,
    default: object | None = None,
) -> float:
    value = segment.get(key, default)
    if (
        not isinstance(value, int | float)
        or isinstance(value, bool)
        or not math.isfinite(float(value))
    ):
        raise ShadeExposureError(f'Segment {fallback_index} {key} must be numeric.')
    return float(value)
