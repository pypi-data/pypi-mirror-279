import pytest
from metoffice_weather_cli.weathercodes import decode_weather_type, decode_uv_index


def test_decode_uv_index():
    assert 'Low exposure' == decode_uv_index(1)
    assert 'Medium exposure' == decode_uv_index(5)
    assert 'High exposure' == decode_uv_index(6)
    assert 'Extremely high exposure' == decode_uv_index(13)
