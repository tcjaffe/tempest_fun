"""End-to-end tests for the tempest_api_client module."""

from src import tempest_api_client


def test_get_stations():
    """Test the get_stations() call."""
    # given a token
    tok = tempest_api_client.get_token()

    # when I fetch the stations associated with that token
    stations = tempest_api_client.get_stations(tok)

    # then I should get the 1 station associated with that token in return
    assert 1 == len(stations)
