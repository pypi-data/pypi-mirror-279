import pytz

from bs4 import BeautifulSoup
from datetime import datetime
from requests import get
from typing import AsyncGenerator, Optional
from unicodedata import normalize

from f1_weather._types import Event
from f1_weather._exceptions import LocationException
from f1_weather._fixes import locations
from f1_weather.location import get_gps_coordinates
from f1_weather.weather import Weather

_WEATHER = Weather()


async def get_events(
    year: int = 2024, filter: Optional[str] = None
) -> AsyncGenerator[Event, None]:
    """
    Parse events from the ESPN website.

    Returns:
        AsyncGenerator[Event]: An async generator of Event objects containing event information.
    """

    with get(
        url=f"https://www.espn.com/racing/schedule/_/series/f1/year/{year}",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        },  # We have to fake a User-Agent to avoid being blocked.
    ) as response:
        page = BeautifulSoup(response.text, "html.parser")
        table = page.find("table", class_="tablehead")
        for row in table.find_all("tr", class_=["oddrow", "evenrow"]):
            data = row.find_all("td")
            event_meta = data[1].get_text(separator="\n").splitlines()
            start_datetime = datetime.strptime(
                normalize("NFKD", data[0].get_text(separator=" "))
                .replace(" ET", f" {year}")
                .replace("Noon", "12:00 PM"),
                "%a, %b %d %I:%M %p %Y",
            ).replace(tzinfo=pytz.timezone("America/New_York"))
            summary: str = event_meta[2].strip("*")
            circuit: str = event_meta[1]

            try:
                lat, lon = await get_gps_coordinates(circuit)
            except LocationException:
                if locations.get(circuit, None):
                    lat, lon = await get_gps_coordinates(locations[circuit])
                else:
                    raise

            if filter and filter.lower() not in summary.lower():
                continue  # Skip events that don't match the filter.

            yield Event(
                summary=summary,
                circuit=circuit,
                start=start_datetime,
                lat=lat,
                lon=lon,
            )
