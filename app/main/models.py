from ..ext import db
from enum import Enum


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    tag_name = db.Column(db.String(30))

    def __repr__(self):
        return self.tag_name


class ProjectPost(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime(), default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    tags = db.relationship(
        'Tag', secondary='project_post_tag', backref='project_posts')
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='project_posts')

    def __repr__(self):
        return self.title[:10]


project_post_tag = db.Table(
    'project_post_tag',
    db.Column('project_post_id', db.Integer(), db.ForeignKey(
        'project_post.id'), primary_key=True),
    db.Column('tag_id', db.Integer(), db.ForeignKey(
        'tag.id'), primary_key=True)
)


class ProjectApplication(db.Model):
    # This model is supposed to be used for users to apply to work on a project
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='project_applications')
    resume_link = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text(), nullable=False)
    project_post_id = db.Column(db.Integer(), db.ForeignKey(
        'project_post.id'), nullable=False)
    project_post = db.relationship('ProjectPost', backref='applications')
    created_at = db.Column(db.DateTime(), default=db.func.now())


class Project(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime(), default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    admin = db.relationship('User', backref='projects')
    users = db.relationship(
        'User', secondary='project_user', backref='user_projects')
    tags = db.relationship(
        'Tag', secondary='project_tag', backref='tag_projects')

    def __repr__(self):
        return self.title[:10]


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    role_name = db.Column(db.String(30), nullable=False)
    project_id = db.Column(db.Integer(), db.ForeignKey(
        'project.id'), nullable=False)
    project = db.relationship('Project', backref='roles')
    users = db.relationship(
        'User', secondary='role_user', backref='user_roles')


role_user = db.Table(
    'role_user',
    db.Column('role_id', db.Integer(), db.ForeignKey(
        'role.id'), primary_key=True),
    db.Column('user_id', db.Integer(), db.ForeignKey(
        'user.id'), primary_key=True)
)

project_user = db.Table(
    'project_user',
    db.Column('project_id', db.Integer(), db.ForeignKey(
        'project.id'), primary_key=True),
    db.Column('user_id', db.Integer(), db.ForeignKey(
        'user.id'), primary_key=True)
)

project_tag = db.Table(
    'project_tag',
    db.Column('project_id', db.Integer(), db.ForeignKey(
        'project.id'), primary_key=True),
    db.Column('tag_id', db.Integer(), db.ForeignKey(
        'tag.id'), primary_key=True)
)


class TicketStatus(Enum):
    UNASSIGNED = 'unassigned'
    ASSIGNED = 'assigned'
    COMPLETED = 'completed'


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship("Project")
    status = db.Column(db.Enum(TicketStatus),
                       default=TicketStatus.UNASSIGNED, nullable=False)
    user = db.relationship('User', backref='tickets')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(
        db.Integer, db.ForeignKey('project.id'), nullable=True)
    project = db.relationship('Project', backref='project_chat_room')
    messages = db.relationship(
        'ChatMessage', backref='chat_room', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)
    role = db.relationship('Role', backref='role_chat_room', uselist=False)


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='messages')
    timestamp = db.Column(db.DateTime, default=db.func.now())
    chat_room_id = db.Column(db.Integer, db.ForeignKey(
        'chat_room.id'), nullable=False)
