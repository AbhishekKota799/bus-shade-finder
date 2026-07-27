import logging
from datetime import date, datetime

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from config import Config
from services.geocoder import GeocodingError, geocode_address
from services.heading import (
    HeadingCalculationError,
    calculate_route_headings,
    serialize_headings,
)
from services.journey_analyzer import JourneyAnalyzer
from services.relative_sun import (
    RelativeSunError,
    classify_route_segments,
    serialize_relative_positions,
)
from services.routing import (
    RoutingError,
    format_distance,
    format_duration,
    get_driving_route,
)
from services.recommendation import (
    RecommendationError,
    recommend_side,
    serialize_recommendation,
)
from services.shade import (
    ShadeExposureError,
    calculate_side_exposure,
    serialize_exposure_summary,
)
from services.solar import SolarCalculationError, calculate_solar_position
from services.timeline import TimelineError

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET', 'POST'])
def home():
    """Render the home page and handle route lookup submissions."""
    context = _default_context()

    if request.method == 'POST':
        form_values = _get_form_values()
        errors = _validate_form_values(form_values)
        context.update(form_values)

        if errors:
            context['errors'] = errors
            context['status_message'] = 'Please fix the highlighted fields.'
        else:
            context.update(_build_route_context(form_values))

    return render_template('index.html', **context)


@app.route('/api/solar')
def solar_data():
    """Return solar azimuth and elevation for query parameters as JSON."""
    try:
        latitude = float(request.args.get('latitude', ''))
        longitude = float(request.args.get('longitude', ''))
        date_value = request.args.get('date', '').strip()
        time_value = request.args.get('time', '').strip()
        timezone_name = request.args.get('timezone', 'UTC').strip() or 'UTC'
        when = datetime.strptime(f'{date_value} {time_value}', '%Y-%m-%d %H:%M')
        position = calculate_solar_position(
            latitude=latitude,
            longitude=longitude,
            when=when,
            timezone_name=timezone_name,
        )
    except ValueError:
        return jsonify({'error': 'Latitude, longitude, date, and time are required and must be valid.'}), 400
    except SolarCalculationError as exc:
        logger.warning('Solar calculation failed: %s', exc)
        return jsonify({'error': str(exc)}), 400

    return jsonify(
        {
            'azimuth': position.azimuth,
            'elevation': position.elevation,
        }
    )


@app.post('/api/headings')
def route_headings():
    """Return travel headings for submitted route coordinates as JSON."""
    payload = request.get_json(silent=True) or {}
    route_coordinates = payload.get('route_coordinates')

    try:
        headings = calculate_route_headings(route_coordinates)
    except HeadingCalculationError as exc:
        logger.warning('Heading calculation failed: %s', exc)
        return jsonify({'error': str(exc)}), 400

    return jsonify(
        {
            'segment_count': len(headings),
            'headings': serialize_headings(headings),
        }
    )


@app.post('/api/relative-sun')
def relative_sun_data():
    """Return sun position classifications for segment headings as JSON."""
    payload = request.get_json(silent=True) or {}

    try:
        sun_azimuth = float(payload.get('sun_azimuth', ''))
        positions = classify_route_segments(
            payload.get('headings'),
            sun_azimuth,
        )
    except (ValueError, TypeError):
        return jsonify({'error': 'Sun azimuth is required and must be numeric.'}), 400
    except RelativeSunError as exc:
        logger.warning('Relative sun calculation failed: %s', exc)
        return jsonify({'error': str(exc)}), 400

    return jsonify(
        {
            'segment_count': len(positions),
            'relative_sun': serialize_relative_positions(positions),
        }
    )


@app.post('/api/shade-exposure')
def shade_exposure_data():
    """Return left and right sunlight exposure counts for route segments."""
    payload = request.get_json(silent=True) or {}

    try:
        summary = calculate_side_exposure(payload.get('segments'))
        recommendation = recommend_side(
            summary.exposure_percentage['left'],
            summary.exposure_percentage['right'],
        )
    except (ShadeExposureError, RecommendationError) as exc:
        logger.warning('Shade exposure calculation failed: %s', exc)
        return jsonify({'error': str(exc)}), 400

    response = serialize_exposure_summary(summary)
    response['recommendation'] = serialize_recommendation(recommendation)
    return jsonify(response)


