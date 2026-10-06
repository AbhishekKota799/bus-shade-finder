import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'change_me')
    OSRM_BASE_URL = os.getenv(
        'OSRM_BASE_URL',
        'https://router.project-osrm.org',
    )
    GEOCODER_BASE_URL = os.getenv(
        'GEOCODER_BASE_URL',
        'https://nominatim.openstreetmap.org/search',
    )
    REQUEST_TIMEOUT_SECONDS = float(os.getenv('REQUEST_TIMEOUT_SECONDS', '10'))
    TIMEZONE_NAME = os.getenv('TIMEZONE_NAME', 'Asia/Kolkata')
    GEOCODER_USER_AGENT = os.getenv(
        'GEOCODER_USER_AGENT',
        'BusShadeFinder/1.0',
    )
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')

