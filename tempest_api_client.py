"""A toy client for calling the Tempest Weather Station REST API"""

import os
import requests

BASE_URL = "https://swd.weatherflow.com/swd/rest/"

def get_token() -> str:
    """Returns the personal access token."""
    return os.getenv('TEMPEST_TOKEN')

def get_stations(token : str) -> list:
    """Returns a list of stations associated with this token."""
    url = BASE_URL + f"stations?token={token}"
    response = requests.get(url=url, timeout=30)
    return response.json()['stations']

def get_device(token: str, device_id: str) -> dict:
    url = BASE_URL + f"observations?device_id={device_id}&token={token}"
    response = requests.get(url=url, timeout=30)
    return response.json()



tok = get_token()
stations = get_stations(tok)
print("stations:")
for station in stations:
    for device in station['devices']:
        print(f"device data for {device}")
        print(get_device(device_id=device['device_id'], token=tok))
