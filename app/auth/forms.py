from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class SignupForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")
    submit = SubmitField("Sign Up")

    