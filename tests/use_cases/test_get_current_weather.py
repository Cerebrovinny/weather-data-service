import pytest
from src.use_cases.get_current_weather import GetCurrentWeather

class DummyWeatherGateway:
    def get_current_weather(self, city):
        if city == "London":
            return {"city": "London", "temperature": 15.0}
        raise ValueError("City not found")

def test_get_current_weather_success():
    usecase = GetCurrentWeather(DummyWeatherGateway())
    result = usecase.execute("London")
    assert result["city"] == "London"
    assert result["temperature"] == 15.0

def test_get_current_weather_city_not_found():
    usecase = GetCurrentWeather(DummyWeatherGateway())
    with pytest.raises(ValueError):
        usecase.execute("Atlantis")
