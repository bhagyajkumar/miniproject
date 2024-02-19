from . import auth as view
from .forms import SignupForm
from flask import render_template
from .models import User
from ..ext import bcrypt, db

@view.route("/")
def test():
    return "auth"

@view.route("/signup",methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(email=form.email.data, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return "User created!"
    return render_template("auth/signup.html", form=form)

