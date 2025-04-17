import pytest
import threading
import json
from http.server import HTTPServer
from urllib.request import urlopen, Request
from src.presentation.api_server import WeatherAPIHandler

class DummyCurrentWeatherUseCase:
    def execute(self, city):
        if city == "London":
            return {"city": "London", "temperature": 15.0}
        raise Exception("City not found")

class DummyWeatherStatsUseCase:
    def execute(self, city):
        if city == "London":
            return {"min": 10.0, "max": 20.0, "avg": 15.0}
        return {"min": None, "max": None, "avg": None}

class TestServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_current_weather_usecase = DummyCurrentWeatherUseCase()
        self.get_weather_stats_usecase = DummyWeatherStatsUseCase()

def run_server(server):
    server.serve_forever()

@pytest.fixture(scope="module")
def api_server():
    server_address = ("localhost", 8090)
    httpd = TestServer(server_address, WeatherAPIHandler)
    thread = threading.Thread(target=run_server, args=(httpd,), daemon=True)
    thread.start()
    yield
    httpd.shutdown()

def test_get_current_weather_success(api_server):
    resp = urlopen("http://localhost:8090/weather/current/London")
    assert resp.status == 200
    data = json.loads(resp.read())
    assert data["city"] == "London"
    assert data["temperature"] == 15.0

def test_get_weather_stats_success(api_server):
    resp = urlopen("http://localhost:8090/weather/stats/London")
    assert resp.status == 200
    data = json.loads(resp.read())
    assert data["min"] == 10.0
    assert data["max"] == 20.0
    assert data["avg"] == 15.0

def test_get_current_weather_city_not_found(api_server):
    req = Request("http://localhost:8090/weather/current/Atlantis")
    try:
        urlopen(req)
    except Exception as e:
        assert hasattr(e, 'code') and e.code == 404

def test_get_weather_stats_empty(api_server):
    resp = urlopen("http://localhost:8090/weather/stats/UnknownCity")
    assert resp.status == 200
    data = json.loads(resp.read())
    assert data["min"] is None
    assert data["max"] is None
    assert data["avg"] is None

def test_404(api_server):
    req = Request("http://localhost:8090/unknown/path")
    try:
        urlopen(req)
    except Exception as e:
        assert hasattr(e, 'code') and e.code == 404

def test_400_missing_city(api_server):
    req = Request("http://localhost:8090/weather/current/")
    try:
        urlopen(req)
    except Exception as e:
        assert hasattr(e, 'code') and e.code == 400
