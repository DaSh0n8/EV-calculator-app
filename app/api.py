from datetime import date, time, timedelta
import requests


class WeatherApiInterface:
    def sunrise(self, postcode: int, day: date) -> time:
        raise NotImplemented

    def sunset(self, postcode: int, day: date) -> time:
        raise NotImplemented

    def solar_insolation(self, postcode: int, day: date) -> float:
        raise NotImplemented

    def cloud_cover(self, postcode: int, day: date, hour: int) -> float:
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

    def cloud_cover(self, postcode: int, day: date, hour: int) -> float:
        data = self.__get_data(postcode, day)

        hourData = [hd for hd in data["hourlyWeatherHistory"] if hd["hour"] == hour]
        assert len(hourData) == 1

        return hourData[0]["cloudCoverPct"] / 100

    def __get_data(self, postcode: int, day: date):
        # Get cached data, or fetch it if it isn't
        key = (postcode, day)
        if key not in self.__data:
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


class MockWeatherApi(WeatherApiInterface):
    __si: float
    __sunrise: time
    __sunset: time
    __cloud_cover: float

    def __init__(self, si: float, sunrise: time, sunset: time, cloud_cover: float):
        self.__si = si
        self.__sunrise = sunrise
        self.__sunset = sunset
        self.__cloud_cover = cloud_cover

    def sunrise(self, postcode: int, day: date) -> time:
        return self.__sunrise

    def sunset(self, postcode: int, day: date) -> time:
        return self.__sunset

    def solar_insolation(self, postcode: int, day: date) -> float:
        return self.__si

    def cloud_cover(self, postcode: int, day: date, hour: int) -> float:
        return self.__cloud_cover
