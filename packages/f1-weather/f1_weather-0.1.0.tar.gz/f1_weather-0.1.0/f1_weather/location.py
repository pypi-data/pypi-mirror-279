import logging

from OSMPythonTools import logger
from OSMPythonTools.nominatim import Nominatim

from f1_weather._exceptions import LocationException


logger.setLevel(
    logging.ERROR
)  # We don't want to see the debug messages from OSMPythonTools.


async def get_gps_coordinates(location: str) -> tuple[float, float]:
    """
    Get the GPS coordinates of a location.

    Args:
        location (str): The location to get the GPS coordinates of.

    Returns:
        tuple[float, float]: The latitude and longitude of the location.
    """
    nominatim = Nominatim()
    query = nominatim.query(location)

    try:
        return (
            float(query.toJSON()[0]["lat"]),
            float(query.toJSON()[0]["lon"]),
        )
    except IndexError:
        raise LocationException(f"Could not find GPS coordinates for {location}.")
