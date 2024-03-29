from .testsbase import *

past_date = date(2008, 7, 1)
future_date = date(2024, 7, 1)

class SolarTests(TestsBase):
    # solar generated test for past dates
    def test_solar_generated_without_cloud_cover_req2(self):
        si, sunrise, sunset = 5.6, time(8), time(8, 59, 59)
        c = mock_calc(si=si, sunrise=sunrise, sunset=sunset)
        r = c.solar_generated(Period(past_date, sunrise, sunset), 1000)

        # Almost equal is required due to floating point operations
        self.assertAlmostEqual(r, si * PANEL_SIZE * PANEL_EFFICIENCY, 2)

    def test_partial_solar_generated_without_cloud_cover_req2(self):
        si, sunrise, sunset = 5.6, time(8), time(10)
        c = mock_calc(si=si, sunrise=sunrise, sunset=sunset)
        r = c.solar_generated(Period(past_date, time(8), time(8, 59, 59)), 1000)
        self.assertAlmostEqual(r, si * PANEL_SIZE * PANEL_EFFICIENCY / 2, 1)

    def test_solar_generated_with_cloud_cover_req2(self):
        si, cc, sunrise, sunset = 5.6, 0.5, time(8), time(8, 59, 59)
        c = mock_calc(si=si, cc=cc, sunrise=sunrise, sunset=sunset)
        r = c.solar_generated(Period(past_date, sunrise, sunset), 1000)
        self.assertAlmostEqual(r, si * (1 - cc) * PANEL_SIZE * PANEL_EFFICIENCY, 2)

    def test_partial_solar_generated_with_cloud_cover_req2(self):
        si, cc, sunrise, sunset = 5.6, 0.5, time(8), time(10)
        c = mock_calc(si=si, cc=cc, sunrise=sunrise, sunset=sunset)
        r = c.solar_generated(Period(past_date, time(8), time(8, 59, 59)), 1000)
        self.assertAlmostEqual(r, si * (1 - cc) * PANEL_SIZE * PANEL_EFFICIENCY / 2, 1)

    def test_solar_generated_without_cloud_cover_current_date(self):
        si, sunrise, sunset = 5.6, time(8), time(8, 59, 59)
        c = mock_calc(si=si, sunrise=sunrise, sunset=sunset)
        r = c.solar_generated(Period(date.today(), sunrise, sunset), 1000)
        self.assertAlmostEqual(r, si * PANEL_SIZE * PANEL_EFFICIENCY, 2)

    def test_partial_solar_generated_without_cloud_cover_current_date(self):
        si, sunrise, sunset = 5.6, time(8), time(10)
        c = mock_calc(si=si, sunrise=sunrise, sunset=sunset)
        r = c.solar_generated(Period(date.today(), time(8), time(8, 59, 59)), 1000)
        self.assertAlmostEqual(r, si * PANEL_SIZE * PANEL_EFFICIENCY / 2, 1)

    def test_solar_generated_with_cloud_cover_current_date(self):
        si, cc, sunrise, sunset = 5.6, 0.5, time(8), time(8, 59, 59)
        c = mock_calc(si=si, cc=cc, sunrise=sunrise, sunset=sunset)
        r = c.solar_generated(Period(date.today(), sunrise, sunset), 1000)
        self.assertAlmostEqual(r, si * (1 - cc) * PANEL_SIZE * PANEL_EFFICIENCY, 2)

    def test_partial_solar_generated_with_cloud_cover_current_date(self):
        si, cc, sunrise, sunset = 5.6, 0.5, time(8), time(10)
        c = mock_calc(si=si, cc=cc, sunrise=sunrise, sunset=sunset)
        r = c.solar_generated(Period(date.today(), time(8), time(8, 59, 59)), 1000)
        self.assertAlmostEqual(r, si * (1 - cc) * PANEL_SIZE * PANEL_EFFICIENCY / 2, 1)

    # solar generated test for future dates
    def test_solar_generated_without_cloud_cover_req3(self):
        si, sunrise, sunset = 5.6, time(8), time(8, 59, 59)
        c = mock_calc(si=si, sunrise=sunrise, sunset=sunset)
        r = c.solar_generated(Period(future_date, sunrise, sunset), 1000)
        self.assertAlmostEqual(r, si * PANEL_SIZE * PANEL_EFFICIENCY, 2)

    def test_partial_solar_generated_without_cloud_cover_req3(self):
        si, sunrise, sunset = 5.6, time(8), time(10)
        c = mock_calc(si=si, sunrise=sunrise, sunset=sunset)
        r = c.solar_generated(Period(future_date, time(8), time(8, 59, 59)), 1000)
        self.assertAlmostEqual(r, si * PANEL_SIZE * PANEL_EFFICIENCY / 2, 1)

    def test_solar_generated_with_cloud_cover_req3(self):
        si, cc, sunrise, sunset = 5.6, 0.5, time(8), time(8, 59, 59)
        c = mock_calc(si=si, cc=cc, sunrise=sunrise, sunset=sunset)
        r = c.solar_generated(Period(future_date, sunrise, sunset), 1000)
        self.assertAlmostEqual(r, si * (1 - cc) * PANEL_SIZE * PANEL_EFFICIENCY, 2)

    def test_partial_solar_generated_with_cloud_cover_req3(self):
        si, cc, sunrise, sunset = 5.6, 0.5, time(8), time(10)
        c = mock_calc(si=si, cc=cc, sunrise=sunrise, sunset=sunset)
        r = c.solar_generated(Period(future_date, time(8), time(8, 59, 59)), 1000)
        self.assertAlmostEqual(r, si * (1 - cc) * PANEL_SIZE * PANEL_EFFICIENCY / 2, 1)

    def test_past_years_from_past_date(self):
        years = Calculator.get_past_years(date(2000, 1, 1), 3)
        self.assertEqual(years, [date(2000, 1, 1), date(1999, 1, 1), date(1998, 1, 1)])

    def test_past_years_from_current_date(self):
        years = Calculator.get_past_years(date.today(), 3)
        self.assertEqual(years, [date.today(), date(date.today().year - 1, date.today().month, date.today().day),
                                 date(date.today().year - 2, date.today().month, date.today().day)])

    def test_past_years_from_future_date(self):
        years = Calculator.get_past_years(date(2025, 11, 12), 3)
        self.assertEqual(years, [date(2021, 11, 12), date(2020, 11, 12), date(2019, 11, 12)])

    def test_averaged_solar_insolation(self):
        si, sunrise, sunset = 5.6, time(8), time(8, 59, 59)
        c = mock_calc(si=si, sunrise=sunrise, sunset=sunset)
        r = c.avg_solar_insolation(Period(date.today(), sunrise, sunset), 1000)
        self.assertAlmostEqual(r, 6, 0)

    def test_averaged_cloud_cover(self):
        si, cc, sunrise, sunset = 5.6, 0.5, time(8), time(8, 59, 59)
        c = mock_calc(si=si, sunrise=sunrise, sunset=sunset)
        r = c.avg_cloud_cover(Period(date.today(), sunrise, sunset), 1000)
        self.assertAlmostEqual(r, 0, 0)
