from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from services.recommendation import recommend_side

DEFAULT_TIMELINE_SEGMENTS = 12


class TimelineError(Exception):
    """Raised when a journey timeline cannot be generated."""


@dataclass(frozen=True)
class TimelineEntry:
    """Sunlight exposure snapshot for one journey segment."""

    time: str
    latitude: float
    longitude: float
    heading: float
    sun_azimuth: float
    sun_elevation: float
    recommended_side: str
    left_exposure: float
    right_exposure: float


def build_journey_timeline(
    analyzed_segments: list[dict[str, Any]],
    segment_count: int = DEFAULT_TIMELINE_SEGMENTS,
) -> list[dict[str, object]]:
    """Build ordered timeline entries from analyzed route segments."""
    _validate_timeline_inputs(analyzed_segments, segment_count)
    sampled_segments = _sample_evenly(analyzed_segments, segment_count)
    return [
        _serialize_timeline_entry(
            segment,
            use_segment_end=index == len(sampled_segments) - 1
            and segment is analyzed_segments[-1],
        )
        for index, segment in enumerate(sampled_segments)
    ]



def _serialize_timeline_entry(
    segment: dict[str, Any],
    use_segment_end: bool = False,
) -> dict[str, object]:
    """Convert one segment to a timeline entry using true exposure percentages."""
    left_percentage = min(segment['left_exposure'] * 100, 100.0)
    right_percentage = min(segment['right_exposure'] * 100, 100.0)

    recommendation = recommend_side(left_percentage, right_percentage)
    timestamp = segment['timestamp']
    coordinate = segment['start']
    if use_segment_end:
        timestamp += timedelta(seconds=segment.get('segment_duration_seconds', 0))
        coordinate = segment['end']
    longitude, latitude = coordinate

    return {
        'time': timestamp.isoformat(timespec='minutes'),
        'latitude': round(latitude, 6),
        'longitude': round(longitude, 6),
        'heading': round(segment['heading'], 2),
        'sun_azimuth': round(segment['sun_azimuth'], 2),
        'sun_elevation': round(segment['sun_elevation'], 2),
        'recommended_side': recommendation.recommended_side,
        'left_exposure': round(left_percentage, 2),
        'right_exposure': round(right_percentage, 2),
    }


def _sample_evenly(
    analyzed_segments: list[dict[str, Any]],
    requested_segments: int,
) -> list[dict[str, Any]]:
    """Sample unique segments evenly across the route (no duplicates)."""
    total = len(analyzed_segments)

    # Never request more samples than available segments.
    sample_count = min(requested_segments, total)

    if sample_count == 1:
        return [analyzed_segments[0]]

    indices = [
        round(index * (total - 1) / (sample_count - 1))
        for index in range(sample_count)
    ]
    return [analyzed_segments[index] for index in indices]


def estimate_segment_timestamp(
    departure_time: datetime,
    elapsed_weight: float,
    total_weight: float,
    duration_seconds: float,
) -> datetime:
    """Estimate segment timestamp from weighted route progress."""
    if total_weight <= 0:
        raise TimelineError('Total segment weight must be greater than zero.')
    progress = elapsed_weight / total_weight
    return departure_time + timedelta(seconds=duration_seconds * progress)


def _validate_timeline_inputs(
    analyzed_segments: list[dict[str, Any]],
    segment_count: int,
) -> None:
    if not isinstance(analyzed_segments, list) or not analyzed_segments:
        raise TimelineError('At least one analyzed segment is required.')
    if not isinstance(segment_count, int) or segment_count < 1:
        raise TimelineError('Timeline segment count must be at least 1.')
