from .testsbase import *

day = date(2000, 1, 1)


class PeriodTests(TestsBase):
    def test_period_start_time_must_be_less_than_end_time(self):
        self.assertValidation(PERIOD_START_AFTER_END, lambda: Period(day, time(1, 45), time(1, 15)))

    def test_period_start_and_end_time_within_same_hour(self):
        self.assertValidation(PERIOD_NOT_THE_SAME_HOUR, lambda: Period(day, time(2), time(5)))

    def test_periods_split_by_hour(self):
        self.assertEqual(split(to_datetime(day, time(1, 30)), to_datetime(day, time(3, 45))), [
            Period(day, time(1, 30), time(1, 59, 59)),
            Period(day, time(2), time(2, 59, 59)),
            Period(day, time(3), time(3, 45)),
        ])

    def test_peak_when_during(self):
        p = Period(day, PEAK_START, add_time(PEAK_START, timedelta(minutes=50)))
        self.assertEqual(p.is_peak, True)

    # TODO: tests for is_peak, is_surcharge_day, base_price_factor, surcharge_factor etc.
