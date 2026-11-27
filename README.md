# Code 7

Jacob's coding workspace: utility scripts, prototypes, and the GitHub Pages
landing page. (Research and documentation live in the separate
`agent-notes` repo.)

Live site: https://agent7jacob-7177.github.io/code7 (served from the `gh-pages` branch)

## Layout

```
code7/
├── scripts/
│   ├── weather/                    # Open-Meteo (no API key)
│   │   ├── weather_checker.py      # 3-day forecast for fixed coords
│   │   ├── current_weather_checker.py  # current conditions, several cities
│   │   ├── get_coordinates.py      # city name -> lat/lon (geocoding)
│   │   └── weather_pipeline.py     # city -> coords -> forecast
│   ├── crypto/
│   │   └── crypto_price_monitor.py # Coinbase Exchange ticker poller
│   └── soccer/                     # World Cup 2026 reminder prototype
│       ├── soccer_monitor.py       # STUB: simulated schedule + alert
│       └── check_reminder.py       # single reminder check using the above
├── requirements.txt
└── README.md
```

## Setup

```
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```
python3 scripts/weather/weather_checker.py
python3 scripts/weather/current_weather_checker.py
python3 scripts/weather/get_coordinates.py London
python3 scripts/weather/weather_pipeline.py "Hamilton, NJ"
python3 scripts/crypto/crypto_price_monitor.py BTC-USD 3 5
python3 scripts/soccer/check_reminder.py
```

Note: the soccer scripts are a prototype — the schedule is hard-coded
sample data and the Telegram alert only prints (no real API calls).
