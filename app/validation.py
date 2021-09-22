from datetime import date, time

from wtforms import ValidationError

CHARGER_CONFIGS = ["1", "2", "3", "4", "5", "6", "7", "8"]


def is_positive_number(n: int):
    return isinstance(n, int) and n > 0


def is_percent(n: int):
    return isinstance(n, int) and 0 <= n <= 100


class BatteryCapacity:
    NotPositiveInteger = ValidationError("Battery capacity must be a positive integer")

    def validate(value: int) -> int:
        if not is_positive_number(value):
            raise BatteryCapacity.NotPositiveInteger
        return value


class InitialCharge:
    NotPercentage = ValidationError("Initial charge must be a percentage [0,100]")
    GreaterThanFinalCharge = ValidationError("Initial charge must be <= final charge")

    def validate(value: int, final_charge: int) -> int:
        if not is_percent(value):
            raise InitialCharge.NotPercentage
        if value > final_charge:
            raise InitialCharge.GreaterThanFinalCharge
        return value


class FinalCharge:
    NotPercentage = ValidationError("Final charge must be a percentage [0,100]")
    LessThanInitialCharge = ValidationError("Final charge must be >= final charge")

    def validate(value: int, initial_charge: int) -> int:
        if not is_percent(value):
            raise FinalCharge.NotPercentage
        if value < initial_charge:
            raise FinalCharge.LessThanInitialCharge
        return value


class StartDate:
    NotValidDate = ValidationError("Start date must be a valid date")

    def validate(value: date) -> date:
        if not isinstance(value, date):
            raise StartDate.NotValidDate
        return value


class StartTime:
    NotValidTime = ValidationError("Start time must be a valid time")

    def validate(value: time) -> time:
        if not isinstance(value, time):
            raise StartTime.NotValidTime
        return value


class ChargerConfiguration:
    Invalid = ValidationError(f"Charger configuration must be one of: {CHARGER_CONFIGS}")

    def validate(value: str) -> str:
        if not (isinstance(value, str) and value in CHARGER_CONFIGS):
            raise ChargerConfiguration.Invalid
        return value


class PostCode:
    NotPositiveInteger = ValidationError("Post code must be a positive integer")

    def validate(value: int) -> int:
        if not is_positive_number(value):
            raise ValidationError("Post code must be a positive integer")
        return value
