from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, SelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget
from .models import Tag


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