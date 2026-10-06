import math
import unittest
from dataclasses import dataclass
from datetime import datetime, timedelta
from unittest.mock import patch

from services.geocoder import Location
from services.heading import (
    HeadingCalculationError,
    calculate_heading,
    calculate_route_headings,
)
from services.journey_analyzer import JourneyAnalyzer
from services.recommendation import RecommendationError, recommend_side
from services.relative_sun import calculate_signed_relative_angle
from services.routing import RouteSummary
from services.shade import ShadeExposureError, calculate_side_exposure
from services.solar import SolarCalculationError, SolarPosition, calculate_solar_position
from services.timeline import build_journey_timeline


class GeometryTests(unittest.TestCase):
    def test_signed_relative_angle_uses_right_positive_left_negative(self) -> None:
        self.assertEqual(calculate_signed_relative_angle(0, 90), 90)
        self.assertEqual(calculate_signed_relative_angle(0, 270), -90)
        self.assertEqual(calculate_signed_relative_angle(90, 0), -90)
        self.assertEqual(calculate_signed_relative_angle(90, 180), 90)

    def test_heading_rejects_zero_length_segment(self) -> None:
        with self.assertRaises(HeadingCalculationError):
            calculate_heading([77.0, 28.0], [77.0, 28.0])

    def test_route_heading_skips_duplicate_coordinates(self) -> None:
        headings = calculate_route_headings([[0.0, 0.0], [0.0, 0.0], [1.0, 0.0]])
        self.assertEqual(len(headings), 1)
        self.assertAlmostEqual(headings[0].heading, 90.0, places=1)

    def test_boolean_coordinates_are_rejected(self) -> None:
        with self.assertRaises(HeadingCalculationError):
            calculate_heading([True, 28.0], [77.1, 28.1])


class ExposureTests(unittest.TestCase):
    def test_left_and_right_side_exposure_geometry(self) -> None:
        right = calculate_side_exposure([
            {'heading': 0, 'sun_azimuth': 90, 'sun_elevation': 45, 'weight': 1},
        ])
        left = calculate_side_exposure([
            {'heading': 0, 'sun_azimuth': 270, 'sun_elevation': 45, 'weight': 1},
        ])

        self.assertGreater(right.exposure_percentage['right'], 0)
        self.assertEqual(right.exposure_percentage['left'], 0)
        self.assertGreater(left.exposure_percentage['left'], 0)
        self.assertEqual(left.exposure_percentage['right'], 0)

    def test_front_rear_and_night_have_no_side_exposure(self) -> None:
        summary = calculate_side_exposure([
            {'heading': 0, 'sun_azimuth': 0, 'sun_elevation': 45, 'weight': 1},
            {'heading': 0, 'sun_azimuth': 180, 'sun_elevation': 45, 'weight': 1},
            {'heading': 0, 'sun_azimuth': 90, 'sun_elevation': -5, 'weight': 1},
        ])
        self.assertEqual(summary.exposure_percentage, {'left': 0.0, 'right': 0.0})

    def test_exposure_increases_with_sun_elevation(self) -> None:
        low = calculate_side_exposure([
            {'heading': 0, 'sun_azimuth': 90, 'sun_elevation': 10, 'weight': 1},
        ])
        high = calculate_side_exposure([
            {'heading': 0, 'sun_azimuth': 90, 'sun_elevation': 80, 'weight': 1},
        ])
        self.assertGreater(high.exposure_percentage['right'], low.exposure_percentage['right'])

    def test_exposure_is_distance_weighted(self) -> None:
        summary = calculate_side_exposure([
            {'heading': 0, 'sun_azimuth': 90, 'sun_elevation': 45, 'weight': 1000},
            {'heading': 0, 'sun_azimuth': 270, 'sun_elevation': 45, 'weight': 10},
        ])
        self.assertGreater(summary.exposure_percentage['right'], summary.exposure_percentage['left'])

    def test_invalid_segment_values_are_rejected(self) -> None:
        with self.assertRaises(ShadeExposureError):
            calculate_side_exposure([
                {'heading': True, 'sun_azimuth': 90, 'sun_elevation': 45, 'weight': 1},
            ])


