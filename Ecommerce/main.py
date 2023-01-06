from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, LoginManager, UserMixin, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from forms import RegistrationForm, Loginform, ResetPassword
from sqlalchemy.orm import relationship
import stripe

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecom.db"
app.config["SECRET_KEY"] = "Jahnavi12345"

app.config['STRIPE_SECRET_KEY'] = 'sk_test_51MMvNFSJAtsv4FR25otBmYuCikjlKYTW2rYUANqm7d0FLEeQzDW9JP3jDCXF9cSKKPwhYY4Zuwr3GTDg28CNpeTW00Xsyqvznq'
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51MMvNFSJAtsv4FR2ogbWYXGVgbYatXws6ggBAIG0XaXnCDUtAlQYax30LV9ofP6b1GvH0346qZi5zgseh8VvJIRM00GUtq8xH3'
stripe.api_key = app.config['STRIPE_SECRET_KEY']

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Bootstrap(app)
ckeditor = CKEditor(app)
# stripe_API_Pass = "Teslamusk@2001"
# code = "kyvr-nbdy-woua-hzki-cnvu"
# https://dashboard.stripe.com/stripecli/confirm_auth?t=ojWA8vfWs6UUZFTlJG6qreKVcIboiTcR (^C to quit)
# > Done! The Stripe CLI is configured for Linkedin with account id acct_1MMvNFSJAtsv4FR2

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
    name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=False)
    cart = relationship("Cart", back_populates="cart_user")


class Items(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)
    img_url = db.Column(db.String)
    price = db.Column(db.String)
    item_name = db.Column(db.String)
    item_sub = db.Column(db.String)
    cart = relationship("Cart", back_populates="cart_item")


class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    cart_user = relationship("Users", back_populates="cart")

    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    cart_item = relationship("Items", back_populates="cart")
    name = db.Column(db.String, nullable=False)


db.create_all()


@app.route('/')
def home():
    all_items = db.session.query(Items).all()
    return render_template("index.html", all_items=all_items, current_user=current_user)


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


@app.route('/item/<int:item_id>')
def item(item_id):
    about_item = db.session.query(Items).get(item_id)
    return render_template("item.html", item=about_item)


@app.route('/add')
def add_to_cart():
    if current_user.is_authenticated:
        id = request.args.get('item_id')
        if not Cart.query.filter_by(item_id=id, user_id=current_user.id).first():
            item = db.session.query(Items).get(id)
            new_item = Cart(name=item.item_name,
                            cart_user=current_user,
                            cart_item=item)
            db.session.add(new_item)
            db.session.commit()
            selected_item = Cart.query.filter_by(item_id=id, user_id=current_user.id).first()
            user = selected_item.user_id
            all_items = Cart.query.filter_by(user_id=user).all()
            return render_template("cart.html", all_items=all_items)
        else:
            all_items = Cart.query.filter_by(user_id=current_user.id).all()
            return render_template("cart.html", all_items=all_items)
    else:
        flash("Please do check if you're logged in!")
        return redirect(url_for('log_in'))


@app.route('/cart')
def cart():
    if current_user.is_authenticated:
        all_items = Cart.query.filter_by(user_id=current_user.id).all()
        return render_template("cart.html", all_items=all_items)
    else:
        flash("Please do check if you're logged in!")
        return redirect(url_for('log_in'))


@app.route('/delete-cart-item')
def delete_cart_item():
    id = request.args.get('item_id')
    item = Cart.query.filter_by(user_id=current_user.id, item_id=id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        all_items = Cart.query.filter_by(user_id=current_user.id).all()
        return render_template("cart.html", all_items=all_items)
    else:
        all_items = Cart.query.filter_by(user_id=current_user.id).all()
        return render_template("cart.html", all_items=all_items)


@app.route('/search', methods=["POST"])
def search():
    if request.method == "POST":
        searched_word = request.form["search-bar"]
        items = db.session.query(Items).filter((Items.item_name).like('%' + searched_word + '%')).all()
        return render_template("searched_items.html", all_items=items)


@app.route('/stripe_pay')
def stripe_pay():
    if current_user.is_authenticated:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_1MNBl3SJAtsv4FR2Sm38t0nj',
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('home', _external=True),
        )
        return {
            'checkout_session_id': session['id'],
            'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
        }
    else:
        return redirect(url_for('log_in'))


@app.route('/thanks')
def thanks():
    return render_template("thanks.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)