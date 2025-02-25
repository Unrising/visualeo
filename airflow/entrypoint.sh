#!/bin/bash

echo "Waiting for PostgreSQL to start..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL started."

echo "Initializing Airflow Database..."
airflow db init
airflow db upgrade

echo "Creating Admin User..."
airflow users create \
    --username ${_AIRFLOW_WWW_USER_USERNAME:-admin} \
    --password ${_AIRFLOW_WWW_USER_PASSWORD:-admin} \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com || echo "User already exists."

echo "Starting Airflow services..."
airflow scheduler & airflow webserver
