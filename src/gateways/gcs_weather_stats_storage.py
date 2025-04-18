import json
from typing import List
from src.config import Config
from src.gateways.weather_stats_storage_gateway import WeatherStatsStorageGateway

class GCSWeatherStatsStorage(WeatherStatsStorageGateway):
    def get_city_temperatures(self, city: str) -> List[float]:
        from google.cloud import storage
        client = storage.Client()
        bucket = client.bucket(Config.GCS_BUCKET_NAME)
        blob = bucket.blob(f"{city}.json")
        if not blob.exists():
            return []
        data = json.loads(blob.download_as_text())
        return data if isinstance(data, list) else []

    def save_city_temperatures(self, city: str, temperatures: List[float]) -> None:
        from google.cloud import storage
        client = storage.Client()
        bucket = client.bucket(Config.GCS_BUCKET_NAME)
        blob = bucket.blob(f"{city}.json")
        blob.upload_from_string(json.dumps(temperatures), content_type="application/json")
