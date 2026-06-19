# weather_checker.py
import requests
import json

# --- CONFIGURATION ---
# 1. Define the desired location by coordinates (Latitude and Longitude).
#    Example: London, UK (Latitude: 51.52, Longitude: -0.12)
LAT = 51.52
LON = -0.12
# 2. Define the time frame for the forecast (e.g., 3 days).
FORECAST_DAYS = 3
# --- END CONFIGURATION ---

def get_weather_forecast(lat, lon, days):
    """
    Fetches weather forecast data from the Open-Meteo API based on coordinates.
    """
    # Open-Meteo forecast URL structure
    url = "https://api.open-meteo.com/v1/forecast"
    
    # Parameters for the forecast: daily weather, temperature, and wind speed
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability",
        "daily_forecast_days": days
    }
    
    print(f"📡 Fetching weather data for Lat: {lat}, Lon: {lon}...")
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise exception for bad status codes (4xx or 5xx)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching weather data: {e}")
        print("   Please check if the coordinates are valid or if the service is temporarily unavailable.")
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
    
    # Optional: Print a summary
    print("\n=============================================")
    print("Weather check complete.")


if __name__ == "__main__":
    # 1. Get Data
    weather_data = get_weather_forecast(LAT, LON, FORECAST_DAYS)
    
    # 2. Display Result
    if weather_data:
        display_forecast(weather_data)

# Note: This script requires the 'requests' library: pip install requests
