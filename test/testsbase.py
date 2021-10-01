import unittest
from app.calculator import *
from app.validation import *
from app.period import *
from app.api import MockWeatherApi


def mock_calc(si: float = 0, sunrise: time = time(), sunset: time = time(), cc: float = 0) -> Calculator:
    return Calculator(MockWeatherApi(si=si, sunrise=sunrise, sunset=sunset, cloud_cover=cc))


class TestsBase(unittest.TestCase):
    def __init__(self, method_name='run'):
        super().__init__(method_name)

    def assertValidation(self, expected_exception: Exception, f, *args, **kwargs):
        with self.assertRaises(expected_exception.__class__) as cm:
            f(*args, **kwargs)

        self.assertEqual(cm.exception, expected_exception)
