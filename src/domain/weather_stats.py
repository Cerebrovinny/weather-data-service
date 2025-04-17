# Domain entity: WeatherStats
class WeatherStats:
    def __init__(self, temperatures):
        self.temperatures = temperatures
        if temperatures:
            self.min_temp = min(temperatures)
            self.max_temp = max(temperatures)
            self.avg_temp = sum(temperatures) / len(temperatures)
        else:
            self.min_temp = None
            self.max_temp = None
            self.avg_temp = None

