import requests
import time
from datetime import datetime, timedelta

def fetch_current_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "eur",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": False
    }

    for attempt in range(5):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching current data: {e}. Retrying in {2 ** attempt} seconds...")
            time.sleep(2 ** attempt)  

    return None 

def fetch_historical_data(days=30):
    historical_data = []

    coins_list_url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        coins_response = requests.get(coins_list_url)
        coins_response.raise_for_status()
        coins = coins_response.json()[:100]  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coins list: {e}")
        return None

    for coin in coins:
        coin_id = coin['id']
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {
            "vs_currency": "eur",
            "days": days,
            "interval": "daily"
        }

        for attempt in range(5):
            try:
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
                
                break  

            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for {coin_id}: {e}. Retrying in {2 ** attempt} seconds...")
                time.sleep(2 ** attempt) 

        time.sleep(1.5)

    return historical_data
