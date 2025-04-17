from src.domain.weather_stats import WeatherStats

def test_weather_stats_computation():
    stats = WeatherStats([10.0, 20.0, 15.0])
    assert stats.min_temp == 10.0
    assert stats.max_temp == 20.0
    assert stats.avg_temp == 15.0

def test_weather_stats_empty():
    stats = WeatherStats([])
    assert stats.min_temp is None
    assert stats.max_temp is None
    assert stats.avg_temp is None
