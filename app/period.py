from datetime import date, time, datetime, timedelta


def to_datetime(d: date, t: time) -> datetime:
    return datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)


DAY_START = time(0)
DAY_END = time(23, 59, 59)
PEAK_START = time(6)
PEAK_END = time(18)
BEFORE_PEAK = (to_datetime(date.today(), PEAK_START) - timedelta(seconds=1)).time()
AFTER_PEAK = (to_datetime(date.today(), PEAK_END) + timedelta(seconds=1)).time()

PERIOD_START_AFTER_END = Exception("Period start time must be before the end time")
PERIOD_NOT_THE_SAME_HOUR = Exception("Period start and end time must be within the same hour")


class Period:
    def __init__(self, day: date, start: time, end: time):
        self.day = day
        self.start = start
        self.end = end

        if start > end:
            raise PERIOD_START_AFTER_END
        if start.hour != end.hour:
            raise PERIOD_NOT_THE_SAME_HOUR

    def __eq__(self, o):
        return (self.day, self.start, self.end) == (o.day, o.start, o.end)

    @property
    def base_price_factor(self) -> int:
        return 1 if self.is_peak else 0.5

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
        # TODO: handle public holidays
        return False


def minus_time(lhs: time, rhs: time) -> timedelta:
    d = datetime.now()
    return to_datetime(d, lhs) - to_datetime(d, rhs)


def add_time(t: time, delta: timedelta) -> time:
    """Warning: this function CAN overflow if time + delta > 24 hours"""
    return (to_datetime(date.today(), t) + delta).time()


def split(start: datetime, end: datetime) -> [Period]:
    # Split into hour periods, to make estimating hourly solar generation (with cloud cover) easy
    if start.date() == end.date() and start.hour == end.hour:
        return [Period(start.date(), start.time(), end.time())]

    end_of_hour = time(start.hour, 59, 59)
    next_hour = to_datetime(start.date(), end_of_hour) + timedelta(seconds=1)
    return [Period(start.date(), start.time(), end_of_hour)] + split(next_hour, end)
