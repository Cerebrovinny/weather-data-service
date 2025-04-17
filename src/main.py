from http.server import HTTPServer
from src.presentation.api_server import WeatherAPIHandler
from src.use_cases.get_current_weather import GetCurrentWeather
from src.use_cases.get_weather_stats import GetWeatherStats
from src.gateways.weather_api_gateway import WeatherAPIGateway
from src.gateways.weather_stats_gateway import WeatherStatsGateway

class WeatherAPIServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, current_weather_usecase, weather_stats_usecase):
        super().__init__(server_address, RequestHandlerClass)
        self.get_current_weather_usecase = current_weather_usecase
        self.get_weather_stats_usecase = weather_stats_usecase

def main():
    current_weather_usecase = GetCurrentWeather(WeatherAPIGateway())
    weather_stats_usecase = GetWeatherStats(WeatherStatsGateway())
    server_address = ("", 8080)
    httpd = WeatherAPIServer(server_address, WeatherAPIHandler, current_weather_usecase, weather_stats_usecase)
    print("Weather API server running on port 8080...")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
