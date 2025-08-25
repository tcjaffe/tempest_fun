"""A toy client for calling the Tempest Weather Station REST API"""

import asyncio
import datetime
import json
import logging
import os
import requests
# pylint: disable-next=import-error
import websockets

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "https://swd.weatherflow.com/swd/rest/"


def get_token() -> str:
    """Returns the personal access token."""
    return os.getenv('TEMPEST_TOKEN')


def get_stations(token: str) -> list:
    """Returns a list of stations associated with this token."""
    url = BASE_URL + f"stations?token={token}"
    response = requests.get(url=url, timeout=30)
    return response.json()['stations']


def get_device(token: str, device_id: str) -> dict:
    """Returns a dict representation of this device."""
    url = BASE_URL + f"observations/device/{device_id}?token={token}"
    response = requests.get(url=url, timeout=30)
    return response.json()


# pylint: disable-next=too-few-public-methods
class ObservationBase:
    """The base class for Tempest Weather Station observations."""
    # timestamp: datetime
    timestamp: int

    def __str__(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)


# pylint: disable-next=too-few-public-methods,too-many-instance-attributes
class Observation(ObservationBase):
    """Represents observation data returned by the Tempest Weather Station."""
    wind_lull: float
    """In m/s"""
    wind_avr: float
    """In m/s"""
    wind_gust: float
    """In m/s"""
    wind_direction: int
    """In degrees"""
    wind_sample_interval: int
    """In seconds."""
    pressure: float
    """(mb)"""
    air_temp: float
    """Celsius"""
    relative_humidity: float
    """Percentage"""
    illuminance: float
    """lux"""
    uv: float
    """index"""
    solar_radiation: float
    """(W/m²)"""
    rain_accumulation: float
    """rain accumulation during the reporting interval (mm)"""
    precipitation_type: int
    """0 = none, 1 = rain, 2 = hail, 3 = rain + hail (experimental)"""
    lightning_average_distance: float
    """(km)"""
    lightning_strike_count: int
    """number of strikes during the reporting interval"""
    battery: float
    """volts"""
    reporting_interval: int
    """minutes"""
    local_day_rain_accumulation: float
    """midnight to midnight rain accumulation in the station's timezone (mm)"""
    nearcast_rain_accumulation: float
    """(mm)"""
    local_day_nearcast_rain_accumulation: float
    """midnight to midnight Nearcast rain accumulation in the station's timezone (mm)"""
    precipitation_analysis_type: int
    """0 = none, 1 = Nearcast value with display on, 2 = Nearcast value with display off"""

    def __init__(self, raw_obs: list):
        # self.timestamp = datetime.datetime.fromtimestamp(raw_obs[0], tz=datetime.timezone.utc)
        # I changed how timestamp is stored so it would be easy to print this object.
        # That's not great, but so far I don't need it for anything else.
        self.timestamp = raw_obs[0]
        self.wind_lull = raw_obs[1]
        self.wind_avr = raw_obs[2]
        self.wind_gust = raw_obs[3]
        self.wind_direction = raw_obs[4]
        self.wind_sample_interval = raw_obs[5]
        self.pressure = raw_obs[6]
        self.air_temp = raw_obs[7]
        self.relative_humidity = raw_obs[8]
        self.illuminance = raw_obs[9]
        self.uv = raw_obs[10]
        self.solar_radiation = raw_obs[11]
        self.rain_accumulation = raw_obs[12]
        self.precipitation_type = raw_obs[13]
        self.lightning_average_distance = raw_obs[14]
        self.lightning_strike_count = raw_obs[15]
        self.battery = raw_obs[16]
        self.reporting_interval = raw_obs[17]
        self.local_day_rain_accumulation = raw_obs[18]
        self.nearcast_rain_accumulation = raw_obs[19]
        self.local_day_nearcast_rain_accumulation = raw_obs[20]
        self.precipitation_analysis_type = raw_obs[21]


def parse_observation(obs: dict, device_type: str) -> ObservationBase:
    """Return an object extending the ObservationBase type"""
    match device_type:
        case 'obs_st':
            return Observation(obs)
        case _:
            raise NotImplementedError()
    raise NotImplementedError()


async def listen(token: str, device_id: str):
    """Listen for observations and events on the given device."""
    async with websockets.connect(f'wss://ws.weatherflow.com/swd/data?token={token}') as websocket:
        message = {
            "type": "listen_start",
            "device_id": device_id,
            "id": "2098388936"
        }
        # Send the message to the server
        await websocket.send(json.dumps(message))
        # Process the responses
        async for response in websocket:
            if response:
                logger.info("Received: %s", response)

if __name__ == "__main__":

    tok = get_token()
    stations = get_stations(tok)

    for station in stations:
        logger.info("Pull devices for station %s", station['station_id'])
        for device in station['devices']:
            did = device['device_id']

            device_data = get_device(device_id=did, token=tok)

            if 'obs' in device_data:
                for ob in device_data['obs']:
                    last_seen = datetime.datetime.fromtimestamp(float(ob[0]))
                    logger.info(
                        "Device with id %s was last heard from at %s", did, last_seen)
                    x = parse_observation(ob, device_data['type'])
                    logger.info(x)

                logger.info(
                    "Listen for observations and events on device %s", did)
                asyncio.run(listen(tok, did))
