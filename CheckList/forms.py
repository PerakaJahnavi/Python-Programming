from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime as dt
now = dt.now()


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    check_box = BooleanField("Manager")
    selection = SelectField("Manager Field", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        managers = kwargs.pop('all_managers')
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.selection.choices = [manager for manager in managers]


class DateForm(FlaskForm):
    year = SelectField("Year", choices=[year for year in range(1976, now.year + 1)])
    month = SelectField("Month", choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    submit = SubmitField("Submit")


class ResetPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    new_password = PasswordField("New_Password", validators=[DataRequired()])
    retype_password = PasswordField("Retype_Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
