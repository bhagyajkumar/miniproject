from flask import Blueprint
from .models import User
from app.ext import admin as flask_admin, db
from .admin import UserAdminView

auth = Blueprint("auth", __name__, url_prefix="/auth")

flask_admin.add_view(UserAdminView(User, db.session))

from . import views

