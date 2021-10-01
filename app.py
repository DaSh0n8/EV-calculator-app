from flask import Flask, flash
from flask import render_template
from flask import request
from app.calculator import *

from app.calculatorform import *
import os

CALCULATOR_PAGE = "calculator.html"

App = Flask(__name__)
App.config['SECRET_KEY'] = os.urandom(32)


@App.route('/', methods=['GET', 'POST'])
def operation_result():
    form = CalculatorForm(request.form)

    # validation of the form
    if request.method == "POST" and form.validate():
        capacity: int = form.capacity.data
        initial_charge: int = form.initial_charge.data
        final_charge: int = form.final_charge.data
        start_date: date = form.start_date.data
        start_time: time = form.start_time.data
        charger_config: str = form.charger_config.data
        postcode = form.post_code.data

        calc = Calculator(WeatherApi())

        (power, price) = CHARGER_CONFIGS[charger_config]
        duration: timedelta = Calculator.charging_duration(initial_charge, final_charge, capacity, power)

        cost = calc.total_cost(initial_charge, final_charge, capacity, charger_config, start_date, start_time, postcode)

        return render_template(CALCULATOR_PAGE, calculation_success=True, form=form,
                               cost=f"${cost}", time=str(duration))

    else:
        flash_errors(form)
        return render_template(CALCULATOR_PAGE, calculation_success=False, form=form)


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


if __name__ == '__main__':
    App.run()
