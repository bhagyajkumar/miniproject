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

class ChatRoomAdminView(ModelView):
    column_display_pk = True
    column_searchable_list = ['name']  # Add columns you want to search by
    form_columns = ['name', 'project', 'role']  # Add columns you want to include in the form
    

class ChatMessageAdminView(ModelView):
    column_display_pk = True
    column_list = ['text', 'user', 'timestamp', 'chat_room']  # Define columns to display in the list view
    column_searchable_list = ['text', 'user.email']  # Add columns you want to search by
    column_filters = ['timestamp']  # Add filters for columns
    column_sortable_list = ['timestamp']  # Add columns you want to be sortable
    form_columns = ['text', 'user', 'chat_room']  # Add columns you want to include in the form

class TicketAdminView(ModelView):
    column_display_pk = True
    column_list = ['description', 'timestamp', 'project', 'status', 'user']  # Define columns to display in the list view
    column_searchable_list = ['description']  # Add columns you want to search by
    column_filters = ['status', 'timestamp']  # Add filters for columns
    column_sortable_list = ['timestamp', 'status']  # Add columns you want to be sortable
    form_columns = ['description', 'project', 'status']  # Add columns you want to include in the form


class RoleAdminView(ModelView):
    column_display_pk = True
    column_list = ['role_name', 'project', 'users', 'chat_room']  # Define columns to display in the list view
    column_searchable_list = ['role_name']  # Add columns you want to search by
    column_filters = ['project']  # Add filters for columns
    column_sortable_list = ['role_name']  # Add columns you want to be sortable
    form_columns = ['role_name', 'project', 'users', "role_chat_room"]  # Add columns you want to include in the form