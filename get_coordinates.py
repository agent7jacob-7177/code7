# get_coordinates.py
import requests
import json
import sys

# --- CONFIGURATION ---
# For this script, we will use the Open-Meteo Geocoding API endpoint.
# The API requires latitude and longitude.
# Open-Meteo documentation indicates a geocoding service is available.

OPEN_METEO_GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
# --- END CONFIGURATION ---

def get_coordinates_by_city(city_name):
    """
    Fetches Latitude and Longitude for a given city name using a public Geocoding API.
    
    Args:
        city_name (str): The name of the city (e.g., "Tokyo").
    
    Returns:
        tuple: (latitude, longitude) if successful, otherwise (None, None).
    """
    if not city_name:
        print("🛑 Error: Please provide a city name.")
        return None, None

    # Parameters for the API call
    params = {
        "name": city_name,
        "count": 1 # We only need the top result
    }
    
    print(f"📡 Searching for coordinates for '{city_name}'...")
    
    try:
        response = requests.get(OPEN_METEO_GEO_URL, params=params)
        response.raise_for_status() # Raises HTTPError for bad status codes (4xx or 5xx)
        data = response.json()
        
        if data.get("results") and len(data["results"]) > 0:
            first_result = data["results"][0]
            lat = first_result.get("latitude")
            lon = first_result.get("longitude")
            print(f"✅ Found coordinates successfully.")
            return lat, lon
        else:
            print(f"❌ Could not find coordinates for '{city_name}'. The API returned no results.")
            return None, None
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ An API error occurred: {e}")
        print("   Please check your internet connection or if the API endpoint is available.")
        return None, None

if __name__ == "__main__":
    # Check if a city name was passed as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python3 get_coordinates.py <City Name>")
        print("Example: python3 get_coordinates.py London")
        # Exit gracefully if no argument is provided
        sys.exit(1)

    # The first argument after the script name is the city name
    city_to_check = sys.argv[1]
    
    lat, lon = get_coordinates_by_city(city_to_check)
    
    if lat and lon:
        print("\n" + "="*50)
        print(f"🌎 Coordinates for {city_to_check.title()}:")
        print(f"   Latitude:  {lat}")
        print(f"   Longitude: {lon}")
        print("="*50)
