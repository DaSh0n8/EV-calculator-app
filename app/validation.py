import math
from datetime import date, time

from wtforms import ValidationError

CHARGER_CONFIGS = {
    "1": 2,  # $0.05     FACTOR IN THE CHARGER CONFIG PRICE?
    "2": 3.6,  # 0.075
    "3": 7.2,  # 0.1
    "4": 11,  # 0.125
    "5": 22,  # 0.15
    "6": 36,  # 0.2
    "7": 90,  # 0.3
    "8": 350,  # 0.5
}


def is_positive_number(n: int):
    return isinstance(n, int) and n > 0


def is_percent(n: int):
    return isinstance(n, int) and 0 <= n <= 100


def validate(**kwargs):
    if "capacity" in kwargs:
        Capacity.validate(kwargs.get("capacity"))
    if "initial_charge" in kwargs:
        InitialCharge.validate(kwargs.get("initial_charge"), kwargs.get("final_charge"))
    if "final_charge" in kwargs:
        FinalCharge.validate(kwargs.get("final_charge"), kwargs.get("initial_charge"))
    if "start_date" in kwargs:
        StartDate.validate(kwargs.get("start_date"))
    if "start_time" in kwargs:
        StartTime.validate(kwargs.get("start_time"))
    if "charger_config" in kwargs:
        ChargerConfig.validate(kwargs.get("charger_config"))
    if "postcode" in kwargs:
        PostCode.validate(kwargs.get("postcode"))


class Capacity:
    NotPositiveInteger = ValidationError("Battery capacity must be a positive integer")

    @staticmethod
    def validate(value: int) -> bool:
        if not is_positive_number(value):
            raise Capacity.NotPositiveInteger
        return True


class InitialCharge:
    NotPercentage = ValidationError("Initial charge must be a percentage [0,100]")
    GreaterThanFinalCharge = ValidationError("Initial charge must be <= final charge")

    @staticmethod
    def validate(value: int, final_charge: int) -> bool:
        if not is_percent(value):
            raise InitialCharge.NotPercentage
        if not is_percent(final_charge):
            raise FinalCharge.NotPercentage
        if value > final_charge:
            raise InitialCharge.GreaterThanFinalCharge
        return True


class FinalCharge:
    NotPercentage = ValidationError("Final charge must be a percentage [0,100]")
    LessThanInitialCharge = ValidationError("Final charge must be >= initial charge")

    @staticmethod
    def validate(value: int, initial_charge: int) -> bool:
        if not is_percent(value):
            raise FinalCharge.NotPercentage
        if not is_percent(initial_charge):
            raise InitialCharge.NotPercentage
        if value < initial_charge:
            raise FinalCharge.LessThanInitialCharge
        return True


class StartDate:
    NotValidDate = ValidationError("Start date must be a valid date")

    @staticmethod
    def validate(value: date) -> bool:
        if not isinstance(value, date):
            raise StartDate.NotValidDate
        return True


class StartTime:
    NotValidTime = ValidationError("Start time must be a valid time")

    @staticmethod
    def validate(value: time) -> bool:
        if not isinstance(value, time):
            raise StartTime.NotValidTime
        return True


class ChargerConfig:
    Invalid = ValidationError(f"Charger configuration must be one of: {CHARGER_CONFIGS}")

    @staticmethod
    def validate(value: str) -> bool:
        if not (isinstance(value, str) and value in CHARGER_CONFIGS):
            raise ChargerConfig.Invalid
        return True


class PostCode:
    NotPositiveInteger = ValidationError("Post code must be a positive integer")
    InvalidDigits = ValidationError("Post code must be [2,4] digits")

    @staticmethod
    def validate(value: int) -> bool:
        if not is_positive_number(value):
            raise PostCode.NotPositiveInteger

        # All Australian postcodes are [2,4] digits; source: https://en.wikipedia.org/wiki/Postcodes_in_Australia
        digits = int(math.log10(value)) + 1
        if not 2 <= digits <= 4:
            raise PostCode.InvalidDigits

        return True
