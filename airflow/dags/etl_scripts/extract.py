import requests
from datetime import datetime
import time  # Import the time module

def fetch_current_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "eur",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def fetch_historical_data(days=30):
    historical_data = []
    
    coins_list_url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(coins_list_url)
    response.raise_for_status()
    coins = response.json()[:100]  # Limiting to the first 100 coins

    for coin in coins:
        coin_id = coin['id']
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {
            "vs_currency": "eur",
            "days": days,
            "interval": "daily"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        for i, price in enumerate(data['prices']):
            historical_data.append({
                "coin_id": coin_id,
                "date": datetime.utcfromtimestamp(price[0] / 1000).strftime('%Y-%m-%d'),
                "price": price[1],
                "market_cap": data['market_caps'][i][1],
                "volume": data['total_volumes'][i][1]
            })
        print("waiting for 30 seconds...")
        time.sleep(30)  
    
    return historical_data
