from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.automap import automap_base
from forms import Loginform, RegistrationForm, NewCafeForm, CommentForm, ResetPassword
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config["SECRET_KEY"] = "Jahnavi12345"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Bootstrap(app)
ckeditor = CKEditor(app)

# Base = automap_base()
# Base.prepare(db.engine, reflect=True)
# Cafes = Base.classes.cafe

login_manager = LoginManager()
login_manager.init_app(app)

gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False,
                    use_ssl=False, base_url=None)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    comments = relationship("Comment", back_populates='comment_user')


class Cafes(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    map_url = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String)
    coffee_price = db.Column(db.String)
    likes = db.Column(db.Integer)
    likes_percent = db.Column(db.Float)
    comments = relationship("Comment", back_populates="cafe")


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_user = relationship("Users", back_populates="comments")

    cafe_id = db.Column(db.Integer, db.ForeignKey("cafe.id"))
    cafe = relationship("Cafes", back_populates="comments")
    text = db.Column(db.Text)


db.create_all()


@app.route('/')
def home():
    all_cafes = db.session.query(Cafes).all()
    return render_template("index.html", cafes=all_cafes)


@app.route('/like')
def likes():
    cafes = db.session.query(Cafes).all()
    total_likes = 0
    for cafe in cafes:
        total_likes += cafe.likes
    cafes_id = request.args.get('cafe_id')
    cafe = Cafes.query.get(cafes_id)
    cafe.likes += 1
    cafe.likes_percent = round(cafe.likes / total_likes * 100)
    db.session.commit()
    return redirect(url_for('home'))


@login_required
@app.route("/cafe/<int:cafe_id>", methods=["POST", "GET"])
def cafe(cafe_id):
    form = CommentForm()
    selected_cafe = db.session.query(Cafes).get(cafe_id)
    if form.validate_on_submit():
        new_comment = Comment(text=form.comment_text.data,
                              comment_user=current_user,
                              cafe=selected_cafe
                              )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('cafe', cafe_id=selected_cafe.id))
    return render_template("cafe.html", choosen_cafe=selected_cafe, form=form, current_user=current_user)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if Users.query.filter_by(email=form.email.data).first():
            flash("You've already registered with that email, log in instead!")
            return redirect(url_for('log_in'))
        hash_and_salted_password = generate_password_hash(form.password.data,
                                                          method='pbkdf2:sha256',
                                                          salt_length=8
                                                          )
        new_user = Users(name=form.name.data,
                         email=form.email.data,
                         password=hash_and_salted_password
                         )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template("register.html", form=form, current_user=current_user)


@app.route("/login", methods=["POST", "GET"])
def log_in():
    needed_form = 0
    reset = request.args.get('reset')
    if not reset:
        form = Loginform()
        if form.validate_on_submit():
            entered_email = form.email.data
            entered_password = form.password.data
            user = Users.query.filter_by(email=entered_email).first()
            if not user:
                flash("That email doesn't exists, please make sure that you've been registered!")
            elif not check_password_hash(user.password, entered_password):
                flash("Incorrect Password, please try again!")
            else:
                login_user(user)
                return redirect(url_for('home'))
        return render_template("login.html", form=form, current_user=current_user, needed_form=needed_form)
    else:
        needed_form = 1
        reset_form = ResetPassword()
        if reset_form.validate_on_submit():
            new_pass = reset_form.new_password.data
            retype_pass = reset_form.retype_password.data
            user = Users.query.filter_by(email=reset_form.email.data).first()
            if new_pass == retype_pass:
                if user:
                    hash_and_salted_password = generate_password_hash(retype_pass,
                                                                      method='pbkdf2:sha256',
                                                                      salt_length=8
                                                                      )
                    user.password = hash_and_salted_password
                    db.session.commit()
                    return redirect(url_for('log_in'))
                else:
                    flash("You're not the correct user, please check the mail you've entered!")
            else:
                flash("Please do check if the two passwords are same!")
        return render_template("login.html", reset_form=reset_form, current_user=current_user, needed_form=needed_form)


@app.route("/add-cafe", methods=["POST", "GET"])
def add_cafe():
    form = NewCafeForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to add cafe.")
            return redirect(url_for('log_in'))
        new_cafe = Cafes(name=form.cafe_name.data,
                         map_url=form.map_url.data,
                         img_url=form.img_url.data,
                         location=form.location.data,
                         has_sockets=form.has_sockets.data,
                         has_toilet=form.has_toilet.data,
                         has_wifi=form.has_wifi.data,
                         can_take_calls=form.can_take_calls.data,
                         seats=form.seats.data,
                         coffee_price=form.coffee_price.data
                         )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("new_cafe.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)