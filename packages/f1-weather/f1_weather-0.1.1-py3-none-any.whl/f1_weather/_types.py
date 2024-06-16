from datetime import datetime


class Event:
    def __init__(
        self, summary: str, circuit: str, start: datetime, lat: float, lon: float
    ):
        self.summary: str = summary
        self.circuit: str = circuit
        self.start: datetime = start
        self.lat: float = lat
        self.lon: float = lon


class Forecast:
    def __init__(
        self,
        temperature: float,
        humidity: float,
        precipitation: float,
        wind_speed: float,
        wind_direction: float,
        surface_pressure: float,
    ):
        self.temperature: float = temperature
        self.humidity: float = humidity
        self.precipitation: float = precipitation
        self.wind_speed: float = wind_speed
        self.wind_direction: float = wind_direction
        self.surface_pressure: float = surface_pressure
