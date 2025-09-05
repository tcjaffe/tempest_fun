"""Classes used to represent Tempest data."""

import json


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
        self.timestamp = int(raw_obs[0])
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
