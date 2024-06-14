import os
import sys
import textwrap
from dotenv import load_dotenv


class Configurator:
    def __init__(self):
        self.env_exists = load_dotenv()
        self.geocode_auth = os.getenv('GEOCODE_AUTH') if self.env_exists else ''
        self.datahub_api_key = os.getenv('DATAHUB_API_KEY') if self.env_exists else ''
        self.datahub_secret = os.getenv('DATAHUB_SECRET') if self.env_exists else ''

    def initial_setup(self):
        """
        Takes 3 inputs from stdin for the geocode.xyz auth token, Met Office Weather DataHub API key and secret,
        which is then written out to a new .env file to use with the program.
        """
        confirmation = input(textwrap.dedent(f"""\
        WARNING: this will truncate the file at {os.path.realpath('./.env')} if it exists.
        Do you wish to continue? (Y/n)
        """))

        if confirmation.lower() != "y":
            print("Exiting without saving...")
            sys.exit(0)

        geocode_auth = input("Please enter your geocode.xyz auth token (or press enter to skip): ")
        if geocode_auth != '':
            self.geocode_auth = geocode_auth

        datahub_api_key = input("Please enter your Met Office Weather DataHub API key (or press enter to skip): ")
        if datahub_api_key != '':
            self.datahub_api_key = datahub_api_key

        self.generate_dotenv()

    def generate_dotenv(self):
        mode = 'w'
        if not self.env_exists:
            mode = 'x'
        with open('./.env', mode) as file:
            file.write(textwrap.dedent(f"""\
            # Environment variables for metoffice-weather-cli
            GEOCODE_AUTH={self.geocode_auth}
            DATAHUB_API_KEY={self.datahub_api_key}
            """))
            print(f"Saved dotenv file at {os.path.realpath('./.env')}")


if __name__ == '__main__':
    configurator = Configurator()
    configurator.initial_setup()
