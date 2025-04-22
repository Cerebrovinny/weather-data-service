import os

class Config:
    OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY", "")
    GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "")
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")  # Optional, for GCP auth
    LOCAL_DATA_PATH = os.environ.get("LOCAL_DATA_PATH", "data/weather_data.json")
    ENV = os.environ.get("ENV", "dev")  # 'dev' or 'prod'
    API_KEY = os.environ.get("API_KEY", "changeme")  # Required for HTTP header auth
    API_RATE_LIMIT = os.environ.get("API_RATE_LIMIT", "100/minute") # Rate limit for API requests
