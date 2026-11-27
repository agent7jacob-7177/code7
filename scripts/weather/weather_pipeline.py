# weather_pipeline.py
"""City name -> coordinates -> 3-day forecast.

Uses known coordinates for names the Open-Meteo geocoder can't resolve
(e.g. "Hamilton, NJ", a township), otherwise geocodes via get_coordinates.py.

Usage: python3 weather_pipeline.py ["City Name"]
"""
import sys

from get_coordinates import get_coordinates_by_city
from weather_checker import display_forecast, get_weather_forecast

# Hamilton Township, Mercer County, NJ
KNOWN_COORDS = {
    "Hamilton, NJ": (40.21, -74.68),
}
DEFAULT_CITY = "Hamilton, NJ"
FORECAST_DAYS = 3


def resolve_coordinates(city_name):
    if city_name in KNOWN_COORDS:
        lat, lon = KNOWN_COORDS[city_name]
        print(f"📍 Using known coordinates for '{city_name}': Lat={lat}, Lon={lon}")
        return lat, lon
    return get_coordinates_by_city(city_name)


if __name__ == "__main__":
    city = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CITY
    lat, lon = resolve_coordinates(city)
    if lat is None or lon is None:
        sys.exit(1)

    weather_data = get_weather_forecast(lat, lon, FORECAST_DAYS)
    if weather_data:
        display_forecast(weather_data)
