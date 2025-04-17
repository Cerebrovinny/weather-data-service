import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

class WeatherAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path.startswith("/weather/current/"):
            city = path[len("/weather/current/"):]
            self.handle_get_current_weather(city)
        elif path.startswith("/weather/stats/"):
            city = path[len("/weather/stats/"):]
            self.handle_get_weather_stats(city)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')

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
