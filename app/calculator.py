from .validation import *
from .api import WeatherApi, WeatherApiInterface
from .period import *

PANEL_SIZE = 50  # 50 m^2
PANEL_EFFICIENCY = 0.2  # 20%
AVERAGE_POINTS = 3


class Calculator:
    def __init__(self, api: WeatherApiInterface = WeatherApi()):
        self.api = api

    def cost(self, initial_charge: int, final_charge: int, capacity: int,
             charger_config: int, start_date: date, start_time: time, postcode: int) -> float:
        (power, price) = CHARGER_CONFIGS[charger_config]
        total_dur: timedelta = Calculator.charging_duration(initial_charge, final_charge, capacity, power)

        start = to_datetime(start_date, start_time)
        periods: [Period] = split(start, start + total_dur)

        total_cost = 0
        for p in periods:
            charge = Calculator.period_charge(p, initial_charge, final_charge, total_dur)
            total_cost += self.period_cost(p, charge, postcode, capacity, price)

        return total_cost

    @staticmethod
    def charging_duration(initial_charge: int, final_charge: int, capacity: int, power: int) -> timedelta:
        hours = (final_charge - initial_charge) / 100 * capacity / power
        return timedelta(hours=hours)

    @staticmethod
    def period_charge(p: Period, initial_charge: int, final_charge: int, total_dur: timedelta) -> float:
        charge_proportion = minus_time(p.end, p.start) / total_dur
        return (final_charge - initial_charge) * charge_proportion

    def period_cost(self, period: Period, charge: float, postcode: int, capacity: int, price: float) -> float:
        energy_used = charge / 100 * capacity
        energy_charged = energy_used - self.solar_generated(period, postcode)

        cost = energy_charged * price * period.base_price_factor / 100 * period.surcharge_factor
        return max(cost, 0)

    def solar_generated(self, period: Period, postcode: int) -> float:
        sunrise = self.api.sunrise(postcode, period.day)
        sunset = self.api.sunset(postcode, period.day)
        dl_hours = minus_time(sunset, sunrise).total_seconds() / 60 / 60

        si = self.__avg_solar_insolation(period, postcode)
        cc = self.__avg_cloud_cover(period, postcode)
        generated_per_hour = (si / dl_hours) * (1 - cc) * PANEL_SIZE * PANEL_EFFICIENCY

        earliest_start = max(sunrise, period.start)
        latest_end = min(sunset, period.end)
        hours_generating = minus_time(latest_end, earliest_start).total_seconds() / 60 / 60

        total: float = generated_per_hour * hours_generating
        return total

    @staticmethod
    def __get_closest_avg_dates(day: date) -> [date]:
        start_year = day.year if day < date.today() else date.today().year
        return [date(start_year - i, day.month, day.day) for i in range(AVERAGE_POINTS)]

    def __avg_solar_insolation(self, period: Period, postcode: int) -> float:
        dates = Calculator.__get_closest_avg_dates(period.day)
        values = [self.api.solar_insolation(postcode, d) for d in dates]
        return sum(values) / len(values)

    def __avg_cloud_cover(self, period: Period, postcode: int) -> float:
        dates = Calculator.__get_closest_avg_dates(period.day)
        values = [self.api.cloud_cover(postcode, d, period.start.hour) for d in dates]
        return sum(values) / len(values)
