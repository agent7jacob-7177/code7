# current_weather_checker.py
"""Current conditions for a few fixed locations via the Open-Meteo API."""
import requests

# --- CONFIGURATION ---
CURRENT_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

LOCATIONS = {
    "New York City, NY": {"lat": 40.71, "lon": -74.00},
    "Hamilton, NJ": {"lat": 40.21, "lon": -74.68},
    "Lynnwood, WA": {"lat": 47.82, "lon": -122.32},
}
# --- END CONFIGURATION ---


def get_current_weather(lat, lon, location_name):
    """Fetch and print current conditions for one location."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "weathercode,temperature_2m,relativehumidity_2m,apparent_temperature",
        "timezone": "auto",
    }

    print(f"\n>>> {location_name} ({lat:.2f}, {lon:.2f}) <<<")

    try:
        response = requests.get(CURRENT_WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as e:
        detail = e.response.text[:200] if e.response is not None else str(e)
        print(f"❌ API HTTP error for {location_name}: {detail}")
        return
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error for {location_name}: {e}")
        return

    current = data.get("current")
    if not current:
        print("❌ 'current' key missing in the API response.")
        return

    print(f"Temperature: {current['temperature_2m']} °C")
    print(f"Feels like:  {current['apparent_temperature']} °C")
    print(f"Humidity:    {current['relativehumidity_2m']}%")


if __name__ == "__main__":
    print("--- Current Weather Check ---")
    for location, coords in LOCATIONS.items():
        get_current_weather(coords["lat"], coords["lon"], location)
    print("\n--- ALL WEATHER CHECKS COMPLETE ---")
