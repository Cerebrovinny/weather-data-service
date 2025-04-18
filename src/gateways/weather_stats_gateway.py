import json
import os
from src.config import Config

class WeatherStatsGateway:
    def get_city_temperatures(self, city):
        if Config.ENV == "prod":
            from google.cloud import storage
            client = storage.Client()
            bucket = client.bucket(Config.GCS_BUCKET_NAME)
            blob = bucket.blob(f"{city}.json")
            if not blob.exists():
                return []
            data = json.loads(blob.download_as_text())
        else:
            path = Config.LOCAL_DATA_PATH
            if not os.path.exists(path):
                return []
            with open(path) as f:
                all_data = json.load(f)
            data = all_data.get(city, [])
        return data if isinstance(data, list) else []
