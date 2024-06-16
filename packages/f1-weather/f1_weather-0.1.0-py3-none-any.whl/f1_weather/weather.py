import openmeteo_requests
import requests_cache

from datetime import datetime
from typing import Optional
from retry_requests import retry

from f1_weather._types import Event, Forecast
from f1_weather._exceptions import WeatherException


class Weather:
    """
    Class to make queries to the OpenMeteo API.
    """

    cache_session: requests_cache.CachedSession = requests_cache.CachedSession(
        ".cache", expire_after=-1
    )
    retry_session: retry = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo: openmeteo_requests.Client = openmeteo_requests.Client(
        session=retry_session
    )

    async def _get_historic(self, params: dict) -> Optional[openmeteo_requests.Client]:
        """
        Get historic weather data for an location.

        Args:
            params (dict): The parameters to pass to the API.

        Returns:
            Optional[openmeteo_requests.Client]: The response from the API.
        """
        url: str = "https://archive-api.open-meteo.com/v1/archive"

        try:
            return self.openmeteo.weather_api(url, params=params)[0]
        except openmeteo_requests.exceptions.OpenMeteoRequestsError:
            return None

    async def _get_forecast(self, params: dict) -> Optional[openmeteo_requests.Client]:
        """
        Get forecast weather data for a location.

        Args:
            params (dict): The parameters to pass to the API.

        Returns:
            Optional[openmeteo_requests.Client]: The response from the API.
        """
        url: str = "https://api.open-meteo.com/v1/forecast"

        try:
            return self.openmeteo.weather_api(url, params=params)[0]
        except Exception:
            return None

    async def get_weather(self, event: Event) -> Forecast:
        """
        Get the weather for an event.

        Args:
            event (Event): The event to get the weather for.

        Returns:
            Forecast: The weather forecast for the event.
        """
        params: dict = {
            "latitude": event.lat,
            "longitude": event.lon,
            "start_date": event.start.strftime("%Y-%m-%d"),
            "end_date": event.start.strftime("%Y-%m-%d"),
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "wind_speed_10m",
                "wind_direction_10m",
                "surface_pressure"
            ],
            "timezone": "America/New_York",
        }
        if event.start < datetime.now(tz=event.start.tzinfo):
            response = await self._get_historic(params)
        else:
            response = await self._get_forecast(params)

        if not response:
            raise WeatherException(f"Could not get weather data for {event.circuit}.")

        hourly = response.Hourly()

        temperature = hourly.Variables(0).ValuesAsNumpy()[event.start.hour]
        humidity = hourly.Variables(1).ValuesAsNumpy()[event.start.hour]
        precipitation = hourly.Variables(2).ValuesAsNumpy()[event.start.hour]
        wind_speed = hourly.Variables(3).ValuesAsNumpy()[event.start.hour]
        wind_direction = hourly.Variables(4).ValuesAsNumpy()[event.start.hour]
        surface_pressure = hourly.Variables(5).ValuesAsNumpy()[event.start.hour]

        return Forecast(
            temperature=temperature,
            humidity=humidity,
            precipitation=precipitation,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            surface_pressure=surface_pressure
        )
