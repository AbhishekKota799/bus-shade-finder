# 🚌 Bus Shade Finder

> Find the best side of a bus to sit on by analyzing the route, travel direction, and the sun's position during the journey.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![Leaflet](https://img.shields.io/badge/Leaflet-Interactive%20Maps-green?logo=leaflet)
![OpenStreetMap](https://img.shields.io/badge/OpenStreetMap-Data-brightgreen?logo=openstreetmap)
![GitHub](https://img.shields.io/badge/GitHub-Open%20Source-black?logo=github)

---

## 🌞 Overview

**Bus Shade Finder** is a Flask-based web application that predicts which side of a bus (left or right) is likely to stay in the shade for most of a journey.

It combines route analysis, solar position calculations, and travel direction to provide a recommendation that can make long bus journeys more comfortable.

---

## ❓ Problem Statement

Passengers often choose a window seat without knowing which side of the bus will receive direct sunlight.

For long trips, especially in hot weather, sitting on the sunny side can make the journey uncomfortable.

There is no simple tool that helps passengers decide which side of the bus will remain shaded during travel.

---

## 💡 Solution

This application analyzes:

- 📍 Source and destination
- 🛣️ Bus route
- ☀️ Sun position
- 🧭 Travel direction

Using this information, it estimates sunlight exposure on both sides of the bus and recommends the better side.

---

## ✨ Features

### ✅ Completed

- Geocoding locations
- Route retrieval using OSRM
- Interactive Leaflet map
- Solar position calculation
- Route heading calculation
- Relative sun direction
- Side exposure analysis

### 🚧 In Progress

- Recommendation Engine
- Journey Analyzer

### 🔮 Planned

- Journey timeline
- Confidence score
- Weather-aware recommendations
- Seat layout visualization
- Mobile optimization

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Maps | Leaflet.js |
| Routing | OSRM |
| Map Data | OpenStreetMap |
| Version Control | Git & GitHub |

---

## 🏗️ System Architecture

```text
User Input
     │
     ▼
Geocoder
     │
     ▼
Route Retrieval
     │
     ▼
Heading Calculation
     │
     ▼
Solar Position
     │
     ▼
Relative Sun Analysis
     │
     ▼
Side Exposure Calculation
     │
     ▼
Recommendation Engine
     │
     ▼
Result
```

---

## 📂 Project Structure

```text
BusShadeFinder/
│
├── services/
│   ├── geocoder.py
│   ├── routing.py
│   ├── heading.py
│   ├── solar.py
│   ├── relative_sun.py
│   ├── shade.py
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/AbhishekKota799/bus-shade-finder.git
```

Go to the project directory:

```bash
cd bus-shade-finder
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## ⚙️ How It Works

1. Enter the source and destination.
2. Retrieve the driving route.
3. Calculate the heading of each route segment.
4. Compute the sun's position for the selected travel time.
5. Compare the bus heading with the sun direction.
6. Estimate sunlight exposure on the left and right sides.
7. Recommend the more comfortable side of the bus.

---

## 📈 Project Status

| Module | Status |
|--------|--------|
| Flask Setup | ✅ Complete |
| UI | ✅ Complete |
| Geocoder | ✅ Complete |
| Route Retrieval | ✅ Complete |
| Interactive Map | ✅ Complete |
| Solar Service | ✅ Complete |
| Heading Service | ✅ Complete |
| Relative Sun Analysis | ✅ Complete |
| Shade Analysis | ✅ Complete |
| Recommendation Engine | 🚧 In Progress |
| Journey Analyzer | 🚧 Planned |
| Deployment | 🚧 Planned |

---

## 🗺️ Roadmap

- [ ] Recommendation Engine
- [ ] Journey Analyzer
- [ ] Confidence Score
- [ ] Journey Timeline
- [ ] Weather Integration
- [ ] Seat Layout Visualization
- [ ] Deployment

---

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome. Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Abhishek Kota**

GitHub: https://github.com/AbhishekKota799


