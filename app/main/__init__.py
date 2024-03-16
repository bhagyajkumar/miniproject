from flask import Blueprint
from app.ext import admin as fadmin, db, socketio
from .admin import TagAdminView, ProjectPostAdminView, ApplicationAdminView, ProjectAdminView, ChatRoomAdminView, ChatMessageAdminView
from .models import Tag, ProjectPost, ProjectApplication, Project, ChatRoom, ChatMessage


main = Blueprint("main", __name__)

fadmin.add_view(TagAdminView(Tag, db.session, category="posts and applications"))
fadmin.add_view(ProjectPostAdminView(ProjectPost, db.session, category="posts and applications"))
fadmin.add_view(ApplicationAdminView(ProjectApplication, db.session, category="posts and applications"))
fadmin.add_view(ProjectAdminView(Project, db.session, category="Projects"))
fadmin.add_view(ChatRoomAdminView(ChatRoom, db.session, category="Chat"))
fadmin.add_view(ChatMessageAdminView(ChatMessage, db.session, category="Chat"))

from . import views
from . import events