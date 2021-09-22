from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, IntegerField, SelectField, validators
from wtforms.validators import DataRequired, ValidationError, Optional
from .validation import *


# validation for form inputs
class CalculatorForm(FlaskForm):
    # this variable name needs to match with the input attribute name in the html file
    # you are NOT ALLOWED to change the field type, however, you can add more built-in validators and custom messages
    capacity = IntegerField("Battery Pack Capacity", [DataRequired("Battery Pack Capacity is required")])
    initial_charge = IntegerField("Initial Charge", [DataRequired("Initial Charge is required")])
    final_charge = IntegerField("Final Charge", [DataRequired("Final Charge is required")])
    start_date = DateField("Start Date", [DataRequired("Start Date is required")])
    start_time = TimeField("Start Time", [DataRequired("Start Time is required")])
    charger_config = SelectField("Charger Configuration",
                                 [DataRequired("Charger Configuration is required")],
                                 choices=CHARGER_CONFIGS)
    post_code = IntegerField("Post Code", [DataRequired("Post Code is required")])

    # use validate_ + field_name to activate the flask-wtforms built-in validator
    def validate_capacity(self, field: IntegerField):
        Capacity.validate(field.data)

    def validate_initial_charge(self, field: IntegerField):
        InitialCharge.validate(field.data, self.final_charge.data)

    def validate_final_charge(self, field: IntegerField):
        FinalCharge.validate(field.data, self.initial_charge.data)

    def validate_start_date(self, field: DateField):
        StartDate.validate(field.data)

    def validate_start_time(self, field: TimeField):
        StartTime.validate(field.data)

    def validate_charger_config(self, field: SelectField):
        ChargerConfig.validate(field.data)

    def validate_post_code(self, field: IntegerField):
        PostCode.validate(field.data)
