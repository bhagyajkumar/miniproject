from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, FileField, TextAreaField


class SignupForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired()])
    full_name = StringField("Full Name", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired(), validators.Length(min=8, max=32)])
    submit = SubmitField("Sign Up")

    
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    submit = SubmitField("Login")

class AvatarUploadForm(FlaskForm):
    file  = FileField("Upload Avatar", validators=[validators.DataRequired()])
    submit = SubmitField("Upload")

class EditProfileForm(FlaskForm):
    fill_name = StringField("Full Name", validators=[validators.DataRequired()])
    bio = TextAreaField("bio", validators=[validators.data_required()])
    email = StringField("email", validators=[validators.data_required()])
    location = StringField("location", validators=[validators.data_required()])
    

