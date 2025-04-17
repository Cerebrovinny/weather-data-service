import pytest
from src.domain.weather_record import WeatherRecord
from datetime import datetime

def test_weather_record_creation():
    record = WeatherRecord(city="London", temperature=15.5, timestamp=datetime(2023, 1, 1, 12, 0, 0))
    assert record.city == "London"
    assert record.temperature == 15.5
    assert record.timestamp == datetime(2023, 1, 1, 12, 0, 0)

def test_weather_record_temperature_type():
    with pytest.raises(TypeError):
        WeatherRecord(city="London", temperature="hot", timestamp=datetime.now())
