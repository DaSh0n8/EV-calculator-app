from .testsbase import *

DAY = date(2000, 1, 1)


class PeriodCostTests(TestsBase):
    def test_on_peak_without_surcharge(self):
        # Saturday (non-surcharge) during peak hours
        p = Period(date(2021, 9, 4), time(13), time(13, 59, 59))
        cost = Calculator.period_cost(p, charge_kwh=20, price=10, solar_generated=10)
        self.assertEqual(cost, 100)

    def test_on_peak_with_surcharge(self):
        pass

    def test_off_peak_without_surcharge(self):
        pass

    def test_off_peak_with_surcharge(self):
        pass

    def test_zero_charge_period_cost(self):
        p = Period(DAY, time(9), time(9, 5))
        self.assertEqual(Calculator.period_cost(p, 0, 20, 50), 0)

    def test_zero_price_period_cost(self):
        pass


class TotalCostTests(TestsBase):
    def test_config_1_off_peak_without_surcharge_and_without_solar_generation(self):
        # Off peak without surcharge
        day, start_time = date(2021, 9, 4), time(19)
        calc = mock_calc(si=0, sunrise=time(7), sunset=time(15), cc=0)
        total_cost = calc.total_cost(initial_charge=0, final_charge=100, capacity=10, charger_config="1",
                                     start_date=day, start_time=start_time, postcode=3000)
        self.assertAlmostEqual(total_cost, 2.5, 2)
