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

import requests

try:
    from src.config import Config
    from src.gateways.weather_stats_gateway import WeatherStatsGateway
except ImportError as e:
    print(f"Error importing src modules: {e}")
    # Define Config class with environment variables
    class Config:
        API_URL = os.environ.get("API_URL", "")
        API_KEY = os.environ.get("API_KEY", "")
        GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "")
    
    # Define WeatherStatsGateway for storing temperature data
    class WeatherStatsGateway:
        def get_city_temperatures(self, city):
            return []
        
        def save_city_temperatures(self, city, temps):
            pass

# Define WeatherAPIGateway that calls the Cloud Run API
class WeatherAPIGateway:
    def __init__(self):
        self.api_url = os.environ.get("API_URL", "")
        self.api_key = os.environ.get("API_KEY", "")
        if not self.api_url:
            print("Warning: API_URL not configured. Using fallback URL.")
            self.api_url = "http://localhost:8000"  # Fallback for local testing
        else:
            # Normalize the URL to prevent issues with duplicate protocol prefixes
            self.api_url = self._normalize_url(self.api_url)
        
        print(f"Using API URL: {self.api_url}")
    
    def _normalize_url(self, url):
        """Normalize URL to prevent issues with duplicate protocol prefixes."""
        import re
        
        # Remove any trailing slashes
        url = url.rstrip('/')
        
        # Fix URLs with duplicate protocol prefixes using regex
        # This matches patterns like http://http://, https://https://, http://https://, etc.
        pattern = r'^(https?://)(?:https?://)(.+)$'
        match = re.match(pattern, url)
        
        if match:
            protocol, rest = match.groups()
            return f"{protocol}{rest}"
            
        return url
    
    def get_current_weather(self, city):
        if not self.api_key:
            raise RuntimeError("API key not configured for Weather API service.")
        
        url = f"{self.api_url}/weather/current/{city}"
        headers = {"X-API-Key": self.api_key}
        
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            
            if resp.status_code == 404:
                raise ValueError(f"City not found: {city}")
            if resp.status_code == 401:
                raise RuntimeError("Authentication failed: Invalid API key")
            if resp.status_code != 200:
                raise RuntimeError(f"API error: {resp.status_code} - {resp.text}")
            
            data = resp.json()
            return {"city": city, "temperature": data.get("temperature", 0.0)}
        except requests.exceptions.RequestException as e:
            print(f"Error calling API: {e}")
            raise RuntimeError(f"Failed to fetch weather data: {str(e)}")

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
