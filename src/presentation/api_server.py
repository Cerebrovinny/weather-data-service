import json
import logging
import time
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from prometheus_client import Counter, Histogram, start_http_server

logger = logging.getLogger(__name__)

from src.config import Config

# Start Prometheus metrics server
start_http_server(8000)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status']
)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP Request latency',
    ['method', 'endpoint']
)
ERROR_COUNT = Counter(
    'http_errors_total',
    'Total HTTP Errors',
    ['type']
)

class WeatherAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        start_time = time.time()
        endpoint = self.path.split('?')[0]  # Remove query parameters
        logger.info(f"Request received: {self.command} {self.path}")
        logger.debug(f"Request headers: {dict(self.headers)}")
        
        # API Key authentication
        api_key = self.headers.get('X-API-Key')
        if not api_key or api_key != Config.API_KEY:
            ERROR_COUNT.labels(type='authentication').inc()
            REQUEST_COUNT.labels(method='GET', endpoint=endpoint, status=401).inc()
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'{"error": "Unauthorized: Invalid or missing API key"}')
            return
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            if path.startswith("/weather/current/"):
                city = path[len("/weather/current/"):]
                with REQUEST_LATENCY.labels(method='GET', endpoint='/weather/current').time():
                    self.handle_get_current_weather(city)
                REQUEST_COUNT.labels(method='GET', endpoint='/weather/current', status=200).inc()
            elif path.startswith("/weather/stats/"):
                city = path[len("/weather/stats/"):]
                with REQUEST_LATENCY.labels(method='GET', endpoint='/weather/stats').time():
                    self.handle_get_weather_stats(city)
                REQUEST_COUNT.labels(method='GET', endpoint='/weather/stats', status=200).inc()
            else:
                ERROR_COUNT.labels(type='not_found').inc()
                REQUEST_COUNT.labels(method='GET', endpoint=endpoint, status=404).inc()
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'{"error": "Not found"}')
        except Exception as e:
            ERROR_COUNT.labels(type='internal_error').inc()
            REQUEST_COUNT.labels(method='GET', endpoint=endpoint, status=500).inc()
            raise
        finally:
            duration = time.time() - start_time
            REQUEST_LATENCY.labels(method='GET', endpoint=endpoint).observe(duration)

    def handle_get_current_weather(self, city):
        if not city:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "City required"}')
            return
        try:
            result = self.server.get_current_weather_usecase.execute(city)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def handle_get_weather_stats(self, city):
        if not city:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "City required"}')
            return
        try:
            result = self.server.get_weather_stats_usecase.execute(city)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
