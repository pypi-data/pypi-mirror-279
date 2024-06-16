import asyncio
import click

from click_default_group import DefaultGroup
from functools import wraps
from json import dumps
from tabulate import tabulate
from typing import Optional

from f1_weather.events import get_events
from f1_weather._exceptions import WeatherException
from f1_weather.weather import Weather

WEATHER = Weather()


def run_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group(cls=DefaultGroup, default="pretty", default_if_no_args=True)
def cli() -> None:
    pass


@click.command()
@click.option("--filter", type=str, help="Filter session.")
@click.option("--skip", is_flag=True, help="Skip events without weather data.")
@click.option("--year", type=int, default=2024, help="Season year to get events for.")
@run_async
async def pretty(filter: Optional[str], skip: bool, year: int) -> None:
    async for event in get_events(year=year, filter=filter):
        try:
            forecast = await WEATHER.get_weather(event)
        except WeatherException:
            forecast = None
        table = [
            ["Session", event.summary],
            ["Location", event.circuit],
            ["Start Time", event.start.strftime("%Y-%m-%d %H:%M")],
        ]

        if forecast:
            table += [
                ["Temperature", f"{forecast.temperature:.2f}°C"],
                ["Humidity", f"{forecast.humidity:.2f}%"],
                ["Precipitation", f"{forecast.precipitation:.2f}mm"],
                ["Wind Speed", f"{forecast.wind_speed:.2f}m/s"],
                ["Wind Direction", f"{forecast.wind_direction:.2f}°"],
                ["Surface Pressure", f"{forecast.surface_pressure:.2f}hPa"],
            ]

        else:
            table += [["ERROR", "No weather data available."]]

        if not forecast and skip:
            continue

        print(tabulate(table, tablefmt="fancy_grid"))


@click.command()
@click.option("--filter", type=str, help="Filter session.")
@click.option("--skip", is_flag=True, help="Skip events without weather data.")
@click.option("--year", type=int, default=2024, help="Season year to get events for.")
@run_async
async def json(filter: Optional[str], skip: bool, year: int) -> None:
    jdoc: dict = {"sessions": []}
    async for event in get_events(year=year, filter=filter):
        try:
            forecast = await WEATHER.get_weather(event)
        except WeatherException:
            forecast = None
        jsession: dict = {
            "session": event.summary,
            "location": event.circuit,
            "startTime": event.start.strftime("%Y-%m-%dT%H:%M:%S.%f"),
        }

        if forecast:
            jsession["temperature"] = str(forecast.temperature)
            jsession["humidity"] = str(forecast.humidity)
            jsession["precipitation"] = str(forecast.precipitation)
            jsession["windSpeed"] = str(forecast.wind_speed)
            jsession["windDirection"] = str(forecast.wind_direction)
            jsession["surfacePressure"] = str(forecast.surface_pressure)
            jsession["error"] = None

        else:
            jsession["error"] = "No weather data available."

        if not forecast and skip:
            continue

        jdoc["sessions"].append(jsession)
        print(dumps(jdoc))


if __name__ == "__main__":
    cli.add_command(pretty)
    cli.add_command(json)
    cli()
