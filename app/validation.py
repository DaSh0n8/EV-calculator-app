from datetime import date, time
from wtforms import ValidationError


CHARGER_CONFIGS = ["1", "2", "3", "4", "5", "6", "7", "8"]


def is_positive_number(n: int):
    return isinstance(n, int) and n > 0


def is_percent(n: int):
    return isinstance(n, int) and 0 <= n <= 100


def expect_battery_capacity(value: int):
    if not is_positive_number(value):
        raise ValidationError("Battery capacity must be a positive integer")


def expect_initial_charge(value: int, final_charge: int):
    if not is_percent(value):
        raise ValidationError("Initial charge must be a percentage [0,100]")
    if value > final_charge:
        raise ValidationError("Initial charge must be <= final charge")


def expect_final_charge(value: int, initial_charge: int):
    if not is_percent(value):
        raise ValidationError("Final charge must be a percentage [0,100]")
    if value < initial_charge:
        raise ValidationError("Final charge must be >= final charge")


def expect_start_date(value: date):
    if not isinstance(value, date):
        raise ValidationError("Start date must be a valid date")


def expect_start_time(value: time):
    if not isinstance(value, time):
        raise ValidationError("Start time must be a valid time")


def expect_charger_configuration(value: str):
    if not (isinstance(value, str) and value in CHARGER_CONFIGS):
        raise ValidationError(f"Charger configuration must be one of: {CHARGER_CONFIGS}")


def expect_post_code(value: int):
    if not is_positive_number(value):
        raise ValidationError("Post code must be a positive integer")
