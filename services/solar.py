from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from astral import Observer
from astral.sun import azimuth, elevation


class SolarCalculationError(Exception):
    """Raised when sun position cannot be calculated from the input data."""


@dataclass(frozen=True)
class SolarPosition:
    """Sun position angles in degrees."""

    azimuth: float
    elevation: float


def calculate_solar_position(
    latitude: float,
    longitude: float,
    when: datetime,
    timezone_name: str = 'UTC',
) -> SolarPosition:
    """Calculate solar azimuth and elevation for a location and time."""
    _validate_coordinates(latitude, longitude)

    try:
        timezone = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise SolarCalculationError('Timezone is invalid or unavailable.') from exc

    localized_time = when.replace(tzinfo=timezone) if when.tzinfo is None else when.astimezone(timezone)
    observer = Observer(latitude=latitude, longitude=longitude)

    try:
        return SolarPosition(
            azimuth=round(float(azimuth(observer, localized_time)), 2),
            elevation=round(float(elevation(observer, localized_time)), 2),
        )
    except Exception as exc:
        raise SolarCalculationError('Unable to calculate solar position.') from exc


def _validate_coordinates(latitude: float, longitude: float) -> None:
    if not -90 <= latitude <= 90:
        raise SolarCalculationError('Latitude must be between -90 and 90.')
    if not -180 <= longitude <= 180:
        raise SolarCalculationError('Longitude must be between -180 and 180.')
