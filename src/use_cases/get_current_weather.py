# Use case: GetCurrentWeather

class GetCurrentWeather:
    def __init__(self, gateway):
        self.gateway = gateway

    def execute(self, city):
        return self.gateway.get_current_weather(city)
