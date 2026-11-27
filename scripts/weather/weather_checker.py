# weather_checker.py
"""Daily weather forecast from the Open-Meteo API (no API key required)."""
import requests

# --- CONFIGURATION ---
# Default location: London, UK
LAT = 51.52
LON = -0.12
FORECAST_DAYS = 3
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
# --- END CONFIGURATION ---


def get_weather_forecast(lat, lon, days):
    """Fetch daily forecast data for the given coordinates. Returns parsed JSON or None."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "forecast_days": days,
        "timezone": "auto",
    }

    print(f"📡 Fetching weather data for Lat: {lat}, Lon: {lon}...")

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching weather data: {e}")
        return None


def display_forecast(data):
    """Print the daily forecast in a readable table."""
    if not data or "daily" not in data:
        print("\nCould not retrieve valid forecast data to display.")
        return

    daily = data["daily"]
    print("\n=============================================")
    print("🌍 ☁️ WEATHER FORECAST ☁️ 🌍")
    print("=============================================")
    print(f"Location: Lat {data['latitude']}, Lon {data['longitude']}")
    print("-" * 56)
    print("Date       | Max Temp (°C) | Min Temp (°C) | Rain Prob (%)")
    print("-----------|---------------|---------------|--------------")

    for i, date in enumerate(daily["time"]):
        max_temp = daily["temperature_2m_max"][i]
        min_temp = daily["temperature_2m_min"][i]
        rain_prob = daily["precipitation_probability_max"][i]
        rain = "n/a" if rain_prob is None else str(int(rain_prob))
        print(f"{date} | {max_temp:13.1f} | {min_temp:13.1f} | {rain:>12}")

    print("=============================================")
    print("Weather check complete.")


if __name__ == "__main__":
    weather_data = get_weather_forecast(LAT, LON, FORECAST_DAYS)
    if weather_data:
        display_forecast(weather_data)
