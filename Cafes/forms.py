from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class Loginform(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let me in!")


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign me up!")


class NewCafeForm(FlaskForm):
    cafe_name = StringField("Name", validators=[DataRequired()])
    map_url = StringField("Map_url", validators=[DataRequired(), URL()])
    img_url = StringField("Img_url", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = BooleanField("Has_sockets")
    has_toilet = BooleanField("Has_toilet")
    has_wifi = BooleanField("Has_wifi")
    can_take_calls = BooleanField("Can_take_calls")
    seats = StringField("Seats")
    coffee_price = StringField("Coffee_price (in form of £2.40)", validators=[DataRequired()])
    submit = SubmitField("Add cafe")


class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")


class ResetPassword(FlaskForm):
    email = StringField("Enter Your Email", validators=[DataRequired()])
    new_password = PasswordField("New_Password", validators=[DataRequired()])
    retype_password = PasswordField("Retype_Password", validators=[DataRequired()])
    submit = SubmitField("Change Password")