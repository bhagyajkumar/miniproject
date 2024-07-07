from . import auth as view
from .forms import LoginForm, SignupForm, AvatarUploadForm, EditProfileForm
from flask import render_template, flash, redirect, url_for, request
from .models import User
from ..ext import bcrypt, db
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_user, login_required, logout_user
from .helpers import allowed_file
from uuid import uuid4

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
@login_required
def profile():
    user = current_user
    posts = user.project_posts
    avatar_form = AvatarUploadForm()

    print(posts)
    return render_template("auth/profile.html", user=user, posts=posts, avatar_form=avatar_form)



@view.route("/profile/avatar/upload", methods=["POST", "GET"])
def upload_avatar():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    form = AvatarUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = "static/avatars/" + str(uuid4()) + "." + file.filename.split(".")[-1]
            file.save("app/" + filename)
            current_user.avatar_url = "/" + filename
            db.session.commit()
            return redirect(url_for("auth.profile"))
        

@view.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    form = EditProfileForm()
    if request.method == "GET":
        form.full_name.data = current_user.full_name
        form.bio.data = current_user.bio
        form.email.data = current_user.email
        form.location.data = current_user.location
    if form.validate_on_submit():
        full_name = form.full_name.data
        bio = form.bio.data
        email = form.email.data
        location = form.location.data
        
        user = User.query.get(current_user.id) 
        
        # Update user's profile
        user.full_name = full_name
        user.bio = bio
        user.email = email
        user.location = location
        
        # Commit changes to the database
        db.session.commit()
        
        # Redirect to profile page or another appropriate page
        return redirect(url_for('auth.profile'))
    return render_template("auth/edit_profile.html", form=form)


@view.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('.login'))