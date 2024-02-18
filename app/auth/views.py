from . import auth as view
from .forms import SignupForm
from flask import render_template

@view.route("/")
def test():
    return "auth"

@view.route("/signup",methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        return "Form submitted" # handle signup here
    return render_template("auth/signup.html", form=form)

