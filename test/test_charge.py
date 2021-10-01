from .testsbase import *

DAY = date(2000, 1, 1)


class ChargeDurationTests(TestsBase):
    def test_charging_duration(self):
        self.assertEqual(Calculator.charging_duration(0, 100, 100, 50), timedelta(hours=2))


class ChargeAmount(TestsBase):
    def test_charge_amount(self):
        charge_kwh = Calculator.charge_amount(Period(DAY, time(3), time(3, 30)), 20, 40, timedelta(minutes=30))
        self.assertEqual(charge_kwh, 20)
