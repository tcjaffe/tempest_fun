"""A toy client for calling the Tempest Weather Station REST and websocket APIs"""

import asyncio
import datetime
import json
import logging
import os
import uuid
import requests
# pylint: disable-next=import-error
import websockets

from devices import Observation, ObservationBase

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "https://swd.weatherflow.com/swd/rest"


def get_token() -> str:
    """Returns the personal access token."""
    return os.getenv('TEMPEST_TOKEN')


def get_stations(token: str) -> list[dict]:
    """Returns a list of stations associated with this token."""
    url = f"{BASE_URL}/stations?token={token}"
    response = requests.get(url=url, timeout=30)
    return response.json()['stations']


def get_device(token: str, device_id: str) -> dict:
    """Returns a dict representation of this device."""
    url = f"{BASE_URL}/observations/device/{device_id}?token={token}"
    response = requests.get(url=url, timeout=30)
    return response.json()


def parse_observation(obs: dict, device_type: str) -> ObservationBase:
    """Return an object extending the ObservationBase type"""
    match device_type:
        case 'obs_st':
            return Observation(obs)
        case _:
            raise NotImplementedError()
    raise NotImplementedError()


async def listen(token: str, device_id: str) -> None:
    """Listen for observations and events on the given device."""
    async with get_websocket_connection(token) as websocket:

        # Start listening
        message = {
            "type": "listen_start",
            "device_id": device_id,
            "id": str(uuid.uuid4())
        }
        await websocket.send(json.dumps(message))
        logger.info(
            "Now listening for observations and events on device %s", device_id)

        # Process the responses
        async for response in websocket:
            if response:
                logger.info("Received: %s", response)
                process_websocket_response(response)


def process_websocket_response(response: str | bytes) -> None:
    """ Process the response from the websocket.
        NOTE: Right now it just logs the observation data.
    """
    device_info = json.loads(response)
    if 'obs' in device_info:
        logger.info("Observations:")
        for ob in device_info['obs']:
            logger.info(parse_observation(ob, device_info['type']))


def get_websocket_connection(token: str) -> websockets.connect:
    """Returns a websocket connection to the tempest API for devices associated with the token."""
    return websockets.connect(f'wss://ws.weatherflow.com/swd/data?token={token}')


async def listen_for_updates(token: str, listenable_devices: list[str]) -> None:
    """Listen for updates on the provided list of devices."""
    if listenable_devices:
        tasks = [listen(token, did) for did in listenable_devices]
        await asyncio.gather(*tasks)


def get_listenable_devices(tok: str, stations: list[dict]) -> list[str]:
    """Returns list of devices that can provide observation data."""
    listenable_devices = []

    for station in stations:
        logger.info("Pull devices for station %s", station['station_id'])
        for device in station['devices']:
            # Only bother with 'ST' type devices.
            # The list actually includes the hub, too, so you need to exclude that.
            if 'ST' == device['device_type']:

                # Add it to our list of devices to listen for updates on.
                did = device['device_id']
                listenable_devices.append(did)
                device_data = get_device(device_id=did, token=tok)

                # Log the latest observation(s) on that device.
                if 'obs' in device_data:
                    for ob in device_data['obs']:
                        parsed = parse_observation(ob, device_data['type'])
                        last_seen = datetime.datetime.fromtimestamp(
                            parsed.timestamp)
                        logger.info(
                            "Device with id %s was last heard from at %s"
                            + "with the following observations:", did, last_seen)

    return listenable_devices


async def main():
    """Query data for all available stations and then listen for updates."""

    tok = get_token()
    stations = get_stations(tok)
    listenable_devices = get_listenable_devices(tok, stations)

    await listen_for_updates(tok, listenable_devices)


if __name__ == "__main__":
    asyncio.run(main())
