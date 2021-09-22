from .validation import *


class Calculator:
    def __init__(self):
        pass

    # you may add more parameters if needed, you may modify the formula also.
    def cost_calculation(self, initial_charge, final_charge, capacity, is_peak, is_holiday):
        validate(initial_charge=initial_charge, final_charge=final_charge, capacity=capacity)

        base_price = 100 if is_peak else 50
        surcharge_factor = 1.1 if is_holiday else 1

        return (final_charge - initial_charge) / 100 * capacity * base_price / 100 * surcharge_factor

    # you may add more parameters if needed, you may also modify the formula.
    def time_calculation(self, initial_charge, final_charge, capacity, power):
        validate(initial_charge=initial_charge, final_charge=final_charge, capacity=capacity)

        return (final_charge - initial_charge) / 100 * capacity / power

    # you may create some new methods at your convenience, or modify these methods, or choose not to use them.
    def __is_holiday(self, start_date):
        pass

    def __is_peak(self):
        pass

    def __peak_period(self, start_time):
        pass

    def __get_duration(self, start_time):
        pass

    # to be acquired through API
    def __get_sun_hour(self, sun_hour):
        pass

    # to be acquired through API
    def __get_solar_energy_duration(self, start_time):
        pass

    # to be acquired through API
    def __get_day_light_length(self, start_time):
        pass

    # to be acquired through API
    def __get_solar_insolation(self, solar_insolation):
        pass

    # to be acquired through API
    def __get_cloud_cover(self):
        pass

    def __calculate_solar_energy(self):
        pass
