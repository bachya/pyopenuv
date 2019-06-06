"""Define fixtures for the client."""
import pytest


@pytest.fixture()
def fixture_protection_window():
    """Return a /protection response."""
    return {
        "result": {
            "from_time": "2018-07-30T15:17:49.750Z",
            "from_uv": 3.2509,
            "to_time": "2018-07-30T22:47:49.750Z",
            "to_uv": 3.6483,
        }
    }


@pytest.fixture()
def fixture_uv_forecast():
    """Return a /forecast response."""
    return {
        "result": [
            {
                "uv": 0,
                "uv_time": "2018-07-30T11:57:49.750Z",
                "sun_position": {
                    "azimuth": -2.0081567900835937,
                    "altitude": -0.011856950133816461,
                },
            },
            {
                "uv": 0.2446,
                "uv_time": "2018-07-30T12:57:49.750Z",
                "sun_position": {
                    "azimuth": -1.845666592871966,
                    "altitude": 0.1764062658258758,
                },
            },
        ]
    }


@pytest.fixture()
def fixture_uv_index():
    """Return a /uv response."""
    return {
        "result": {
            "uv": 8.2342,
            "uv_time": "2018-07-30T20:53:06.302Z",
            "uv_max": 10.3335,
            "uv_max_time": "2018-07-30T19:07:11.505Z",
            "ozone": 300.7,
            "ozone_time": "2018-07-30T18:07:04.466Z",
            "safe_exposure_time": {
                "st1": 20,
                "st2": 24,
                "st3": 32,
                "st4": 40,
                "st5": 65,
                "st6": 121,
            },
            "sun_info": {
                "sun_times": {
                    "solarNoon": "2018-07-30T19:07:11.505Z",
                    "nadir": "2018-07-30T07:07:11.505Z",
                    "sunrise": "2018-07-30T11:57:49.750Z",
                    "sunset": "2018-07-31T02:16:33.259Z",
                    "sunriseEnd": "2018-07-30T12:00:53.253Z",
                    "sunsetStart": "2018-07-31T02:13:29.756Z",
                    "dawn": "2018-07-30T11:27:27.911Z",
                    "dusk": "2018-07-31T02:46:55.099Z",
                    "nauticalDawn": "2018-07-30T10:50:01.621Z",
                    "nauticalDusk": "2018-07-31T03:24:21.389Z",
                    "nightEnd": "2018-07-30T10:08:47.846Z",
                    "night": "2018-07-31T04:05:35.163Z",
                    "goldenHourEnd": "2018-07-30T12:36:14.026Z",
                    "goldenHour": "2018-07-31T01:38:08.983Z",
                },
                "sun_position": {
                    "azimuth": 0.9567419441563509,
                    "altitude": 1.0235714275875594,
                },
            },
        }
    }
