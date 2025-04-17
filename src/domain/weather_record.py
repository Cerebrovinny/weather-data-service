# Domain entity: WeatherRecord
class WeatherRecord:
    def __init__(self, city, temperature, timestamp):
        if not isinstance(temperature, (float, int)):
            raise TypeError("Temperature must be a float or int.")
        self.city = city
        self.temperature = temperature
        self.timestamp = timestamp

