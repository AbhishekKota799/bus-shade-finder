from dataclasses import dataclass


class RecommendationError(Exception):
    """Raised when a recommendation cannot be calculated."""


@dataclass(frozen=True)
class SeatRecommendation:
    """Recommended bus side with confidence and explanation."""

    recommended_side: str
    confidence: float
    reason: str


def recommend_side(
    left_percentage: float,
    right_percentage: float,
) -> SeatRecommendation:
    """Recommend the bus side with lower sunlight exposure."""
    _validate_percentage(left_percentage, 'Left exposure')
    _validate_percentage(right_percentage, 'Right exposure')

    difference = abs(left_percentage - right_percentage)
    confidence = round(difference, 2)

    if difference < 5:
        return SeatRecommendation(
            recommended_side='Either Side',
            confidence=confidence,
            reason=(
                'Both sides have nearly equal sunlight exposure, '
                'so either side should feel similar.'
            ),
        )

    if left_percentage < right_percentage:
        return SeatRecommendation(
            recommended_side='Left',
            confidence=confidence,
            reason=(
                'The left side has less estimated sunlight exposure '
                'than the right side.'
            ),
        )

    return SeatRecommendation(
        recommended_side='Right',
        confidence=confidence,
        reason=(
            'The right side has less estimated sunlight exposure '
            'than the left side.'
        ),
    )


def serialize_recommendation(
    recommendation: SeatRecommendation,
) -> dict[str, object]:
    """Convert a seat recommendation to a JSON-serializable dictionary."""
    return {
        'recommended_side': recommendation.recommended_side,
        'confidence': recommendation.confidence,
        'reason': recommendation.reason,
    }


def _validate_percentage(value: float, label: str) -> None:
    if not isinstance(value, int | float):
        raise RecommendationError(f'{label} must be numeric.')
    if not 0 <= value <= 100:
        raise RecommendationError(f'{label} must be between 0 and 100.')
