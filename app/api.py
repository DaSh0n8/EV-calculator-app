from datetime import date, time, timedelta
import requests


class WeatherApiInterface:
    def sunrise(self, postcode: int, day: date) -> time:
        raise NotImplemented

    def sunset(self, postcode: int, day: date) -> time:
        raise NotImplemented

    def solar_insolation(self, postcode: int, day: date) -> float:
        raise NotImplemented


class WeatherApi(WeatherApiInterface):
    URI = "http://118.138.246.158/api/v1"

    def __init__(self):
        self.__data = {}

    def sunrise(self, postcode: int, day: date) -> time:
        return time.fromisoformat(self.__get_data(postcode, day)["sunrise"])

    def sunset(self, postcode: int, day: date) -> time:
        return time.fromisoformat(self.__get_data(postcode, day)["sunset"])

    def solar_insolation(self, postcode: int, day: date) -> float:
        return float(self.__get_data(postcode, day)["sunHours"])

    def __get_data(self, postcode: int, day: date):
        # Get cached data, or fetch it if it isn't
        key = (postcode, day)
        if self.__data[key] is None:
            self.__data[key] = WeatherApi.fetch_data(postcode, day)
        return self.__data[key]

    @staticmethod
    def fetch_location_id(postcode: int) -> str:
        locations = requests.get(f"{WeatherApi.URI}/location", params={"postcode": postcode}).json()
        return locations[0]["id"]

    @staticmethod
    def fetch_data(postcode: int, day: date):
        loc_id = WeatherApi.fetch_location_id(postcode)
        return requests.get(f"{WeatherApi.URI}/weather", params={"location": loc_id, "date": str(day)}).json()
