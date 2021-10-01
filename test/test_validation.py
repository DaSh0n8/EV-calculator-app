from .testsbase import *


class ValidationTests(TestsBase):
    def test_battery(self):
        # Valid input
        self.assertTrue(Capacity.validate(5))
        # Using 0 as input
        self.assertValidation(Capacity.NotPositiveInteger, Capacity.validate, 0)
        # Negative number as input
        self.assertValidation(Capacity.NotPositiveInteger, Capacity.validate, -25)
        # Non-numerical input
        self.assertValidation(Capacity.NotPositiveInteger, Capacity.validate, "abc")

    def test_soc(self):
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
        # self.assertEqual(self.soc_test(0, 100), 82.5)
        # Invalid initial SoC with off-point final SoC
        self.assertValidation(InitialCharge.NotPercentage, lambda: InitialCharge.validate(120, 100))

    def test_charger_config(self):
        # CHARGER CONFIGURATION
        # Description: Using boundary testing for charger configuration
        # Using an off-point value at the beginning of the range
        self.assertValidation(ChargerConfig.Invalid, lambda: ChargerConfig.validate("0"))
        # Using an on-point value at the beginning of the range

        # Using an on-point value at the end of the range

        # Using an off-point value at the end of the range
        self.assertValidation(ChargerConfig.Invalid, lambda: ChargerConfig.validate("9"))
        # Using an in-point value

        # Using an out-point value
        self.assertValidation(ChargerConfig.Invalid, lambda: ChargerConfig.validate("12"))
        # Using an invalid input
        self.assertValidation(ChargerConfig.Invalid, lambda: ChargerConfig.validate("abc"))

    def test_postcode(self):
        self.assertTrue(PostCode.validate(3000))
        self.assertValidation(PostCode.NotPositiveInteger, lambda: PostCode.validate(0))
        self.assertValidation(PostCode.InvalidDigits, lambda: PostCode.validate(10000))
