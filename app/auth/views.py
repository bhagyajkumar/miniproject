from . import auth as view
from .forms import LoginForm, SignupForm
from flask import render_template, flash, redirect, url_for
from .models import User
from ..ext import bcrypt, db
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_user

@view.route("/")
def test():
    return "auth"

@view.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        try:
            password_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(email=form.email.data, password_hash=password_hash, full_name=form.full_name.data)
            

            db.session.add(user)
            db.session.commit()
            
            flash("Account created successfully! You can now login.", "success")
            

            return redirect(url_for("auth.login"))
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
            login_user(user)
            return redirect("/")
        else:
            flash('Invalid email or password', 'danger')
    return render_template('auth/login.html', form=form)


@view.route("/profile")
def profile():
    user = current_user
    return render_template("auth/profile.html", user=user)