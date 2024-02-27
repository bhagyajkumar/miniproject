from . import auth as view
from .forms import LoginForm, SignupForm
from flask import render_template, flash, redirect, url_for
from .models import User
from ..ext import bcrypt, db
from sqlalchemy.exc import IntegrityError

@view.route("/")
def test():
    return "auth"

@view.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        try:
            password_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(email=form.email.data, password_hash=password_hash)
            

            db.session.add(user)
            db.session.commit()
            
            flash("Account created successfully! You can now login.", "success")
            

            return redirect(url_for("login"))
        except IntegrityError:
            db.session.rollback()
            flash("Email already exists. Please use a different email.", "danger")

    return render_template("auth/signup.html", form=form)

@view.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            flash('Login successful!', 'success')
            return redirect("/")
        else:
            flash('Invalid email or password', 'danger')
    return render_template('auth/login.html', form=form)