def _default_context() -> dict[str, object]:
    return {
        'current_year': date.today().year,
        'recommended_side': '--',
        'shade_score': '--',
        'sunny_side': '--',
        'estimated_travel_time': '--',
        'route_distance': '--',
        'status_message': 'Enter a journey to retrieve route details.',
        'errors': [],
        'route_coordinates': [],
        'start_marker': None,
        'destination_marker': None,
    }


def _get_form_values() -> dict[str, str]:
    return {
        'start_location': request.form.get('start_location', '').strip(),
        'destination': request.form.get('destination', '').strip(),
        'departure_date': request.form.get('departure_date', '').strip(),
        'departure_time': request.form.get('departure_time', '').strip(),
    }


def _validate_form_values(form_values: dict[str, str]) -> list[str]:
    errors: list[str] = []

    if not form_values['start_location']:
        errors.append('Starting location is required.')
    if not form_values['destination']:
        errors.append('Destination is required.')
    if not form_values['departure_date']:
        errors.append('Departure date is required.')
    else:
        try:
            datetime.strptime(form_values['departure_date'], '%Y-%m-%d')
        except ValueError:
            errors.append('Departure date must be a valid date.')
    if not form_values['departure_time']:
        errors.append('Departure time is required.')
    else:
        try:
            datetime.strptime(form_values['departure_time'], '%H:%M')
        except ValueError:
            errors.append('Departure time must be a valid time.')

    if (
        form_values['start_location']
        and form_values['destination']
        and form_values['start_location'].casefold()
        == form_values['destination'].casefold()
    ):
        errors.append('Starting location and destination must be different.')

    return errors


def _build_route_context(form_values: dict[str, str]) -> dict[str, object]:
    try:
        analyzer = JourneyAnalyzer(
            geocoder_base_url=app.config['GEOCODER_BASE_URL'],
            geocoder_user_agent=app.config['GEOCODER_USER_AGENT'],
            osrm_base_url=app.config['OSRM_BASE_URL'],
            request_timeout_seconds=app.config['REQUEST_TIMEOUT_SECONDS'],
        )
        departure_time = datetime.strptime(
            f"{form_values['departure_date']} {form_values['departure_time']}",
            '%Y-%m-%d %H:%M',
        )
        analysis = analyzer.analyze(
            source=form_values['start_location'],
            destination=form_values['destination'],
            departure_time=departure_time,
        )
    except (
        GeocodingError,
        HeadingCalculationError,
        RecommendationError,
        RelativeSunError,
        RoutingError,
        ShadeExposureError,
        SolarCalculationError,
        TimelineError,
    ) as exc:
        logger.warning('Route lookup failed: %s', exc)
        return {
            'errors': [str(exc)],
            'status_message': 'Route lookup failed. Please check the locations and try again.',
        }

    route = analysis['route']
    recommendation = analysis['recommendation']
    logger.info(
        'Route retrieved: %s to %s, %.0f meters, %.0f seconds, %s turns',
        route['origin']['label'],
        route['destination']['label'],
        route['distance_meters'],
        route['duration_seconds'],
        route['turn_count'],
    )
    return {
        'estimated_travel_time': route['duration'],
        'route_distance': route['distance'],
        'status_message': 'Driving route retrieved successfully.',
        'route_coordinate_count': route['coordinate_count'],
        'turn_count': route['turn_count'],
        'route_coordinates': route['coordinates'],
        'start_marker': route['origin'],
        'destination_marker': route['destination'],
        'recommended_side': recommendation['recommended_side'],
        'shade_score': recommendation['confidence'],
    }


if __name__ == '__main__':
    app.run(debug=True)
