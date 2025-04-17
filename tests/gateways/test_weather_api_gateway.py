import pytest
from unittest.mock import patch
from src.gateways.weather_api_gateway import WeatherAPIGateway

@patch("src.gateways.weather_api_gateway.requests.get")
def test_get_current_weather_success(mock_get, monkeypatch):
    monkeypatch.setattr("src.config.Config.OPENWEATHERMAP_API_KEY", "dummy")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"main": {"temp": 12.3}}
    gw = WeatherAPIGateway()
    result = gw.get_current_weather("London")
    assert result["city"] == "London"
    assert result["temperature"] == 12.3

@patch("src.gateways.weather_api_gateway.requests.get")
def test_get_current_weather_city_not_found(mock_get, monkeypatch):
    monkeypatch.setattr("src.config.Config.OPENWEATHERMAP_API_KEY", "dummy")
    mock_get.return_value.status_code = 404
    gw = WeatherAPIGateway()
    with pytest.raises(ValueError):
        gw.get_current_weather("Atlantis")

@patch("src.gateways.weather_api_gateway.requests.get")
def test_get_current_weather_api_error(mock_get, monkeypatch):
    monkeypatch.setattr("src.config.Config.OPENWEATHERMAP_API_KEY", "dummy")
    mock_get.return_value.status_code = 500
    gw = WeatherAPIGateway()
    with pytest.raises(RuntimeError):
        gw.get_current_weather("London")
