from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign me up!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let me in!")


class ResetPassword(FlaskForm):
    email = StringField("Enter Your Email", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    retype_password = PasswordField("Retype Password", validators=[DataRequired()])
    submit = SubmitField("Change Password")