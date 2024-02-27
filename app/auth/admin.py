from flask_admin.contrib.sqla import ModelView, form
from wtforms.fields import PasswordField

from app.ext import bcrypt

class UserAdminView(ModelView):
    column_exclude_list = ('password_hash',)  # Exclude password_hash from displayed columns

    form_extra_fields = {
        'password': PasswordField('Password')  # Use PasswordField for password input in forms
    }

    def on_model_change(self, form, model, is_created):
        model.password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        return super().on_model_change(form, model, is_created)