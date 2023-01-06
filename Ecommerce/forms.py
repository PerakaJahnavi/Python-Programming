from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor


class Loginform(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let me in!")


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign me up!")


class ResetPassword(FlaskForm):
    email = StringField("Enter Your Email", validators=[DataRequired()])
    new_password = PasswordField("New_Password", validators=[DataRequired()])
    retype_password = PasswordField("Retype_Password", validators=[DataRequired()])
    submit = SubmitField("Change Password")