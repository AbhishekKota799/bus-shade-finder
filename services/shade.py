from dataclasses import dataclass
from typing import Any

from services.relative_sun import RelativeSunError, classify_sun_position


class ShadeExposureError(Exception):
    """Raised when side exposure cannot be calculated."""


@dataclass(frozen=True)
class SegmentExposure:
    """Sunlight exposure classification for one route segment."""

    segment_index: int
    heading: float
    sun_azimuth: float
    sunlight_side: str
    left_exposed: bool
    right_exposed: bool


@dataclass(frozen=True)
class ShadeExposureSummary:
    """Total left and right side exposure for a route."""

    left_exposure: int
    right_exposure: int
    exposure_percentage: dict[str, float]
    segments: list[SegmentExposure]


def calculate_side_exposure(
    segments: list[dict[str, Any]],
) -> ShadeExposureSummary:
    """Calculate left and right sunlight exposure across route segments."""
    if not isinstance(segments, list) or not segments:
        raise ShadeExposureError('At least one route segment is required.')

    segment_exposures: list[SegmentExposure] = []
    left_exposure = 0
    right_exposure = 0

    for index, segment in enumerate(segments):
        heading, sun_azimuth, segment_index = _parse_segment(segment, index)
        sunlight_side = _classify_segment(heading, sun_azimuth)
        left_exposed = sunlight_side == 'LEFT'
        right_exposed = sunlight_side == 'RIGHT'

        left_exposure += int(left_exposed)
        right_exposure += int(right_exposed)
        segment_exposures.append(
            SegmentExposure(
                segment_index=segment_index,
                heading=round(heading, 2),
                sun_azimuth=round(sun_azimuth, 2),
                sunlight_side=sunlight_side,
                left_exposed=left_exposed,
                right_exposed=right_exposed,
            )
        )

    total_segments = len(segment_exposures)
    return ShadeExposureSummary(
        left_exposure=left_exposure,
        right_exposure=right_exposure,
        exposure_percentage={
            'left': round((left_exposure / total_segments) * 100, 2),
            'right': round((right_exposure / total_segments) * 100, 2),
        },
        segments=segment_exposures,
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
            {
                'segment_index': segment.segment_index,
                'heading': segment.heading,
                'sun_azimuth': segment.sun_azimuth,
                'sunlight_side': segment.sunlight_side,
                'left_exposed': segment.left_exposed,
                'right_exposed': segment.right_exposed,
            }
            for segment in summary.segments
        ],
    }


def _parse_segment(
    segment: dict[str, Any],
    fallback_index: int,
) -> tuple[float, float, int]:
    if not isinstance(segment, dict):
        raise ShadeExposureError(f'Segment {fallback_index} must be an object.')

    heading = segment.get('heading')
    sun_azimuth = segment.get('sun_azimuth')
    segment_index = segment.get('segment_index', fallback_index)

    if not isinstance(heading, int | float):
        raise ShadeExposureError(f'Segment {fallback_index} heading must be numeric.')
    if not isinstance(sun_azimuth, int | float):
        raise ShadeExposureError(f'Segment {fallback_index} sun_azimuth must be numeric.')
    if not isinstance(segment_index, int):
        raise ShadeExposureError(f'Segment {fallback_index} segment_index must be an integer.')

    return float(heading), float(sun_azimuth), segment_index


def _classify_segment(heading: float, sun_azimuth: float) -> str:
    try:
        return classify_sun_position(heading, sun_azimuth)
    except RelativeSunError as exc:
        raise ShadeExposureError(str(exc)) from exc
