class Calculator():
    # you can choose to initialise variables here, if needed.
    def __init__(self):
        pass

    # you may add more parameters if needed, you may modify the formula also.
    def cost_calculation(self, initial_state, final_state, capacity, is_peak, is_holiday):
        if is_peak:
            base_price = 100
        else:
            base_price = 50

        if is_holiday:
            surcharge_factor = 1.1
        else:
            surcharge_factor = 1

        cost = (final_state - initial_state) / 100 * capacity * base_price / 100 * surcharge_factor
        return cost

    # you may add more parameters if needed, you may also modify the formula.
    def time_calculation(self, initial_state, final_state, capacity, power):
        time = (final_state - initial_state) / 100 * capacity / power
        return time

    def battery_test(self, capacity):
        cost = self.cost_calculation(20, 30, capacity, False, False)
        return cost

    def soc_test(self, initial_state, final_state):
        if (type(initial_state) != int) or (type(final_state) != int):
            result = "Must be numerical value"
            return result
        elif (initial_state > 100) or (final_state > 100):
            result = "Percentage cannot exceed 100"
            return result
        elif (initial_state < 0) or (final_state < 0):
            result = "Percentage cannot be lower than 0"
            return result
        else:
            result = self.cost_calculation(initial_state, final_state, 75, True, True)
            return result

    def time_and_date_test(self, on_peak, surcharge):
        if isinstance(on_peak, bool) and isinstance(surcharge, bool):
            result = self.cost_calculation(20, 30, 75, on_peak, surcharge)
            return result
        else:
            result = "Must be either True or False"
            return result

    def charger_config_test(self, configuration):
        if configuration == 1:
            power = 2
            time = self.time_calculation(20, 30, 75, power)
            return time
        elif configuration == 2:
            power = 3.6
            time = self.time_calculation(20, 30, 75, power)
            return time
        elif configuration == 3:
            power = 7.2
            time = self.time_calculation(20, 30, 75, power)
            return time
        elif configuration == 4:
            power = 11
            time = self.time_calculation(20, 30, 75, power)
            return time
        elif configuration == 5:
            power = 22
            time = self.time_calculation(20, 30, 75, power)
            return time
        elif configuration == 6:
            power = 36
            time = self.time_calculation(20, 30, 75, power)
            return time
        elif configuration == 7:
            power = 90
            time = self.time_calculation(20, 30, 75, power)
            return time
        elif configuration == 8:
            power = 350
            time = self.time_calculation(20, 30, 75, power)
            return time
        else:
            time = "Configuration must be in rage 1-8"
            return time

    # you may create some new methods at your convenience, or modify these methods, or choose not to use them.
    def is_holiday(self, start_date):
        pass

    def is_peak(self):
        pass

    def peak_period(self, start_time):
        pass

    def get_duration(self, start_time):
        pass

    # to be acquired through API
    def get_sun_hour(self, sun_hour):
        pass

    # to be acquired through API
    def get_solar_energy_duration(self, start_time):
        pass

    # to be acquired through API
    def get_day_light_length(self, start_time):
        pass

    # to be acquired through API
    def get_solar_insolation(self, solar_insolation):
        pass

    # to be acquired through API
    def get_cloud_cover(self):
        pass

    def calculate_solar_energy(self):
        pass


