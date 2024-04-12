from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, SelectMultipleField, SelectField
from wtforms.widgets import CheckboxInput, ListWidget
from .models import Tag
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
    desctiption = TextAreaField("Description", validators=[validators.DataRequired()])
    user = SelectField ('User',
                        choices=[]
                        )
    
    def __init__(self, project, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.user.choices = [(user.id, user.full_name) for user in project.users]