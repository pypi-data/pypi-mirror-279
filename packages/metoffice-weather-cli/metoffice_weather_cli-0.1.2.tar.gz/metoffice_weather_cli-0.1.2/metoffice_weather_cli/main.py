import argparse
import sys
from metoffice_weather_cli.configurator import Configurator
from metoffice_weather_cli import weather
from dotenv import load_dotenv


def run():
    parser = argparse.ArgumentParser(
        prog="weather-cli",
        description="A CLI tool for fetching and printing weather data"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--config',
                       action='store_true',
                       help="""Configures the .env file with your geocode.xyz auth token and
                       Met Office Weather DataHub API key"""
                       )
    group.add_argument('-s', '--search',
                       action='store',
                       nargs=1,
                       type=str,
                       metavar='<location>',
                       help="Fetch and print the weather given the name of a city or town"
                       )
    group.add_argument('-g', '--geocode',
                       action='store',
                       nargs=1,
                       type=str,
                       metavar='<location>',
                       help="Fetch and print the latitude and longitude coordinates of a city or town"
                       )
    group.add_argument('-w', '--weather',
                       action='store',
                       nargs=2,
                       type=float,
                       metavar=('<latitude>', '<longitude>'),
                       help="Fetch and print the weather at a set of latitude and longitude coordinates.",
                       )

    args = parser.parse_args()
    if args.config and len(sys.argv) > 1:
        cfg = Configurator()
        print("Running initial setup...")
        cfg.initial_setup()
        sys.exit(0)
    else:
        load_dotenv()

    if args.search is not None:
        geolocation = weather.get_geolocation(args.search)
        data = weather.get_weather_info(
            geolocation['standard']['city'],
            geolocation['standard']['countryname'],
            geolocation['latt'],
            geolocation['longt']
        )
        weather.print_results(data)

    elif args.geocode is not None:
        geolocation = weather.get_geolocation(args.search)
        print(f"{args.geocode[0]} is located at {geolocation['latt']}, {geolocation['longt']}")

    elif args.weather is not None:
        data = weather.get_weather_info(
            str(args.weather[0]),
            str(args.weather[1]),
            args.weather[0],
            args.weather[1])
        weather.print_results(data)

    else:
        parser.print_help()
