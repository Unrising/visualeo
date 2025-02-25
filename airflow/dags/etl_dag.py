from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from etl_scripts.run_etl import run_etl

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 2, 25),
    'retries': 1,
}

dag = DAG(
    'crypto_etl',
    default_args=default_args,
    description='A simple crypto ETL DAG',
    schedule_interval='@daily',
)

run_current_etl = PythonOperator(
    task_id='run_current_etl',
    python_callable=run_etl,
    op_args=['current'],
    dag=dag,
)

run_historical_etl = PythonOperator(
    task_id='run_historical_etl',
    python_callable=run_etl,
    op_args=['historical'],
    dag=dag,
)

run_current_etl >> run_historical_etl