class RecommendationTests(unittest.TestCase):
    def test_recommendation_threshold_and_zero_sunlight(self) -> None:
        self.assertEqual(recommend_side(10, 13).recommended_side, 'Either Side')
        self.assertEqual(recommend_side(0, 0).recommended_side, 'Either Side')
        self.assertEqual(recommend_side(10, 80).recommended_side, 'Left')
        self.assertEqual(recommend_side(80, 10).recommended_side, 'Right')

    def test_boolean_percentages_are_rejected(self) -> None:
        with self.assertRaises(RecommendationError):
            recommend_side(True, 10)


class SolarTests(unittest.TestCase):
    def test_solar_service_rejects_boolean_coordinates(self) -> None:
        with self.assertRaises(SolarCalculationError):
            calculate_solar_position(True, 77.0, datetime(2026, 1, 1, 12, 0))


class TimelineTests(unittest.TestCase):
    def test_timeline_starts_at_departure_and_ends_at_arrival(self) -> None:
        departure = datetime(2026, 1, 1, 8, 0)
        segments = [
            {
                'start': [0.0, 0.0],
                'end': [1.0, 0.0],
                'timestamp': departure,
                'segment_duration_seconds': 600,
                'heading': 90,
                'sun_azimuth': 180,
                'sun_elevation': 45,
                'left_exposure': 0,
                'right_exposure': math.sqrt(0.5),
            },
            {
                'start': [1.0, 0.0],
                'end': [1.0, 1.0],
                'timestamp': departure + timedelta(seconds=600),
                'segment_duration_seconds': 600,
                'heading': 0,
                'sun_azimuth': 180,
                'sun_elevation': 45,
                'left_exposure': 0,
                'right_exposure': 0,
            },
        ]

        timeline = build_journey_timeline(segments)

        self.assertEqual(timeline[0]['time'], '2026-01-01T08:00')
        self.assertEqual(timeline[-1]['time'], '2026-01-01T08:20')
        self.assertEqual(timeline[-1]['latitude'], 1.0)
        self.assertEqual(timeline[-1]['longitude'], 1.0)


@dataclass(frozen=True)
class FakeSolarSequence:
    positions: list[SolarPosition]
    index: int = 0

    def next(self, **_: object) -> SolarPosition:
        position = self.positions[min(self.index, len(self.positions) - 1)]
        object.__setattr__(self, 'index', self.index + 1)
        return position


class JourneyAnalyzerTests(unittest.TestCase):
    def test_analyzer_returns_route_exposure_recommendation_and_timeline(self) -> None:
        def fake_geocode(address: str, *_: object) -> Location:
            return Location(address, address, 0.0, 0.0)

        route = RouteSummary(
            distance_meters=222000,
            duration_seconds=1200,
            geometry={'type': 'LineString', 'coordinates': [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]]},
            coordinates=[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]],
            turns=[],
        )
        solar_sequence = FakeSolarSequence([
            SolarPosition(azimuth=180, elevation=45),
            SolarPosition(azimuth=180, elevation=45),
        ])
        analyzer = JourneyAnalyzer('', '', '', 1, geocode_func=fake_geocode)

        with patch('services.journey_analyzer.get_driving_route', return_value=route), patch(
            'services.journey_analyzer.calculate_solar_position',
            side_effect=solar_sequence.next,
        ):
            result = analyzer.analyze('Start', 'End', datetime(2026, 1, 1, 8, 0))

        self.assertIn('route', result)
        self.assertIn('exposure', result)
        self.assertIn('recommendation', result)
        self.assertIn('timeline', result)
        self.assertEqual(result['recommendation']['recommended_side'], 'Left')
        self.assertEqual(result['timeline'][-1]['time'], '2026-01-01T08:20')


if __name__ == '__main__':
    unittest.main()
