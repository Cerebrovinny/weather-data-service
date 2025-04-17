# Domain entity: City
class City:
    def __init__(self, name):
        if not name:
            raise ValueError("City name cannot be empty.")
        self.name = name

