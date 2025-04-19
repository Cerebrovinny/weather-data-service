import os
import pytest
from unittest.mock import patch, MagicMock
from airflow.models import DagBag

def test_dag_loaded():
    dagbag = DagBag(dag_folder="./dags", include_examples=False)
    assert "weather_data_pipeline" in dagbag.dags
    assert dagbag.import_errors == {}

def test_city_tasks_created():
    dagbag = DagBag(dag_folder="./dags", include_examples=False)
    dag = dagbag.get_dag("weather_data_pipeline")
    cities = os.environ.get("CITIES", "London,Paris,Berlin").split(",")
    for city in cities:
        task_id = f"fetch_and_store_{city.lower()}"
        assert task_id in dag.task_ids

@patch("src.gateways.weather_api_gateway.WeatherAPIGateway.get_current_weather")
@patch("src.gateways.weather_stats_gateway.WeatherStatsGateway.get_city_temperatures")
@patch("src.gateways.weather_stats_gateway.WeatherStatsGateway.save_city_temperatures")
def test_fetch_and_store_weather(mock_save, mock_get_temps, mock_get_weather):
    # Setup mocks
    mock_get_weather.return_value = {"temperature": 20}
    mock_get_temps.return_value = [18, 19]
    from dags.weather_data_pipeline import fetch_and_store_weather
    fetch_and_store_weather("London")
    mock_get_weather.assert_called_once_with("London")
    mock_get_temps.assert_called_once_with("London")
    mock_save.assert_called_once_with("London", [18, 19, 20])
