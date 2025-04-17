import pytest
from src.domain.city import City

def test_city_creation():
    city = City(name="London")
    assert city.name == "London"

def test_city_name_required():
    with pytest.raises(ValueError):
        City(name=None)
