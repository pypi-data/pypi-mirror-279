# metoffice-weather-cli
A CLI tool for fetching and printing weather data from the 
[Met Office Weather DataHub API](https://metoffice.apiconnect.ibmcloud.com/metoffice/production/).

## Installation  

### PyPI
Open the command line and type `python3 -m pip install metoffice-weather-cli`. You can then run the program anywhere
by typing `python3 -m metoffice_weather_cli <flags>`.  

Note: you may need to replace `python3` with your OS's equivalent.

## Usage

To use this program, you must have a Met Office Weather DataHub API key and
a geocode.xyz Auth token (optional, used for geocoding only). These can be added by running the program with 
the `-c` flag or manually added in a .env file placed in the `metoffice-weather-cli` package directory as such:
```
DATAHUB_API_KEY=xxxxxxxx
DATAHUB_SECRET=xxxxxxxx
GEOCODE_AUTH=xxxxxxxx
```
Run `python3 -m metoffice_weather_cli` in the command line (optionally with the `-h` flag) to view the help page.

## Todo

- Pick all 'useful' information out of the Met Office data - some is currently omitted
- Allow preferences to be set in a config file for the data printed out
- Switch from .env-based saving of API keys to another format (e.g. JSON) to avoid wiping files containing
environment variables unrelated to the program
