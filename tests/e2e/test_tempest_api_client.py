"""End-to-end tests for the tempest_api_client module."""

import asyncio
from unittest import mock
import pytest
from src import tempest_api_client


@pytest.mark.asyncio
@mock.patch('src.tempest_api_client.process_websocket_response')
async def test_get_stations_and_devices_then_listen_for_updates(process_mock: mock.Mock):
    """Test the get_stations() call."""
    # given a token
    tok = tempest_api_client.get_token()

    # when I fetch the stations associated with that token
    stations = tempest_api_client.get_stations(tok)

    # then I should get the 1 station associated with that token in return
    assert 1 == len(stations)

    # and that station should be associated with two devices, a HUB and a weather device
    assert 2 == len(stations[0]['devices'])
    hub = [d for d in stations[0]['devices'] if d['device_type'] == 'HB'][0]
    weather_station = [d for d in stations[0]
                       ['devices'] if d['device_type'] == 'ST'][0]
    assert hub is not None
    assert weather_station is not None

    # and when I query for data related to the weather device
    device_data = tempest_api_client.get_device(
        token=tok, device_id=weather_station['device_id'])
    assert device_data is not None

    # then I should get observations in return
    assert len(device_data['obs'])
    observations = [tempest_api_client.parse_observation(
        obs=ob, device_type=device_data['type']) for ob in device_data['obs']]
    assert len(observations) > 0

    # and when I listen for updates on that device
    task = tempest_api_client.listen(tok, weather_station['device_id'])
    try:
        await asyncio.wait_for(task, 70)
    except TimeoutError:
        pass

    # then within 1 minute I should receive a fresh set of observations
    process_mock.assert_called()
