from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime as dt
from forms import LoginForm, RegistrationForm, ResetPassword
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship
from flask_login import login_user, LoginManager, logout_user, current_user, UserMixin
import pandas as pd

app = Flask(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config["SECRET_KEY"] = "Jahnavi12345"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Bootstrap(app)
now = str(dt.now().date())
completed_events = []

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
    password = db.Column(db.String, nullable=False)
    all_list = relationship("TodoList", back_populates="user_name")
    completed_list = relationship("TodoListCompleted", back_populates="user_name")


class TodoList(db.Model):
    __tablename__ = "lists"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_name = relationship("Users", back_populates="all_list")
    date = db.Column(db.String)
    todo_list = db.Column(db.String, nullable=False)


class TodoListCompleted(db.Model):
    __tablename__ = "lists-completed"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_name = relationship("Users", back_populates="completed_list")
    date = db.Column(db.String)
    todo_list = db.Column(db.String, nullable=False)


db.create_all()


@app.route('/')
def home():
    try:
        all_todo = pd.read_sql(db.session.query(TodoList).filter_by(user_id=current_user.id).statement, db.session.bind)
        today_events = all_todo.loc[all_todo['date'] == now]
        return render_template("index.html", today_events=today_events["todo_list"])
    except AttributeError:
        return redirect(url_for('login'))


@app.route('/list', methods=["POST", "GET"])
def all_list():
    try:
        event = request.form['listing'].capitalize()
        new_event = TodoList(user_id=current_user.id,
                             date=now,
                             todo_list=event)
        db.session.add(new_event)
        db.session.commit()
        all_todo = pd.read_sql(db.session.query(TodoList).filter_by(user_id=current_user.id).statement, db.session.bind)
        return redirect(url_for('home', today_events=all_todo['todo_list']))
    except KeyError:
        event = request.args.get('event')
        new_event = TodoList(user_id=current_user.id,
                             date=now,
                             todo_list=event)
        db.session.add(new_event)
        db.session.commit()
        should_delete = TodoListCompleted.query.filter_by(todo_list=event).first()
        db.session.delete(should_delete)
        db.session.commit()
        all_todo = pd.read_sql(db.session.query(TodoList).filter_by(user_id=current_user.id).statement, db.session.bind)
        all_todo_completed = pd.read_sql(db.session.query(TodoListCompleted).filter_by(user_id=current_user.id).statement, db.session.bind)
        return redirect(url_for('create', day_events=all_todo['todo_list'], completed_events=all_todo_completed['todo_list'], date=now))


@app.route('/delete', methods=["POST", "GET"])
def delete_event():
    event_no = request.args.get('event_no')
    event_to_delete = request.args.get('event_to_delete')
    deleted_one = TodoList.query.filter_by(todo_list=event_to_delete).first()
    if event_no == "1":
        completed_event = TodoListCompleted(user_id=current_user.id,
                                            date=now,
                                            todo_list=event_to_delete)
        db.session.add(completed_event)
        db.session.commit()
        db.session.delete(deleted_one)
        db.session.commit()
        all_todo = pd.read_sql(db.session.query(TodoList).filter_by(user_id=current_user.id).statement, db.session.bind)
        all_todo_completed = pd.read_sql(db.session.query(TodoListCompleted).filter_by(user_id=current_user.id).statement, db.session.bind)
        return redirect(url_for('create', day_events=all_todo['todo_list'], completed_events=all_todo_completed['todo_list']))
    else:
        all_todo = pd.read_sql(db.session.query(TodoList).filter_by(user_id=current_user.id).statement, db.session.bind)
        db.session.delete(deleted_one)
        db.session.commit()
        return redirect(url_for('home', today_events=all_todo['todo_list']))


@app.route('/create', methods=["POST", "GET"])
def create():
    if current_user.is_authenticated:
        all_todo = pd.read_sql(db.session.query(TodoList).filter_by(user_id=current_user.id).statement, db.session.bind)
        all_todo_completed = pd.read_sql(db.session.query(TodoListCompleted).filter_by(user_id=current_user.id).statement, db.session.bind)
        today_events = all_todo.loc[all_todo['date'] == now]
        today_completed_events = all_todo_completed.loc[all_todo_completed['date'] == now]
        return render_template("create.html", day_events=today_events['todo_list'], completed_events=today_completed_events['todo_list'], current_user=current_user, date=now)
    else:
        flash("You've to login to create list!")
        return redirect(url_for('login'))


@app.route('/my_list')
def my_list():
    if current_user.is_authenticated:
        all_todo = pd.read_sql(db.session.query(TodoList).filter_by(user_id=current_user.id).statement, db.session.bind)
        all_todo_completed = pd.read_sql(db.session.query(TodoListCompleted).filter_by(user_id=current_user.id).statement, db.session.bind)
        todo = list(all_todo['date'].unique())
        todo_completed = list(all_todo_completed['date'].unique())
        return render_template("list.html", all_days=set(todo + todo_completed))


@app.route('/todos')
def todos():
    day = request.args.get('date')
    all_todo = pd.read_sql(db.session.query(TodoList).filter_by(user_id=current_user.id, date=day).statement, db.session.bind)
    all_todo_completed = pd.read_sql(db.session.query(TodoListCompleted).filter_by(user_id=current_user.id, date=day).statement,db.session.bind)
    return render_template("todos.html", listed_todo=all_todo['todo_list'], completed_events=all_todo_completed['todo_list'], date=day)


@app.route('/register', methods=["POST", "GET"])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        user = Users.query.filter_by(email=register_form.email.data).first()
        if user:
            flash("You've already registered with this email, please Login to continue!")
            return redirect(url_for('login'))
        hash_and_salted_password = generate_password_hash(register_form.password.data,
                                                          method='pbkdf2:sha256',
                                                          salt_length=8
                                                          )
        new_user = Users(name=register_form.name.data,
                         email=register_form.email.data,
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
            return redirect(url_for('home'))
    return render_template("register.html", form=login_form, form_type="Login", current_user=current_user)


@app.route('/reset', methods=["POST", "GET"])
def reset_pass():
    reset_form = ResetPassword()
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


@app.route('/logout')
def logout():
    logout_user()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
