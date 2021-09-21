import unittest
from app.calculator import *
from app.calculator_form import *


class TestCalculator(unittest.TestCase):

    # you may create more test methods
    # you may add parameters to test methods
    # this is an example

    def test_cost(self):
        self.calculator = Calculator()
        self.assertEqual(self.calculator.cost_calculation(20, 30, 75, True, True), 8.25)


    def test_functions(self):
        self.calculator = Calculator()
        # Valid input
        self.assertEqual(self.calculator.battery_test(75), 3.75)
        # Using 0 as input
        self.assertEqual(self.calculator.battery_test(0), 0)
        # Negative number as input
        self.assertEqual(self.calculator.battery_test(-25), -1.25)
        # Non-numerical input
        # self.assertEqual(self.calculator.battery_test(0), 0)
        # INITIAL AND FINAL SOC
        # Off-point value for initial SoC with on-point value for final SoC
        self.assertEqual(self.calculator.soc_test(-1, 100), "Percentage cannot be lower than 0")
        # Off-point value for initial SoC with invalid final SoC
        self.assertEqual(self.calculator.soc_test(-1, -20), "Percentage cannot be lower than 0")
        # On-point value for initial SoC with off-point value for final SoC
        self.assertEqual(self.calculator.soc_test(0, 101), "Percentage cannot exceed 100")
        # Out-point value for initial SoC and on-point value for final SoC
        self.assertEqual(self.calculator.soc_test(120, 100), "Percentage cannot exceed 100")
        # On-point value for initial SoC and invalid final SoC
        self.assertEqual(self.calculator.soc_test(0, "ab"), "Must be numerical value")
        # Invalid initial SoC with invalid final SoC
        self.assertEqual(self.calculator.soc_test(-30, -50), "Percentage cannot be lower than 0")
        # Off-point value for initial SoC and off-point value for final SoC
        self.assertEqual(self.calculator.soc_test(-1, 101), "Percentage cannot exceed 100")
        # On-point value for initial SoC and on-point value for final SoC
        self.assertEqual(self.calculator.soc_test(0, 100), 82.5)
        # Invalid initial SoC with off-point final SoC
        self.assertEqual(self.calculator.soc_test(120, 101), "Percentage cannot exceed 100")

        # TIME AND DATE
        # Description: Pairwise testing for Time and Date inputs
        # Off-peak hour with surcharge
        self.assertEqual(self.calculator.time_and_date_test(False, True), 4.125)
        # Off-peak hour with invalid date
        self.assertEqual(self.calculator.time_and_date_test(False, "abc"), "Must be either True or False")
        # On-peak hour without surcharge
        self.assertEqual(self.calculator.time_and_date_test(True, False), 7.5)
        # Invalid time with surcharge
        self.assertEqual(self.calculator.time_and_date_test("asd", True), "Must be either True or False")
        # On-peak hour with invalid date
        self.assertEqual(self.calculator.time_and_date_test(True, "aabcs"), "Must be either True or False")
        # Invalid time with invalid date
        self.assertEqual(self.calculator.time_and_date_test("abc", "aabcs"), "Must be either True or False")
        # Off-peak hour without surcharge
        self.assertEqual(self.calculator.time_and_date_test(False, False), 3.75)
        # On-peak hour with surcharge
        self.assertEqual(self.calculator.time_and_date_test(True, True), 8.25)
        # Invalid time without surcharge
        self.assertEqual(self.calculator.time_and_date_test("abc", True), "Must be either True or False")

        # Description: Boundary testing for on-peak and off-peak hours
        # Starting one minute before off-peak hours
        # Starting one minute before on-peak hours

        # Description: Boundary testing for days with and without surcharge
        # Starting one minute before day with surcharge
        # Starting one minute before day without surcharge

        # CHARGER CONFIGURATION
        # Description: Using boundary testing for charger configuration
        # Using an off-point value at the beginning of the range
        self.assertEqual(self.calculator.charger_config_test(0), "Configuration must be in rage 1-8")
        # Using an on-point value at the beginning of the range
        self.assertEqual(self.calculator.charger_config_test(1), 3.75)
        # Using an on-point value at the end of the range
        self.assertEqual(self.calculator.charger_config_test(8), 0.02142857142857143)
        # Using an off-point value at the end of the range
        self.assertEqual(self.calculator.charger_config_test(9), "Configuration must be in rage 1-8")
        # Using an in-point value
        self.assertEqual(self.calculator.charger_config_test(4), 0.6818181818181818)
        # Using an out-point value
        self.assertEqual(self.calculator.charger_config_test(12), "Configuration must be in rage 1-8")
        # Using an invalid input
        self.assertEqual(self.calculator.charger_config_test("asd"), "Configuration must be in rage 1-8")



    # you may create test suite if needed
    if __name__ == "__main__":
        unittest.main()



    # this is required for test suite and run it
