"""
Indonesia Weather Data Source for dlt

Fetches daily historical weather data for 5 major Indonesian cities
from the Open-Meteo Archive API. No API key required.

Cities: Jakarta, Surabaya, Denpasar (Bali), Medan, Makassar
Data range: Configurable (default: 2020-2025)
Resolution: Daily aggregations

API Docs: https://open-meteo.com/en/docs/historical-weather-api
"""

import dlt
import logging
import requests

logger = logging.getLogger(__name__)

# Indonesian cities with their coordinates
CITIES = {
    "Jakarta": {"latitude": -6.21, "longitude": 106.85},
    "Surabaya": {"latitude": -7.25, "longitude": 112.75},
    "Denpasar": {"latitude": -8.65, "longitude": 115.22},
    "Medan": {"latitude": 3.59, "longitude": 98.67},
    "Makassar": {"latitude": -5.14, "longitude": 119.42},
}

# Open-Meteo Historical Weather API (free, no authentication)
OPEN_METEO_BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

# Daily weather variables to fetch
DAILY_VARIABLES = [
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "precipitation_sum",
    "rain_sum",
    "windspeed_10m_max",
    "sunshine_duration",
    "weathercode",
]


@dlt.source(name="indonesia_weather")
def weather_source(start_date="2020-01-01", end_date="2025-12-31"):
    """Indonesia weather data source.

    Fetches daily weather data for all configured Indonesian cities
    from the Open-Meteo Archive API. Free, no API key required.
    """
    yield daily_weather_resource(start_date=start_date, end_date=end_date)


@dlt.resource(
    name="daily_weather",
    write_disposition="replace",
)
def daily_weather_resource(start_date, end_date):
    """Fetch daily weather data for all Indonesian cities.

    Iterates over each city and yields one row per city per day.
    Total rows: ~11,000 (5 cities x ~2,190 days for 6 years).

    Data is fetched from Open-Meteo's free historical weather API.
    No authentication or API key is required.
    """
    for city_name, coords in CITIES.items():
        logger.info(f"Fetching weather data for {city_name}...")

        params = {
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
            "start_date": start_date,
            "end_date": end_date,
            "daily": ",".join(DAILY_VARIABLES),
            "timezone": "Asia/Jakarta",
        }

        try:
            response = requests.get(
                OPEN_METEO_BASE_URL,
                params=params,
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()

            daily = data["daily"]
            dates = daily["time"]

            rows_count = 0
            for i, date in enumerate(dates):
                yield {
                    "city_name": city_name,
                    "latitude": coords["latitude"],
                    "longitude": coords["longitude"],
                    "observation_date": date,
                    "temperature_2m_max": daily["temperature_2m_max"][i],
                    "temperature_2m_min": daily["temperature_2m_min"][i],
                    "temperature_2m_mean": daily["temperature_2m_mean"][i],
                    "precipitation_sum": daily["precipitation_sum"][i],
                    "rain_sum": daily["rain_sum"][i],
                    "windspeed_10m_max": daily["windspeed_10m_max"][i],
                    "sunshine_duration": daily["sunshine_duration"][i],
                    "weather_code": daily["weathercode"][i],
                }
                rows_count += 1

            logger.info(f"  OK {city_name}: {rows_count:,} days fetched")

        except requests.exceptions.RequestException as e:
            logger.error(f"  FAIL {city_name}: network error - {e}")
        except KeyError as e:
            logger.error(f"  FAIL {city_name}: unexpected API response - missing key {e}")
        except Exception as e:
            logger.error(f"  FAIL {city_name}: {e}")
