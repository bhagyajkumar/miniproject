from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, validators, TextAreaField, SelectMultipleField, SelectField
from wtforms.widgets import CheckboxInput, ListWidget
from .models import Project, Role, Tag
from app.auth.models import User


class PostForm(FlaskForm):
    title = StringField("Title", validators=[validators.DataRequired()])
    description = TextAreaField("Description", validators=[validators.DataRequired()])
    tags = SelectMultipleField('Tags', 
                               choices=[],
                               option_widget=CheckboxInput(),
                               widget=ListWidget(prefix_label=False)
                             )

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.tags.choices = [(tag.id, tag.tag_name) for tag in Tag.query.all()]
        
class TicketForm(FlaskForm):
    description = TextAreaField("Description", validators=[validators.DataRequired()])


class AssignTicketForm(FlaskForm):
    # all users from that project
    assignee = SelectField("Assignee", choices=[])

    def __init__(self, project_id, *args, **kwargs):
        super(AssignTicketForm, self).__init__(*args, **kwargs)
        project = Project.query.get(project_id)
        project_users = project.users if project.users else []
        self.assignee.choices = [(user.id, user.email) for user in project_users]
        self.assignee.choices.insert(0,("", "Unassigned"))


class CreateRoleForm(FlaskForm):
    role_name = StringField("Role Name", validators=[validators.DataRequired()])
    


class CreateProjectForm(FlaskForm):
    title = StringField("Title", validators=[validators.DataRequired()])
    description = TextAreaField("Description", validators=[validators.DataRequired()])

class AddUserToProjectForm(FlaskForm):
    email = EmailField("Email", validators=[validators.DataRequired()])


class AddUserToRoleForm(FlaskForm):
    user = SelectField("Member", choices=[], validators=[validators.DataRequired()])

    def __init__(self, project_id,role_id, *args, **kwargs):
        super(AddUserToRoleForm, self).__init__(*args, **kwargs)
        project = Project.query.get(project_id)
        role = Role.query.get(role_id)
        project_users = project.users if project.users else []
        for i,j in enumerate(project_users):
            if j in role.users:
                project_users.pop(i)
        self.user.choices = [(user.id, user.email) for user in project_users]