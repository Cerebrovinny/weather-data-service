import pytest
import json
import os
from src.gateways.weather_stats_gateway import WeatherStatsGateway
from src.config import Config

class DummyConfig:
    ENV = "dev"
    LOCAL_DATA_PATH = "test_weather_data.json"

@pytest.fixture
def temp_json(monkeypatch):
    data = {"London": [10.0, 15.0, 20.0], "Paris": [12.0, 14.0]}
    with open("test_weather_data.json", "w") as f:
        json.dump(data, f)
    monkeypatch.setattr("src.config.Config.LOCAL_DATA_PATH", "test_weather_data.json")
    yield
    os.remove("test_weather_data.json")

def test_get_city_temperatures_dev(temp_json):
    gw = WeatherStatsGateway()
    temps = gw.get_city_temperatures("London")
    assert temps == [10.0, 15.0, 20.0]
    temps2 = gw.get_city_temperatures("Paris")
    assert temps2 == [12.0, 14.0]
    temps3 = gw.get_city_temperatures("Berlin")
    assert temps3 == []

def test_get_city_temperatures_missing_file(monkeypatch):
    monkeypatch.setattr("src.config.Config.LOCAL_DATA_PATH", "notfound.json")
    gw = WeatherStatsGateway()
    temps = gw.get_city_temperatures("London")
    assert temps == []
