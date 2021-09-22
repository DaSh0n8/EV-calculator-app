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
        # if valid, create calculator to calculate the time and cost
        calculator = Calculator()

        # extract information from the form
        capacity = form.capacity.data
        initial_charge = form.initial_charge.data
        final_charge = form.final_charge.data
        start_date = form.start_date.data
        start_time = form.start_time.data
        charger_config = form.charger_config.data

        # you may change the logic as your like
        duration = calculator.get_duration(start_time)

        is_peak = calculator.is_peak()

        if is_peak:
            peak_period = calculator.peak_period(start_date)

        is_holiday = calculator.is_holiday(start_date)

        # cost = calculator.cost_calculation(initial_charge, final_charge, battery_capacity, is_peak, is_holiday)

        # time = calculator.time_calculation(initial_charge, final_charge, battery_capacity, power)

        # you may change the return statement also

        # values of variables can be sent to the template for rendering the webpage that users will see
        # return render_template('calculator.html', cost = cost, time = time, calculation_success = True, form = form)
        return render_template(CALCULATOR_PAGE, calculation_success=True, form=form)

    else:
        # battery_capacity = request.form['BatteryPackCapacity']
        # flash(battery_capacity)
        # flash("something went wrong")
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
