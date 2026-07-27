import math
from dataclasses import dataclass


class HeadingCalculationError(Exception):
    """Raised when route headings cannot be calculated."""


@dataclass(frozen=True)
class RouteSegmentHeading:
    """Heading details for one route segment."""

    segment_index: int
    start: list[float]
    end: list[float]
    heading: float


def calculate_route_headings(
    route_coordinates: list[list[float]],
) -> list[RouteSegmentHeading]:
    """Calculate compass headings for consecutive route coordinate pairs."""
    _validate_route_coordinates(route_coordinates)

    headings: list[RouteSegmentHeading] = []
    for index in range(len(route_coordinates) - 1):
        start = route_coordinates[index]
        end = route_coordinates[index + 1]
        headings.append(
            RouteSegmentHeading(
                segment_index=index,
                start=start,
                end=end,
                heading=calculate_heading(start, end),
            )
        )

    return headings


def calculate_heading(start: list[float], end: list[float]) -> float:
    """Calculate heading in degrees from one coordinate to another."""
    _validate_coordinate(start, 'start')
    _validate_coordinate(end, 'end')

    start_lon, start_lat = start
    end_lon, end_lat = end

    start_lat_rad = math.radians(start_lat)
    end_lat_rad = math.radians(end_lat)
    delta_lon_rad = math.radians(end_lon - start_lon)

    x = math.sin(delta_lon_rad) * math.cos(end_lat_rad)
    y = (
        math.cos(start_lat_rad) * math.sin(end_lat_rad)
        - math.sin(start_lat_rad)
        * math.cos(end_lat_rad)
        * math.cos(delta_lon_rad)
    )
    bearing = math.degrees(math.atan2(x, y))
    return round((bearing + 360) % 360, 2)


def serialize_headings(
    headings: list[RouteSegmentHeading],
) -> list[dict[str, object]]:
    """Convert heading dataclasses to JSON-serializable dictionaries."""
    return [
        {
            'segment_index': item.segment_index,
            'start': item.start,
            'end': item.end,
            'heading': item.heading,
        }
        for item in headings
    ]


def _validate_route_coordinates(route_coordinates: list[list[float]]) -> None:
    if not route_coordinates:
        raise HeadingCalculationError('Route coordinates are required.')
    if len(route_coordinates) < 2:
        raise HeadingCalculationError('At least two route coordinates are required.')

    for index, coordinate in enumerate(route_coordinates):
        _validate_coordinate(coordinate, f'coordinate {index}')


def _validate_coordinate(coordinate: list[float], label: str) -> None:
    if not isinstance(coordinate, list) or len(coordinate) < 2:
        raise HeadingCalculationError(f'{label} must contain longitude and latitude.')

    longitude = coordinate[0]
    latitude = coordinate[1]
    if not isinstance(longitude, int | float) or not isinstance(latitude, int | float):
        raise HeadingCalculationError(f'{label} must contain numeric values.')
    if not -180 <= longitude <= 180:
        raise HeadingCalculationError(f'{label} longitude must be between -180 and 180.')
    if not -90 <= latitude <= 90:
        raise HeadingCalculationError(f'{label} latitude must be between -90 and 90.')
