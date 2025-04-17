from src.use_cases.get_weather_stats import GetWeatherStats

class DummyWeatherStatsGateway:
    def get_city_temperatures(self, city):
        if city == "London":
            return [10.0, 15.0, 20.0]
        return []

def test_get_weather_stats_success():
    usecase = GetWeatherStats(DummyWeatherStatsGateway())
    stats = usecase.execute("London")
    assert stats["min"] == 10.0
    assert stats["max"] == 20.0
    assert stats["avg"] == 15.0

def test_get_weather_stats_empty():
    usecase = GetWeatherStats(DummyWeatherStatsGateway())
    stats = usecase.execute("UnknownCity")
    assert stats["min"] is None
    assert stats["max"] is None
    assert stats["avg"] is None
