import pandas as pd

def transform_current_data(data):
    df = pd.DataFrame(data)
    df = df[['id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume']]
    df.rename(columns={
        'id': 'coin_id',
        'current_price': 'price',
        'total_volume': 'volume'
    }, inplace=True)
    df['retrieved_at'] = pd.Timestamp.utcnow()
    return df

def transform_historical_data(data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df