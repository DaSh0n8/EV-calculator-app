from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, IntegerField, SelectField, validators
from wtforms.validators import DataRequired, ValidationError, Optional

CHARGER_CONFIGS = ["1", "2", "3", "4", "5", "6", "7", "8"]


def is_percent(n: int):
    return 0 <= n <= 100


# validation for form inputs
class CalculatorForm(FlaskForm):
    # this variable name needs to match with the input attribute name in the html file
    # you are NOT ALLOWED to change the field type, however, you can add more built-in validators and custom messages
    battery_capacity = IntegerField("Battery Pack Capacity", [DataRequired("Battery Pack Capacity is required")])
    initial_charge = IntegerField("Initial Charge", [DataRequired("Initial Charge is required")])
    final_charge = IntegerField("Final Charge", [DataRequired("Final Charge is required")])
    start_date = DateField("Start Date", [DataRequired("Start Date is required")])
    start_time = TimeField("Start Time", [DataRequired("Start Time is required")])
    charger_configuration = SelectField("Charger Configuration", [DataRequired("Charger Configuration is required")],
                                        choices=CHARGER_CONFIGS)
    post_code = IntegerField("Post Code", [DataRequired("Post Code is required")])

    # use validate_ + field_name to activate the flask-wtforms built-in validator
    def validate_battery_capacity(self, field):
        if field.data is None or field.data == "":
            raise ValidationError("Value is empty")
        if not field.data > 0:
            raise ValidationError("Capacity must be > 0")

    # validate initial charge here
    def validate_initial_charge(self, field):
        # another example of how to compare initial charge with final charge
        # you may modify this part of the code
        if field.data > self.final_charge.data:
            raise ValueError("Initial charge data error")

    # validate final charge here
    def validate_final_charge(self, field):
        pass

    # validate start date here
    def validate_start_date(self, field):
        pass

    # validate start time here
    def validate_start_time(self, field):
        pass

    # validate charger configuration here
    def validate_charger_configuration(self, field):
        pass

    # validate postcode here
    def validate_post_code(self, field):
        pass
