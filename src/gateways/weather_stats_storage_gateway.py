from abc import ABC, abstractmethod
from typing import List

class WeatherStatsStorageGateway(ABC):
    @abstractmethod
    def get_city_temperatures(self, city: str) -> List[float]:
        """Retrieve historical temperature records for a city."""
        pass

    @abstractmethod
    def save_city_temperatures(self, city: str, temperatures: List[float]) -> None:
        """Persist temperature records for a city."""
        pass
