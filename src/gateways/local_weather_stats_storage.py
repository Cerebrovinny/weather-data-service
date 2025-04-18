import json
import os
from typing import List
from src.config import Config
from src.gateways.weather_stats_storage_gateway import WeatherStatsStorageGateway

class LocalWeatherStatsStorage(WeatherStatsStorageGateway):
    def get_city_temperatures(self, city: str) -> List[float]:
        path = Config.LOCAL_DATA_PATH
        if not os.path.exists(path):
            return []
        with open(path) as f:
            all_data = json.load(f)
        data = all_data.get(city, [])
        return data if isinstance(data, list) else []

    def save_city_temperatures(self, city: str, temperatures: List[float]) -> None:
        path = Config.LOCAL_DATA_PATH
        if os.path.exists(path):
            with open(path) as f:
                all_data = json.load(f)
        else:
            all_data = {}
        all_data[city] = temperatures
        with open(path, "w") as f:
            json.dump(all_data, f)
