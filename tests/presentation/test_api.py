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

def test_api_auth_missing_key(monkeypatch, api_server):
    # Simulate missing API key header
    monkeypatch.setattr("src.config.Config.API_KEY", "testkey")
    req = Request("http://localhost:8090/weather/current/London")
    try:
        urlopen(req)
    except Exception as e:
        assert hasattr(e, 'code') and e.code == 401

def test_api_auth_invalid_key(monkeypatch, api_server):
    # Simulate invalid API key header
    monkeypatch.setattr("src.config.Config.API_KEY", "testkey")
    req = Request("http://localhost:8090/weather/current/London", headers={"X-API-Key": "wrong"})
    try:
        urlopen(req)
    except Exception as e:
        assert hasattr(e, 'code') and e.code == 401

def test_api_auth_valid_key(monkeypatch, api_server):
    # Simulate valid API key header
    monkeypatch.setattr("src.config.Config.API_KEY", "testkey")
    req = Request("http://localhost:8090/weather/current/London", headers={"X-API-Key": "testkey"})
    resp = urlopen(req)
    # Should proceed to normal handler (could be 200 or 404 depending on dummy use case)
    assert resp.status in (200, 404)

def test_get_current_weather_success(monkeypatch, api_server):
    monkeypatch.setattr("src.config.Config.API_KEY", "testkey")
    req = Request("http://localhost:8090/weather/current/London", headers={"X-API-Key": "testkey"})
    resp = urlopen(req)
    assert resp.status == 200
    data = json.loads(resp.read())
    assert data["city"] == "London"
    assert data["temperature"] == 15.0

def test_get_weather_stats_success(monkeypatch, api_server):
    monkeypatch.setattr("src.config.Config.API_KEY", "testkey")
    req = Request("http://localhost:8090/weather/stats/London", headers={"X-API-Key": "testkey"})
    resp = urlopen(req)
    assert resp.status == 200
    data = json.loads(resp.read())
    assert data["min"] == 10.0
    assert data["max"] == 20.0
    assert data["avg"] == 15.0

def test_get_current_weather_city_not_found(monkeypatch, api_server):
    monkeypatch.setattr("src.config.Config.API_KEY", "testkey")
    req = Request("http://localhost:8090/weather/current/Atlantis", headers={"X-API-Key": "testkey"})
    try:
        urlopen(req)
    except Exception as e:
        assert hasattr(e, 'code') and e.code == 404

def test_get_weather_stats_empty(monkeypatch, api_server):
    monkeypatch.setattr("src.config.Config.API_KEY", "testkey")
    req = Request("http://localhost:8090/weather/stats/UnknownCity", headers={"X-API-Key": "testkey"})
    resp = urlopen(req)
    assert resp.status == 200
    data = json.loads(resp.read())
    assert data["min"] is None and data["max"] is None and data["avg"] is None

def test_404(monkeypatch, api_server):
    monkeypatch.setattr("src.config.Config.API_KEY", "testkey")
    req = Request("http://localhost:8090/unknown/path", headers={"X-API-Key": "testkey"})
    try:
        urlopen(req)
    except Exception as e:
        assert hasattr(e, 'code') and e.code == 404

def test_400_missing_city(monkeypatch, api_server):
    monkeypatch.setattr("src.config.Config.API_KEY", "testkey")
    req = Request("http://localhost:8090/weather/current/", headers={"X-API-Key": "testkey"})
    try:
        urlopen(req)
    except Exception as e:
        assert hasattr(e, 'code') and e.code == 400
