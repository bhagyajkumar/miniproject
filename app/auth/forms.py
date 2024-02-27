from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

class SignupForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired(), validators.Length(min=8, max=32)])
    submit = SubmitField("Sign Up")

    
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    submit = SubmitField("Login")