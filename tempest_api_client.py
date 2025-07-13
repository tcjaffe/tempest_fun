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


tok = get_token()
print(get_stations(tok))
