from ..ext import db

class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    tag_name = db.Column(db.String(30))

    def __repr__(self):
        return self.tag_name
    
    
class ProjectPost(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime(), default=db.func.now())
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    tags = db.relationship('Tag', secondary='project_post_tag', backref='project_posts')
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='project_posts')

project_post_tag = db.Table(
    'project_post_tag',
    db.Column('project_post_id', db.Integer(), db.ForeignKey('project_post.id')),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'))
)
