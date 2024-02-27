from . import auth as view
from .forms import SignupForm
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
            # Hash the password before storing it
            password_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            
            # Create a new user with the form data
            user = User(email=form.email.data, password_hash=password_hash)
            
            # Add the user to the database
            db.session.add(user)
            db.session.commit()
            
            flash("Account created successfully! You can now login.", "success")
            
            # Redirect to the login page
            return redirect(url_for("login"))
        except IntegrityError:
            db.session.rollback()
            flash("Email already exists. Please use a different email.", "danger")

    # If the form is not submitted or has errors, render the signup template
    return render_template("auth/signup.html", form=form)