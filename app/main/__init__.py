from flask import Blueprint
from app.ext import admin as fadmin, db
from .admin import TagAdminView, ProjectPostAdminView
from .models import Tag, ProjectPost

main = Blueprint("main", __name__)

fadmin.add_view(TagAdminView(Tag, db.session))
fadmin.add_view(ProjectPostAdminView(ProjectPost, db.session))

from . import views
