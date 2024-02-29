from flask import Blueprint
from app.ext import admin as fadmin, db
from .admin import TagAdminView
from .models import Tag

main = Blueprint("main", __name__)

fadmin.add_view(TagAdminView(Tag, db.session))

from . import views
