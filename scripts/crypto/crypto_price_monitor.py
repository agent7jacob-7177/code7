# crypto_price_monitor.py
"""Poll a Coinbase Exchange product ticker (public endpoint, no API key needed).

Usage: python3 crypto_price_monitor.py [PRODUCT_ID] [ITERATIONS] [DELAY_SECONDS]
       e.g. python3 crypto_price_monitor.py ETH-USD 5 10

Note: Coinbase lists crypto pairs only; stocks such as AMD are not available.
"""
import sys
import time

import requests

DEFAULT_PRODUCT_ID = "BTC-USD"
# api.pro.coinbase.com was retired; Coinbase Exchange is its replacement.
TICKER_URL = "https://api.exchange.coinbase.com/products/{product_id}/ticker"


def fetch_ticker(product_id):
    """Return the ticker dict (price, bid, ask, volume, time) or None on failure."""
    url = TICKER_URL.format(product_id=product_id)
    try:
        response = requests.get(url, headers={"User-Agent": "code7-price-monitor"}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error: {e}. Is '{product_id}' a valid Coinbase product?")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    return None


def monitor_price(product_id=DEFAULT_PRODUCT_ID, iterations=3, delay_seconds=5):
    print(f"Monitoring {product_id}: {iterations} checks, {delay_seconds}s apart (REST snapshots).")
    previous_price = None

    for i in range(1, iterations + 1):
        print(f"\n===== Check {i}/{iterations} =====")
        ticker = fetch_ticker(product_id)

        if ticker and "price" in ticker:
            price = float(ticker["price"])
            print(f"Last price: {price:,.2f}")
            print(f"Bid / Ask:  {ticker.get('bid', 'n/a')} / {ticker.get('ask', 'n/a')}")
            print(f"As of:      {ticker.get('time', 'n/a')}")

            if previous_price is not None:
                delta = price - previous_price
                if delta:
                    print(f"🚨 Price changed by {delta:+,.2f} ({delta / previous_price:+.4%})")
                else:
                    print("✨ Price unchanged since last check.")
            previous_price = price
        else:
            print("❌ No ticker data received.")

        if i < iterations:
            time.sleep(delay_seconds)


if __name__ == "__main__":
    args = sys.argv[1:]
    product = args[0] if len(args) > 0 else DEFAULT_PRODUCT_ID
    runs = int(args[1]) if len(args) > 1 else 3
    delay = int(args[2]) if len(args) > 2 else 5
    monitor_price(product, runs, delay)
