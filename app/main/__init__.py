from flask import Blueprint
from app.ext import admin as fadmin, db
from .admin import TagAdminView, ProjectPostAdminView, ApplicationAdminView
from .models import Tag, ProjectPost, ProjectApplication

main = Blueprint("main", __name__)

fadmin.add_view(TagAdminView(Tag, db.session, category="posts and applications"))
fadmin.add_view(ProjectPostAdminView(ProjectPost, db.session, category="posts and applications"))
fadmin.add_view(ApplicationAdminView(ProjectApplication, db.session, category="posts and applications"))

from . import views
