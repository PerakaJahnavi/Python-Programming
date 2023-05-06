from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime as dt
from forms import LoginForm, RegistrationForm, ResetPasswordForm, DateForm
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship
from flask_login import login_user, LoginManager, logout_user, current_user, UserMixin
import calendar

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///members.db"
app.config["SECRET_KEY"] = "Jahnavi123"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Bootstrap(app)
now = dt.now()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    designation = db.Column(db.String, nullable=False)
    reporting_manager = db.Column(db.String)
    password = db.Column(db.String, nullable=False)


class LoginCheck(db.Model):
    __tablename__ = "login_check"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)


db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    managers = Users.query.filter_by(designation="Manager").all()
    all_manager_list = ["None"]
    for manager in managers:
        all_manager_list.append(manager.name)
    register_form = RegistrationForm(all_managers=all_manager_list)
    if register_form.validate_on_submit():
        user = Users.query.filter_by(email=register_form.email.data).first()
        if user:
            flash("You've already registered with this email, please Login to continue!")
            return redirect(url_for('login'))
        hash_and_salted_password = generate_password_hash(register_form.password.data,
                                                          method='pbkdf2:sha256',
                                                          salt_length=8
                                                          )
        if register_form.check_box.data:
            role = "Manager"

        else:
            role = "Member"

        new_user = Users(name=register_form.name.data,
                         email=register_form.email.data,
                         designation=role,
                         reporting_manager=register_form.selection.data,
                         password=hash_and_salted_password
                         )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template("register.html", form=register_form, form_type="Registration", current_user=current_user)


@app.route('/login', methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Users.query.filter_by(email=login_form.email.data).first()
        entered_password = login_form.password.data
        if not user:
            flash("That email doesn't exists, please make sure that you've been registered!")
            return redirect(url_for('register'))
        elif not check_password_hash(user.password, entered_password):
            flash("Incorrect Password, please try again!")
        else:
            login_user(user)
            if not LoginCheck.query.filter_by(email=login_form.email.data).filter_by(date=now.strftime('%d-%m-%Y')).all():
                new_login = LoginCheck(email=login_form.email.data,
                                       date=now.strftime('%d-%m-%Y')
                                       )
                db.session.add(new_login)
                db.session.commit()
            return redirect(url_for('home'))
    return render_template("register.html", form=login_form, form_type="Login", current_user=current_user)


@app.route('/reset', methods=["POST", "GET"])
def reset_pass():
    reset_form = ResetPasswordForm()
    if reset_form.validate_on_submit():
        user = Users.query.filter_by(email=reset_form.email.data).first()
        if not user:
            flash("This email doesn't exists, please check your email")
        else:
            if reset_form.new_password.data == reset_form.retype_password.data:
                hash_and_salted_password = generate_password_hash(reset_form.new_password.data,
                                                              method='pbkdf2:sha256',
                                                              salt_length=8
                                                              )
                user.password = hash_and_salted_password
                db.session.commit()
                return redirect(url_for('login'))
            else:
                flash("Please do check if the two password are same!")
    return render_template("reset_password.html", form=reset_form)


@app.route('/members')
def members():
    try:
        manager_name = current_user.name
        members = Users.query.filter_by(reporting_manager=manager_name).all()
        return render_template("members.html", current_user=current_user, members=members)
    except AttributeError:
        return redirect(url_for('login'))


@app.route('/presence', methods=["POST", "GET"])
def presence():
    email = request.args.get('email')
    login_days = []
    month_days = []
    login_person = LoginCheck.query.filter_by(email=email).all()
    for day in login_person:
        date = day.date.split("-")
        login_days.append([int(i) for i in date])
    date_form = DateForm()
    if date_form.validate_on_submit():
        year = int(date_form.year.data)
        month = int(date_form.month.data)
        cal = calendar.monthcalendar(year, month)
        for day in login_days:
            if day[1] == month and day[2] == year:
                month_days.append(day[0])
        return render_template("calendar.html", cal=cal, year=year, month=calendar.month_name[month], form=date_form, login_days=month_days)
    cal = calendar.monthcalendar(now.year, now.month)
    for day in login_days:
        if day[1] == int(now.strftime('%m')) and day[2] == now.year:
            month_days.append(day[0])
    return render_template("calendar.html", cal=cal, year=now.year, month=now.strftime("%B"), form=date_form, login_days=month_days)


@app.route('/logout')
def logout():
    logout_user()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
