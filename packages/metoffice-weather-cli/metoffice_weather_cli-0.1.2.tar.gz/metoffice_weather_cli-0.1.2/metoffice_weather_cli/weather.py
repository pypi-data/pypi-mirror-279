import os
from dotenv import load_dotenv, find_dotenv
import http.client
import urllib.parse
import json
from metoffice_weather_cli.weathercodes import decode_weather_type, decode_uv_index


def get_geolocation(location: str):
    load_dotenv()
    # connect to geocoding API
    _check_env_variable_exists('GEOCODE_AUTH')

    connection = http.client.HTTPSConnection("geocode.xyz")
    params = urllib.parse.urlencode({
        'auth': os.getenv('GEOCODE_AUTH'),
        'locate': location,
        'json': 1
    })

    connection.request("GET", "/?{}".format(params))

    geocode_res = connection.getresponse()
    geocode_json = json.loads(geocode_res.read())  # reads JSON file from response

    if 'error' in geocode_json:
        raise KeyError("API error - your request produced no suggestions.")
    return geocode_json


def get_weather_info(city: str, country: str, latt: float, longt: float):
    load_dotenv()
    _check_env_variable_exists('DATAHUB_API_KEY')

    # connect to Weather DataHub
    datahub_conn = http.client.HTTPSConnection("data.hub.api.metoffice.gov.uk")

    datahub_headers = {
        'apikey': os.getenv('DATAHUB_API_KEY'),
        'accept': "application/json"
    }

    datahub_params = urllib.parse.urlencode({
        'excludeParameterMetadata': 'true',
        'includeLocationName': 'true',
        'latitude': str(latt),
        'longitude': str(longt)
    })

    datahub_conn.request('GET',
                         '/sitespecific/v0/point/daily?{}'.format(datahub_params),
                         headers=datahub_headers
                         )

    datahub_res = datahub_conn.getresponse()
    datahub_json = json.loads(datahub_res.read())

    if 'features' not in datahub_json:
        raise KeyError("Met Office API error - check that your API key and secret are correct.")
    time_series = datahub_json['features'][0]['properties']['timeSeries'][1]

    weather_data = {
        "City": city,
        "Country": country,
        "TimeOfModel": time_series['time'],
        "WeatherType": decode_weather_type(time_series['daySignificantWeatherCode']),
        "MaxTemperature": time_series['dayUpperBoundMaxTemp'],  # degrees Celsius
        "MinTemperature": time_series['dayLowerBoundMaxTemp'],
        "ChanceOfPrecipitation": time_series['dayProbabilityOfPrecipitation'],  # %
        "WindSpeed": time_series['midday10MWindSpeed'],  # m/s
        "MaxUvIndex": time_series['maxUvIndex'],
        "SignificantWeatherCode": str(time_series['daySignificantWeatherCode']),
        "MeanSeaLevelPressure": time_series['middayMslp'],  # bar
        "Visibility": time_series['middayVisibility'],  # m
        "WindDirection": time_series['midday10MWindDirection'],  # bearing
        "RelativeHumidity": time_series['middayRelativeHumidity'] / 100,  # %
        "ProbabilityOfSnow": time_series['dayProbabilityOfSnow'] / 100,  # %
        "ProbabilityOfHail": time_series['dayProbabilityOfHail'] / 100,  # %
        "ProbabilityOfSferics": time_series['dayProbabilityOfSferics'] / 100  # %
    }
    return weather_data


def _check_env_variable_exists(env_variable):
    if os.getenv(env_variable) is None or os.getenv(env_variable) == '':
        raise ValueError(f"'{env_variable}' environment variable not set, check your .env file")


def print_results(data):
    # todo: control which options are printed as determined by args
    print(f"Weather for {data['City']}, {data['Country']}")
    print(f"Weather: {data['WeatherType']}")
    print(f"Max temp: {round(data['MaxTemperature'])} degrees Celsius")
    print(f"Min temp: {round(data['MinTemperature'])} degrees Celsius")
    print(f"Chance of precipitation: {data['ChanceOfPrecipitation']}%")
    print(f"Wind speed: {round(float(data['WindSpeed'] / 0.44704), 1)} mph")
    print(f"Peak UV Index: {data['MaxUvIndex']} ({decode_uv_index(data['MaxUvIndex'])})")


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    print("Please enter desired city:")
    stdin = input("> ")
    geolocation = get_geolocation(stdin)
    result = get_weather_info(
        geolocation['standard']['city'],
        geolocation['standard']['countryname'],
        geolocation['latt'],
        geolocation['longt']
    )
    print_results(result)
