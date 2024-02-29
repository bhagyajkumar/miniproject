from app.ext import admin
from flask_admin.contrib.sqla import ModelView

class TagAdminView(ModelView):
    column_display_pk = True