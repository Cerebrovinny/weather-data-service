import requests
from src.config import Config

class WeatherAPIGateway:
    def get_current_weather(self, city):
        api_key = Config.OPENWEATHERMAP_API_KEY
        if not api_key:
            raise RuntimeError("OpenWeatherMap API key not configured.")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 404:
            raise ValueError("City not found")
        if resp.status_code != 200:
            raise RuntimeError(f"OpenWeatherMap error: {resp.status_code}")
        data = resp.json()
        return {"city": city, "temperature": data["main"]["temp"]}
