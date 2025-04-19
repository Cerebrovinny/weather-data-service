import json, os, tempfile
from typing import List
from src.config import Config
from src.gateways.weather_stats_storage_gateway import WeatherStatsStorageGateway

class LocalWeatherStatsStorage(WeatherStatsStorageGateway):
    def get_city_temperatures(self, city: str) -> List[float]:
        """Retrieve temperature data from a city-specific file."""        
        data_dir = os.path.dirname(Config.LOCAL_DATA_PATH)
        city_file = os.path.join(data_dir, f"{city}.json")
        
        if not os.path.exists(city_file):
            if os.path.exists(Config.LOCAL_DATA_PATH):
                try:
                    with open(Config.LOCAL_DATA_PATH) as f:
                        all_data = json.load(f)
                        data = all_data.get(city, [])
                        return data if isinstance(data, list) else []
                except (json.JSONDecodeError, FileNotFoundError):
                    return []
            return []
            
        try:
            with open(city_file) as f:
                temperatures = json.load(f)
                return temperatures if isinstance(temperatures, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_city_temperatures(self, city: str, temperatures: List[float]) -> None:
        """Save temperature data to a city-specific file, eliminating concurrency issues."""        
        data_dir = os.path.dirname(Config.LOCAL_DATA_PATH)
        os.makedirs(data_dir, exist_ok=True)
        
        city_file = os.path.join(data_dir, f"{city}.json")
        
        with tempfile.NamedTemporaryFile('w', dir=data_dir, delete=False) as tf:
            json.dump(temperatures, tf)
            tempname = tf.name
        os.replace(tempname, city_file)

