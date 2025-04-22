from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import sys
import requests

try:
    from airflow.providers.google.cloud.hooks.secret_manager import GoogleCloudSecretManagerHook
    HAS_SECRET_MANAGER = True
except ImportError:
    print("GoogleCloudSecretManagerHook not available. Will use environment variables for API key.")
    HAS_SECRET_MANAGER = False

def setup_python_path():
    # Check if we're running in Docker
    is_docker = os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER', False)
    
    # Check if we're running in Airflow
    airflow_home = os.environ.get('AIRFLOW_HOME', '')

    # Different path strategies based on environment
    if is_docker:
        # In Docker, the src directory is mounted at /opt/airflow/src
        docker_src_path = '/opt/airflow/src'
        if os.path.exists(docker_src_path) and docker_src_path not in sys.path:
            sys.path.insert(0, os.path.dirname(docker_src_path))
            print(f"Docker environment: Added {os.path.dirname(docker_src_path)} to Python path")
            return True
    
    # Standard Airflow paths
    plugins_dir = os.path.join(airflow_home, 'plugins') if airflow_home else '/home/airflow/gcs/plugins'
    src_in_plugins = os.path.join(plugins_dir, 'src')

    dags_dir = os.path.dirname(os.path.abspath(__file__))
    src_in_dags = os.path.join(os.path.dirname(dags_dir), 'src')

    # Try all potential paths
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

try:
    from src.config import Config
    from src.gateways.weather_stats_gateway import WeatherStatsGateway
except ImportError as e:
    print(f"Error importing src modules: {e}")
    # Define Config class with environment variables
    class Config:
        API_URL = os.environ.get("API_URL", "")
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
        # Check if we're running in a Docker environment
        self.is_docker = os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER', False)
        
        # Get API URL from environment with Docker-aware defaults
        self.api_url = os.environ.get("API_URL", "")
        
        # Try to get API key - with multiple fallback options for local Docker
        try:
            # First try: Direct environment variable (simplest for local Docker)
            self.api_key = os.environ.get("API_KEY", "")
            if self.api_key:
                print("Using API key from environment variables")
            elif HAS_SECRET_MANAGER:
                # Second try: Secret Manager (for Cloud environments)
                try:
                    hook = GoogleCloudSecretManagerHook(gcp_conn_id="google_cloud_default")
                    # Fetch the secret from Secret Manager
                    secret_id = "weather-api-key"
                    secret_version = "latest"
                    response = hook.access_secret(secret_id=secret_id, secret_version=secret_version)
                    if not response or not response.payload or not response.payload.data:
                        raise ValueError(f"Secret '{secret_id}' version '{secret_version}' not found or payload is empty.")
                    
                    # Decode the payload data
                    self.api_key = response.payload.data.decode("UTF-8")
                    print(f"Successfully fetched API key from Secret Manager")
                except Exception as e:
                    print(f"Error fetching API key from Secret Manager: {e}")
                    if self.is_docker:
                        print("Running in Docker without API key - this may be fine for local testing")
                    else:
                        raise ValueError("No API key available from environment or Secret Manager")
            else:
                # Secret Manager not available
                print("Secret Manager not available. Running without API key.")
                if not self.is_docker:
                    print("WARNING: Running in production without API key. This is not recommended.")
        except Exception as e:
            print(f"Error setting up API key: {e}")
            if not self.is_docker:
                raise RuntimeError(f"Failed to setup API key: {e}")


        # Set appropriate API URL based on environment
        if not self.api_url:
            if self.is_docker:
                print("Docker environment detected. Using api service name for URL.")
                self.api_url = "http://api:8000"
            else:
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
        if not self.api_key and not self.is_docker:
            # In production, we must have an API key
            raise RuntimeError("API key not configured for Weather API service.")

        url = f"{self.api_url}/weather/current/{city}"
        headers = {"X-API-Key": self.api_key} if self.api_key else {}

        try:
            print(f"Requesting weather data from: {url}")
            resp = requests.get(url, headers=headers, timeout=10)

            if resp.status_code == 404:
                raise ValueError(f"City not found: {city}")
            if resp.status_code == 401:
                raise RuntimeError("Authentication failed: Invalid API key")
            if resp.status_code != 200:
                raise RuntimeError(f"API error: {resp.status_code} - {resp.text}")

            data = resp.json()
            print(f"Successfully retrieved weather data for {city}")
            return {"city": city, "temperature": data.get("temperature", 0.0)}
        except requests.exceptions.RequestException as e:
            print(f"Error calling API: {e}")
            # In Docker environment, provide more helpful error message for networking issues
            if self.is_docker and "Connection refused" in str(e):
                print("This may be a Docker networking issue. Ensure the API service is running and accessible.")
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
