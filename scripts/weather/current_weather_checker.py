# current_weather_checker.py
import requests
import json
import sys

# --- CONFIGURATION ---
# Open-Meteo API for current weather data.
CURRENT_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Fallback coordinates for key cities (since Geocoding API is unstable)
# These are hardcoded to make the script runnable and demonstrate the full pipeline flow.
FALLBACK_COORDS = {
    "New York City, New York": {"lat": 40.71, "lon": -74.00},
    "Hamilton, NJ": {"lat": 43.25, "lon": -79.84},
    "Lynnwood, WA": {"lat": 47.74, "lon": -122.15}
}
# --- END CONFIGURATION ---

def get_current_weather(lat, lon, location_name):
    """
    Fetches and prints current weather data from the Open-Meteo API.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        # Requesting only current conditions data points
        "current": "weathercode,temperature_2m,relativehumidity_2m,apparent_temperature_2m",
        "timezone": "auto"
    }
    
    print(f"\n>>> TESTING {location_name} ({lat:.2f}, {lon:.2f}) <<<")
    
    try:
        response = requests.get(CURRENT_WEATHER_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'current' in data:
            current = data['current']
            print("\n✅ SUCCESS: Current Weather Data Received!")
            print("==========================================")
            print(f"Location: {location_name}")
            print(f"Temperature: {current['temperature_2m']} °C")
            print(f"Feels Like:   {current['apparent_temperature_2m']} °C")
            print(f"Humidity:     {current['relativehumidity_2m']}%")
            print("==========================================")
        else:
            print("\n❌ FAILURE: 'current' data key missing in the API response.")
            
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ FAILURE: API HTTP Error ({e.response.status_code}). Could not retrieve data for {location_name}. Check coordinates.")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ FAILURE: Connection Error for {location_name}: {e}")

if __name__ == "__main__":
    print("--- Starting Weather Check Pipeline (Current Conditions Mode) ---")
    
    # Test all defined locations sequentially
    for location, coords in FALLBACK_COORDS.items():
        get_current_weather(coords['lat'], coords['lon'], location)

print("\n--- ALL WEATHER CHECKS COMPLETE ---")