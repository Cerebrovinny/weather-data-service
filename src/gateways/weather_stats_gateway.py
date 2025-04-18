import json
import os
from src.config import Config

from src.gateways.local_weather_stats_storage import LocalWeatherStatsStorage
from src.gateways.gcs_weather_stats_storage import GCSWeatherStatsStorage

class WeatherStatsGateway:
    def __init__(self):
        if Config.ENV == "prod":
            self._impl = GCSWeatherStatsStorage()
        else:
            self._impl = LocalWeatherStatsStorage()

    def get_city_temperatures(self, city):
        return self._impl.get_city_temperatures(city)

    def save_city_temperatures(self, city, temperatures):
        return self._impl.save_city_temperatures(city, temperatures)
