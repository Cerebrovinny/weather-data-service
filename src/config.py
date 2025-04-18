import os

class Config:
    OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY", "")
    GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "")
    LOCAL_DATA_PATH = os.environ.get("LOCAL_DATA_PATH", "data/weather_data.json")
    ENV = os.environ.get("ENV", "dev")  # 'dev' or 'prod'
