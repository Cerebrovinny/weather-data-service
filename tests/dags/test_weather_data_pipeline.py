import os
import sys
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def test_dag_loaded():
    from dags.weather_data_pipeline import dag
    assert dag is not None
    assert dag.dag_id == "weather_data_pipeline"

def test_city_tasks_created():
    # Load DAG and check for city tasks
    from dags.weather_data_pipeline import dag
    
    # Test that tasks for each city exist
    cities = os.environ.get("CITIES", "London,Paris,Berlin").split(",")
    for city in cities:
        task_id = f"fetch_and_store_{city.lower()}"
        assert task_id in dag.task_ids

@patch("dags.weather_data_pipeline.WeatherAPIGateway")
@patch("dags.weather_data_pipeline.WeatherStatsGateway")
def test_fetch_and_store_weather(mock_stats_gateway_class, mock_api_gateway_class):
    mock_api_gateway = MagicMock()
    mock_stats_gateway = MagicMock()
    
    mock_api_gateway_class.return_value = mock_api_gateway
    mock_stats_gateway_class.return_value = mock_stats_gateway
    
    mock_api_gateway.get_current_weather.return_value = {"temperature": 20}
    mock_stats_gateway.get_city_temperatures.return_value = [18, 19]
    
    from dags.weather_data_pipeline import fetch_and_store_weather
    
    fetch_and_store_weather("London")
    
    mock_api_gateway.get_current_weather.assert_called_once_with("London")
    mock_stats_gateway.get_city_temperatures.assert_called_once_with("London")
    mock_stats_gateway.save_city_temperatures.assert_called_once_with("London", [18, 19, 20])
