from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os

# Import your gateways and config
from src.config import Config
from src.gateways.weather_api_gateway import WeatherAPIGateway
from src.gateways.weather_stats_gateway import WeatherStatsGateway

def fetch_and_store_weather(city):
    gw = WeatherAPIGateway()
    stats_gw = WeatherStatsGateway()
    weather = gw.get_current_weather(city)
    temps = stats_gw.get_city_temperatures(city)
    temps.append(weather["temperature"])
    stats_gw.save_city_temperatures(city, temps)

# Configurable cities from env or default
CITIES = os.environ.get("CITIES", "London,Paris,Berlin").split(",")

def create_city_task(city, dag):
    return PythonOperator(
        task_id=f"fetch_and_store_{city.lower()}",
        python_callable=fetch_and_store_weather,
        op_args=[city],
        dag=dag,
    )

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

import re
from airflow.utils.dates import days_ago
from airflow.utils import timezone

# Allow schedule to be set via env (cron or timedelta string)
def parse_schedule(val):
    if not val:
        return timedelta(hours=1)
    val = val.strip()
    # If looks like cron (contains space or * or /)
    if re.match(r"[\d\s\*\/\-,]+", val) and (" " in val or "*" in val or "/" in val):
        return val  # Airflow will accept cron string
    # If looks like timedelta, e.g. 'hours=2'
    try:
        return eval(f"timedelta({val})", {'timedelta': timedelta})
    except Exception:
        return timedelta(hours=1)

SCHEDULE = os.environ.get("PIPELINE_SCHEDULE", None)


dag = DAG(
    'weather_data_pipeline',
    default_args=default_args,
    description='Fetch and store weather data for cities',
    schedule_interval=parse_schedule(SCHEDULE),
    catchup=False,
)

for city in CITIES:
    create_city_task(city, dag)
