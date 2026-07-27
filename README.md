# Bus Shade Finder

Bus Shade Finder is a Flask website that will recommend whether a passenger should sit on the left or right side of a bus to stay in the shade during a journey.

## Project setup

Clone or open this project folder, then create a local Python environment before installing dependencies.

## Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Create the .env file

Create a file named `.env` in the project root with:

```env
FLASK_ENV=development
SECRET_KEY=change_me
GEOCODER_BASE_URL=https://nominatim.openstreetmap.org/search
OSRM_BASE_URL=https://router.project-osrm.org
REQUEST_TIMEOUT_SECONDS=10
GEOCODER_USER_AGENT=BusShadeFinder/1.0
```

## Run the Flask app

```bash
python app.py
```

Open the local Flask URL shown in the terminal.
