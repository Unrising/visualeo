from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../etl'))

from extract import fetch_current_data, fetch_historical_data
from transform import transform_current_data, transform_historical_data
from load import load_data
import pandas as pd

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


with DAG(
    dag_id='crypto_etl_dag',
    default_args=default_args,
    description='Extract, Transform, and Load cryptocurrency data',
    schedule_interval='@daily',  
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    def extract_current():
        """Extract current cryptocurrency data."""
        data = fetch_current_data()
        if data:
            df = transform_current_data(data)
            df.to_csv('/tmp/current_crypto.csv', index=False)  

    def extract_historical():
        """Extract historical cryptocurrency data."""
        historical_data = fetch_historical_data(days=30)  

        if historical_data:
            df = transform_historical_data(historical_data)
            df.to_csv('/tmp/historical_crypto.csv', index=False)  

    def load_current():
        """Load current cryptocurrency data into PostgreSQL."""
        df = pd.read_csv('/tmp/current_crypto.csv')
        load_data(df, 'crypto_current')

    def load_historical():
        """Load historical cryptocurrency data into PostgreSQL."""
        df = pd.read_csv('/tmp/historical_crypto.csv')
        load_data(df, 'crypto_historical')

    extract_current_task = PythonOperator(
        task_id='extract_current_data',
        python_callable=extract_current
    )

    extract_historical_task = PythonOperator(
        task_id='extract_historical_data',
        python_callable=extract_historical
    )

    load_current_task = PythonOperator(
        task_id='load_current_data',
        python_callable=load_current
    )

    load_historical_task = PythonOperator(
        task_id='load_historical_data',
        python_callable=load_historical
    )

    extract_current_task >> load_current_task
    extract_historical_task >> load_historical_task
