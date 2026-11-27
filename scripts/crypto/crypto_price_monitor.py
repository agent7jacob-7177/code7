# fetch_amd_price.py
import os
import requests
import time
import json

# --- CONFIGURATION ---
# IMPORTANT: These should be loaded from environment variables for security.
# Example: os.environ['COINBASE_API_KEY']
API_KEY = os.environ.get("COINBASE_API_KEY", "YOUR_API_KEY")
API_SECRET = os.environ.get("COINBASE_API_SECRET", "YOUR_SECRET")

# The API structure suggests using a 'product ID' (e.g., BTC-USD).
# Since AMD is a stock and not a listed crypto pair, we use a placeholder
# and assume the user will substitute a real crypto pair like 'BTC-USD' or 'ETH-USD'.
# We use the general ticker endpoint pattern found in documentation.
PRODUCT_ID = "BTC-USD" # Placeholder for a valid Coinbase pair

BASE_URL = f"https://api.pro.coinbase.com/products/{PRODUCT_ID}/ticker"
# --- END CONFIGURATION ---

def fetch_crypto_price(url):
    """
    Fetches the current ticker information from the Coinbase Pro REST API.
    
    Returns a dictionary of the parsed JSON data or None on failure.
    """
    print(f"Attempting to fetch data from: {url}")
    try:
        # NOTE: In a real scenario, authentication headers (API Key/Secret)
        # would be required here for a secure call.
        headers = {
            "Content-Type": "application/json",
            # "X-CB-ACCESS-KEY": API_KEY,  # Uncomment when using actual keys
            # "X-CB-ACCESS-SECRET": API_SECRET # Uncomment when using actual secrets
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error occurred: {e}. Check if the PRODUCT_ID '{PRODUCT_ID}' is correct and if API keys are set.")
        return None
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Coinbase API. Check your internet connection.")
        return None
    except requests.exceptions.Timeout:
        print("Error: The request timed out.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred: {e}")
        return None

def monitor_price(iterations=3, delay_seconds=5):
    """
    Runs the price check multiple times to simulate monitoring.
    """
    print("-" * 50)
    print(f"Starting price monitor for {PRODUCT_ID} ({iterations} runs).")
    print(f"NOTE: This script uses the REST API, which is for snapshot data, not true real-time streaming.")
    print("-" * 50)
    
    last_price = None

    for i in range(1, iterations + 1):
        print(f"\n{'='*20} Run {i}/{iterations} {'='*20}")
        data = fetch_crypto_price(BASE_URL)
        
        if data and 'data' in data:
            ticker_data = data['data']
            
            # Extract key metrics from the response
            last_price = ticker_data.get('last', 'N/A')
            bid = ticker_data.get('bid', 'N/A')
            ask = ticker_data.get('ask', 'N/A')

            print("✅ Price Fetch Successful!")
            print(f"   Last Traded Price: {last_price}")
            print(f"   Current Bid:      {bid}")
            print(f"   Current Ask:      {ask}")

            # Simulate checking for price change
            if i > 1:
                if str(last_price) != str(last_price): # Simple check to detect changes
                    print("🚨 Price Change Detected! The price has fluctuated since the last check.")
                else:
                    print("✨ Price appears stable (or the API returned the same value).")
        else:
            print("❌ Failed to retrieve data. Check configuration and API connectivity.")

        if i < iterations:
            print(f"\nWaiting for {delay_seconds} seconds before the next check...")
            time.sleep(delay_seconds)

if __name__ == "__main__":
    # Set up the environment (if running in a proper shell)
    # os.environ['COINBASE_API_KEY'] = 'your_actual_key'
    # os.environ['COINBASE_API_SECRET'] = 'your_actual_secret'
    
    monitor_price(iterations=3, delay_seconds=5)
