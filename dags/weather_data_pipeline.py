from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import sys
import importlib.util

# Add the src module to the Python path
def setup_python_path():
    # Check if we're running in Airflow
    airflow_home = os.environ.get('AIRFLOW_HOME', '')
    
    plugins_dir = os.path.join(airflow_home, 'plugins') if airflow_home else '/home/airflow/gcs/plugins'
    src_in_plugins = os.path.join(plugins_dir, 'src')
    
    dags_dir = os.path.dirname(os.path.abspath(__file__))
    src_in_dags = os.path.join(os.path.dirname(dags_dir), 'src')
    
    potential_paths = [src_in_plugins, src_in_dags]
    for path in potential_paths:
        if os.path.exists(path) and path not in sys.path:
            sys.path.insert(0, os.path.dirname(path))
            print(f"Added {os.path.dirname(path)} to Python path")
            return True
    
    print("Warning: Could not find src module in expected locations")
    return False

# Setup the Python path
setup_python_path()

# Import your gateways and config
try:
    from src.config import Config
    from src.gateways.weather_api_gateway import WeatherAPIGateway
    from src.gateways.weather_stats_gateway import WeatherStatsGateway
except ImportError as e:
    print(f"Error importing src modules: {e}")
    # Provide mock implementations for testing
    class Config:
        pass
    
    class WeatherAPIGateway:
        def get_current_weather(self, city):
            return {"temperature": 20.0}
    
    class WeatherStatsGateway:
        def get_city_temperatures(self, city):
            return []
        
        def save_city_temperatures(self, city, temps):
            pass

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
    # Create a valid task_id by replacing spaces with underscores and removing any other invalid characters
    safe_city_name = city.lower().replace(' ', '_').replace('-', '_')
    # Remove any other characters that aren't alphanumeric, underscore, dot, or dash
    safe_city_name = ''.join(c for c in safe_city_name if c.isalnum() or c in '_.-')
    
    return PythonOperator(
        task_id=f"fetch_and_store_{safe_city_name}",
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
