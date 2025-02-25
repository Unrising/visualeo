from etl_scripts.extract import fetch_current_data, fetch_historical_data
from etl_scripts.transform import transform_current_data, transform_historical_data
from etl_scripts.load import load_data

def run_etl(etl_type):
    if etl_type == "current":
        print("Running ETL for current cryptocurrency data...")
        data = fetch_current_data()
        if data:
            df = transform_current_data(data)
            load_data(df, 'crypto_current')

    elif etl_type == "historical":
        print("Running ETL for historical cryptocurrency data...")
        data = fetch_historical_data(days=30)
        if data:
            df = transform_historical_data(data)
            load_data(df, 'crypto_historical')

    else:
        print("Invalid ETL type. Use 'current' or 'historical'.")
        raise ValueError("Invalid ETL type")