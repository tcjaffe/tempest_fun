"""A toy client for calling the Tempest Weather Station REST API"""

import datetime
import os
import requests

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


tok = get_token()
stations = get_stations(tok)

for station in stations:
    print(f"pull devices for station {station}")
    for device in station['devices']:
        did = device['device_id']

        print(f"device data for {did}:")
        device_data = get_device(device_id=did, token=tok)
        print(device_data)

        if 'obs' in device_data:
            for ob in device_data['obs']:
                last_seen = datetime.datetime.fromtimestamp(float(ob[0]))
                print(
                    f'This device was last heard from at {last_seen}')
