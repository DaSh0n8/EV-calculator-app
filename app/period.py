from datetime import date, time, datetime, timedelta

DAY_START = time(0)
DAY_END = time(23, 59, 59)
PEAK_START = time(6)
PEAK_END = time(18)


def minus_time(lhs: time, rhs: time) -> timedelta:
    d = datetime.now()
    return datetime(d.year, d.month, d.day, lhs.hour, lhs.minute, lhs.second) - \
           datetime(d.year, d.month, d.day, rhs.hour, rhs.minute, rhs.second)


class Period:
    def __init__(self, day: date, start: time, end: time):
        self.day = day
        self.start = start
        self.end = end
        assert start < end

    @property
    def base_price(self) -> int:
        # TODO: change this to base_price_factor if price is based on charger configuration
        return 100 if self.is_peak else 50

    @property
    def surcharge_factor(self) -> float:
        return 1.1 if self.is_surcharge_day else 1

    @property
    def is_peak(self):
        return PEAK_START <= self.start <= PEAK_END \
               or PEAK_START <= self.end <= PEAK_END \
               or (self.start < PEAK_START and PEAK_END < self.end)

    @property
    def is_surcharge_day(self):
        return self.__is_weekday() or self.__is_holiday()

    @staticmethod
    def __is_peak(start: time, end: time) -> bool:
        return PEAK_START <= start <= PEAK_END \
               or PEAK_START <= end <= PEAK_END \
               or (start < PEAK_START and PEAK_END < end)

    def __is_weekday(self) -> bool:
        return self.day.weekday() < 5

    def __is_holiday(self) -> bool:
        # TODO: handle public & school holidays
        return False


def to_datetime(d: date, t: time) -> datetime:
    return datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)


def split_by_day(start: datetime, end: datetime) -> [Period]:
    assert start <= end
    if start.date() == end.date():
        return [Period(start.date(), start.time(), end.time())]

    end_of_a = to_datetime(start.date(), DAY_END)
    return [Period(start.date(), start.time(), end_of_a.time())] + split_by_day(end_of_a + timedelta(seconds=1), end)


BEFORE_PEAK = (to_datetime(date.today(), PEAK_START) - timedelta(seconds=1)).time()
AFTER_PEAK = (to_datetime(date.today(), PEAK_END) + timedelta(seconds=1)).time()


def split_into_distinct_peak_periods(period: Period) -> [Period]:
    """Splits the (start, end) period such into distinct non-overlapping peak and non-peak periods"""
    start = period.start
    end = period.end

    def P(s: time, e: time) -> Period:
        return Period(period.day, s, e)

    # Case 1: period is outside of peak timing
    if end < PEAK_START or PEAK_END < start:
        return [P(start, end)]

    # Case 2: period starts prior to peak
    if start < PEAK_START:
        pre = P(start, BEFORE_PEAK)
        # Case 2.1: ends during peak
        if end < PEAK_END:
            return [pre, P(PEAK_START, end)]
        # Case 2.2: ends after peak
        else:
            return [pre, P(PEAK_START, PEAK_END), P(AFTER_PEAK, end)]
    # Case 3: period starts during peak
    else:
        # Case 3.1: ends during peak
        if end < PEAK_END:
            return [P(start, end)]
        # Case 3.2: ends after peak
        else:
            return [P(start, PEAK_END), P(AFTER_PEAK, end)]


def split(start: datetime, end: datetime) -> [Period]:
    day_periods: [Period] = split_by_day(start, end)

    distinct_periods = []
    for p in day_periods:
        distinct_periods += split_into_distinct_peak_periods(p)

    return distinct_periods
