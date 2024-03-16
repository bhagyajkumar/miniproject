from app.ext import admin
from flask_admin.contrib.sqla import ModelView
from .models import Tag, ProjectPost, ProjectApplication
from app.ext import db
from app.auth.models import User

class TagAdminView(ModelView):
    column_display_pk = True

class ProjectPostAdminView(ModelView):
    column_display_pk = True
    column_exclude_list = ('created_at', 'updated_at')
    form_excluded_columns = ('created_at', 'updated_at')
    form_ajax_refs = {
        'tags': {
            'fields': (Tag.tag_name,)
        },
        'user': {
            'fields': (User.email,)
        }
    }

class ApplicationAdminView(ModelView):
    column_display_pk = True
    column_exclude_list = ('created_at',)
    form_excluded_columns = ('created_at',)
    form_ajax_refs = {
        'user': {
            'fields': (User.email,)
        },
        'project_post': {
            'fields': (ProjectPost.title,)
        }
    }

class ProjectAdminView(ModelView):
    column_display_pk = True
    column_exclude_list = ('created_at', 'updated_at')
    form_excluded_columns = ('created_at', 'updated_at')
    form_ajax_refs = {
        'admin': {
            'fields': (User.email,)
        },
        'users': {
            'fields': (User.email,)
        },
        'tags': {
            'fields': (Tag.tag_name,)
        }
    }