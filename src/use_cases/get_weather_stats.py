# Use case: GetWeatherStats

class GetWeatherStats:
    def __init__(self, gateway):
        self.gateway = gateway

    def execute(self, city):
        temps = self.gateway.get_city_temperatures(city)
        if temps:
            return {
                "min": min(temps),
                "max": max(temps),
                "avg": sum(temps) / len(temps)
            }
        return {"min": None, "max": None, "avg": None}
