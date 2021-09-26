import unittest
from app.calculator import *
from app.validation import *
from app.validation import *
from app.period import *
from app.api import MockWeatherApi


def get_calc(si: float = 0, sunrise: time = time(), sunset: time = time(), cc: float = 0) -> Calculator:
    return Calculator(MockWeatherApi(si=si, sunrise=sunrise, sunset=sunset, cloud_cover=cc))


class TestCalculator(unittest.TestCase):

    def __init__(self, method_name='runTest'):
        super().__init__(method_name)
        self.calculator = Calculator()

    def assertValidation(self, expected_exception: Exception, f, *args, **kwargs):
        with self.assertRaises(expected_exception.__class__) as cm:
            f(*args, **kwargs)

        self.assertEqual(cm.exception, expected_exception)

    def test_periods_split_by_hour(self):
        day = date(2000, 1, 1)
        self.assertEqual(split(to_datetime(day, time(1, 30)), to_datetime(day, time(3, 45))), [
            Period(day, time(1, 30), time(1, 59, 59)),
            Period(day, time(2), time(2, 59, 59)),
            Period(day, time(3), time(3, 45)),
        ])

    def test_single_period_charge(self):
        p = Period(date.today(), time(3), time(5))
        self.assertEqual(self.calculator.period_charge(p, 0, 50, timedelta(hours=2)), 50)

    def test_multi_period_charge(self):
        p = Period(date.today(), time(3), time(5))
        self.assertEqual(self.calculator.period_charge(p, 0, 50, timedelta(hours=4)), 25)

    def test_solar_generated(self):
        si, sunrise, sunset = 5.6, time(8), time(16)
        c = get_calc(si=si, sunrise=sunrise, sunset=sunset)
        r = c.solar_generated(Period(date.today(), sunrise, sunset), 1000)
        self.assertEqual(r, si * PANEL_SIZE * PANEL_EFFICIENCY)

    def test_partial_solar_generated(self):
        si, sunrise, sunset = 5.6, time(8), time(16)
        c = get_calc(si=si, sunrise=sunrise, sunset=sunset)
        r = c.solar_generated(Period(date.today(), time(12), sunset), 1000)
        self.assertEqual(r, si * PANEL_SIZE * PANEL_EFFICIENCY / 2)

    def test_battery_capacity1(self):
        self.assertValidation(Capacity.NotPositiveInteger, lambda: Capacity.validate(-1))
        # This is equivalent to
        self.assertValidation(Capacity.NotPositiveInteger, Capacity.validate, -1)

    def test_battery_capacity2(self):
        self.assertTrue(Capacity.validate(5))

    def test_cost(self):
        self.assertEqual(self.calculator.cost_calculation(20, 30, 75, True, True), 8.25)

    def test_functions(self):
        # Valid input
        self.assertEqual(self.battery_test(75), 3.75)
        # Using 0 as input
        self.assertValidation(Capacity.NotPositiveInteger, Capacity.validate, 0)
        # Negative number as input
        self.assertValidation(Capacity.NotPositiveInteger, Capacity.validate, -25)
        # Non-numerical input
        self.assertValidation(Capacity.NotPositiveInteger, Capacity.validate, "abc")

        # INITIAL AND FINAL SOC
        # Off-point value for initial SoC with on-point value for final SoC
        self.assertValidation(InitialCharge.NotPercentage, lambda: InitialCharge.validate(-1, 100))
        # Off-point value for initial SoC with invalid final SoC
        self.assertValidation(InitialCharge.NotPercentage, lambda: InitialCharge.validate(-1, -20))
        # On-point value for initial SoC with off-point value for final SoC
        self.assertValidation(FinalCharge.NotPercentage, lambda: FinalCharge.validate(101, 0))
        # Out-point value for initial SoC and on-point value for final SoC
        self.assertValidation(InitialCharge.NotPercentage, lambda: InitialCharge.validate(120, 100))
        # On-point value for initial SoC and invalid final SoC
        self.assertValidation(FinalCharge.NotPercentage, lambda: FinalCharge.validate("abc", 0))
        # Invalid initial SoC with invalid final SoC
        self.assertValidation(InitialCharge.NotPercentage, lambda: InitialCharge.validate(-30, -50))
        # Off-point value for initial SoC and off-point value for final SoC
        self.assertValidation(InitialCharge.NotPercentage, lambda: InitialCharge.validate(-1, 101))
        # On-point value for initial SoC and on-point value for final SoC
        self.assertEqual(self.soc_test(0, 100), 82.5)
        # Invalid initial SoC with off-point final SoC
        self.assertValidation(InitialCharge.NotPercentage, lambda: InitialCharge.validate(120, 100))

        # TIME AND DATE
        # Description: Pairwise testing for Time and Date inputs
        # Off-peak hour with surcharge
        self.assertEqual(self.time_and_date_test(False, True), 4.125)
        # Off-peak hour with invalid date
        self.assertEqual(self.time_and_date_test(False, "abc"), "Must be either True or False")
        # On-peak hour without surcharge
        self.assertEqual(self.time_and_date_test(True, False), 7.5)
        # Invalid time with surcharge
        self.assertEqual(self.time_and_date_test("asd", True), "Must be either True or False")
        # On-peak hour with invalid date
        self.assertEqual(self.time_and_date_test(True, "aabcs"), "Must be either True or False")
        # Invalid time with invalid date
        self.assertEqual(self.time_and_date_test("abc", "aabcs"), "Must be either True or False")
        # Off-peak hour without surcharge
        self.assertEqual(self.time_and_date_test(False, False), 3.75)
        # On-peak hour with surcharge
        self.assertEqual(self.time_and_date_test(True, True), 8.25)
        # Invalid time without surcharge
        self.assertEqual(self.time_and_date_test("abc", True), "Must be either True or False")

        # Description: Boundary testing for on-peak and off-peak hours
        # Starting one minute before off-peak hours
        # Starting one minute before on-peak hours

        # Description: Boundary testing for days with and without surcharge
        # Starting one minute before day with surcharge
        # Starting one minute before day without surcharge

        # CHARGER CONFIGURATION
        # Description: Using boundary testing for charger configuration
        # Using an off-point value at the beginning of the range
        self.assertValidation(ChargerConfig.Invalid, lambda: ChargerConfig.validate("0"))
        # Using an on-point value at the beginning of the range
        self.assertEqual(self.charger_config_test(1), 3.75)
        # Using an on-point value at the end of the range
        self.assertEqual(self.charger_config_test(8), 0.02142857142857143)
        # Using an off-point value at the end of the range
        self.assertValidation(ChargerConfig.Invalid, lambda: ChargerConfig.validate("9"))
        # Using an in-point value
        self.assertEqual(self.charger_config_test(4), 0.6818181818181818)
        # Using an out-point value
        self.assertValidation(ChargerConfig.Invalid, lambda: ChargerConfig.validate("12"))
        # Using an invalid input
        self.assertValidation(ChargerConfig.Invalid, lambda: ChargerConfig.validate("abc"))

    def battery_test(self, capacity):
        if Capacity.validate(capacity):
            cost = self.calculator.cost_calculation(20, 30, capacity, False, False)
            return cost
        else:
            raise Capacity.NotPositiveInteger

    def time_and_date_test(self, on_peak, surcharge):
        if isinstance(on_peak, bool) and isinstance(surcharge, bool):
            result = self.calculator.cost_calculation(20, 30, 75, on_peak, surcharge)
            return result
        else:
            result = "Must be either True or False"
            return result

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
            result = self.calculator.cost_calculation(initial_state, final_state, 75, True, True)
            return result

    def charger_config_test(self, configuration):
        if configuration == 1:
            power = 2
            time = self.calculator.time_calculation(20, 30, 75, power)
            return time
        elif configuration == 2:
            power = 3.6
            time = self.calculator.time_calculation(20, 30, 75, power)
            return time
        elif configuration == 3:
            power = 7.2
            time = self.calculator.time_calculation(20, 30, 75, power)
            return time
        elif configuration == 4:
            power = 11
            time = self.calculator.time_calculation(20, 30, 75, power)
            return time
        elif configuration == 5:
            power = 22
            time = self.calculator.time_calculation(20, 30, 75, power)
            return time
        elif configuration == 6:
            power = 36
            time = self.calculator.time_calculation(20, 30, 75, power)
            return time
        elif configuration == 7:
            power = 90
            time = self.calculator.time_calculation(20, 30, 75, power)
            return time
        elif configuration == 8:
            power = 350
            time = self.calculator.time_calculation(20, 30, 75, power)
            return time
        else:
            time = "Configuration must be in rage 1-8"
            return time


# you may create test suite if needed
if __name__ == "__main__":
    unittest.main()
