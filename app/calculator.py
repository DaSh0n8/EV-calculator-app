from .validation import *
from .api import WeatherApi, WeatherApiInterface
from .period import *

PANEL_SIZE = 50  # 50 m^2
PANEL_EFFICIENCY = 0.2  # 20%

TOTAL_DURATION_ZERO = ValidationError("Total duration must be greater than 0 seconds")


class Calculator:
    def __init__(self, api: WeatherApiInterface):
        self.api: WeatherApiInterface = api

    def total_cost(self, initial_charge: int, final_charge: int, capacity: int,
                   charger_config: str, start_date: date, start_time: time, postcode: int) -> float:
        validate(initial_charge=initial_charge, final_charge=final_charge, capacity=capacity,
                 charger_config=charger_config, start_date=start_date, start_time=start_time)

        (power, price) = CHARGER_CONFIGS[charger_config]
        total_dur: timedelta = Calculator.charging_duration(initial_charge, final_charge, capacity, power)

        start = to_datetime(start_date, start_time)
        periods: [Period] = split(start, start + total_dur)

        total_cost = 0
        for p in periods:
            charge_kwh = Calculator.charge_amount(p, initial_charge, final_charge, total_dur)
            solar_generated = self.solar_generated(Period(p.day, p.start, p.end), postcode)
            total_cost += self.period_cost(p, charge_kwh, price, solar_generated)

        return total_cost

    @staticmethod
    def period_cost(period: Period, charge_kwh: float, price: float, solar_generated: float) -> float:
        cost = (charge_kwh - solar_generated) * price * period.base_price_factor * period.surcharge_factor
        return max(cost, 0)

    @staticmethod
    def charging_duration(initial_charge: int, final_charge: int, capacity: int, power: float) -> timedelta:
        validate(initial_charge=initial_charge, final_charge=final_charge, capacity=capacity)
        hours = (final_charge - initial_charge) / 100 * capacity / power
        return timedelta(hours=hours)

    @staticmethod
    def charge_amount(p: Period, initial_charge: int, final_charge: int, total_dur: timedelta) -> float:
        """Returns: the amount the vehicle charged in the given period in kWh"""
        validate(initial_charge=initial_charge, final_charge=final_charge)
        if total_dur.total_seconds() == 0:
            raise TOTAL_DURATION_ZERO

        charge_proportion = minus_time(p.end, p.start) / total_dur
        return (final_charge - initial_charge) * charge_proportion

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
    def get_past_years(day: date, past_years: int = 3) -> [date]:
        start_year = day.year if day < date.today() else date.today().year
        return [date(start_year - i, day.month, day.day) for i in range(past_years)]

    def __avg_solar_insolation(self, period: Period, postcode: int) -> float:
        dates = Calculator.get_past_years(period.day)
        values = [self.api.solar_insolation(postcode, d) for d in dates]
        return sum(values) / len(values)

    def __avg_cloud_cover(self, period: Period, postcode: int) -> float:
        dates = Calculator.get_past_years(period.day)
        values = [self.api.cloud_cover(postcode, d, period.start.hour) for d in dates]
        return sum(values) / len(values)
