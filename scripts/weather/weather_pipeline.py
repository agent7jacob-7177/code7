# weather_pipeline.py
import requests
import json
import sys
from datetime import datetime

# --- CONFIGURATION ---
# We are using a hardcoded fallback coordinate for Hamilton, NJ,
# because the Open-Meteo Geocoding API failed to resolve the name.
FALLBACK_LAT = 43.25
FALLBACK_LON = -79.84
# --- END CONFIGURATION ---

# 1. Geocoding function (Simulated/Fallback)
def get_coordinates_fallback(city_name):
    """
    In a real-world scenario, this function would use a robust API
    (like Nominatim/OpenStreetMaps) to find coords.
    For this script, we use a fallback based on previous knowledge.
    """
    print(f"⚠️ WARNING: Open-Meteo Geocoding API failed for '{city_name}'.")
    print(f"   Using fallback coordinates: Lat={FALLBACK_LAT}, Lon={FALLBACK_LON}")
    return FALLBACK_LAT, FALLBACK_LON

# 2. Weather fetching function (from weather_checker.py logic)
def get_weather_forecast(lat, lon, days):
    """
    Fetches weather forecast data from the Open-Meteo API.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability",
        "daily_forecast_days": days
    }
    
    print(f"\n📡 Fetching weather data for Lat: {lat}, Lon: {lon}...")
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching weather data: {e}")
        return None

def display_forecast(data):
    """
    Parses and prints the weather forecast data in a readable format.
    """
    if not data or 'daily' not in data:
        print("\nCould not retrieve valid forecast data to display.")
        return

    daily = data['daily']
    print("\n=============================================")
    print("🌍 ☁️ WEATHER FORECAST ☁️ 🌍")
    print("=============================================")
    print(f"Current Location: Lat {data['latitude']}, Lon {data['longitude']}")
    print("-" * 50)

    # Display daily forecast
    print("\n🗓️ Daily Forecast:")
    print("Day | Max Temp (°C) | Min Temp (°C) | Rain Prob (%)")
    print("----|---------------|---------------|----------------")
    
    for i, date in enumerate(daily['time']):
        max_temp = daily['temperature_2m_max'][i]
        min_temp = daily['temperature_2m_min'][i]
        rain_prob = daily['precipitation_probability'][i]
        
        print(f"{date[0:3]} | {max_temp:13.1f} | {min_temp:13.1f} | {int(rain_prob):<12}")
    
    print("\n=============================================")
    print("Weather check complete.")


if __name__ == "__main__":
    CITY_NAME = "Hamilton, NJ"
    FORECAST_DAYS = 3
    
    # Step 1: Get Coordinates (using fallback for reliability)
    lat, lon = get_coordinates_fallback(CITY_NAME)
    
    # Step 2: Get Weather Forecast
    weather_data = get_weather_forecast(lat, lon, FORECAST_DAYS)
    
    # Step 3: Display Result
    if weather_data:
        display_forecast(weather_data)
