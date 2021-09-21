from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, IntegerField, SelectField, validators
from wtforms.validators import DataRequired, ValidationError, Optional
from .validation import *


# validation for form inputs
class CalculatorForm(FlaskForm):
    # this variable name needs to match with the input attribute name in the html file
    # you are NOT ALLOWED to change the field type, however, you can add more built-in validators and custom messages
    battery_capacity = IntegerField("Battery Pack Capacity", [DataRequired("Battery Pack Capacity is required")])
    initial_charge = IntegerField("Initial Charge", [DataRequired("Initial Charge is required")])
    final_charge = IntegerField("Final Charge", [DataRequired("Final Charge is required")])
    start_date = DateField("Start Date", [DataRequired("Start Date is required")])
    start_time = TimeField("Start Time", [DataRequired("Start Time is required")])
    charger_configuration = SelectField("Charger Configuration",
                                        [DataRequired("Charger Configuration is required")],
                                        choices=CHARGER_CONFIGS)
    post_code = IntegerField("Post Code", [DataRequired("Post Code is required")])

    # use validate_ + field_name to activate the flask-wtforms built-in validator
    def validate_battery_capacity(self, field: IntegerField):
        expect_battery_capacity(field.data)

    def validate_initial_charge(self, field: IntegerField):
        expect_initial_charge(field.data, self.final_charge.data)

    def validate_final_charge(self, field: IntegerField):
        expect_final_charge(field.data, self.initial_charge.data)

    def validate_start_date(self, field: DateField):
        expect_start_date(field.data)

    def validate_start_time(self, field: TimeField):
        expect_start_time(field.data)

    def validate_charger_configuration(self, field: SelectField):
        expect_charger_configuration(field.data)

    def validate_post_code(self, field: IntegerField):
        expect_post_code(field.data)
