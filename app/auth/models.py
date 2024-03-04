from ..ext import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), default=db.func.now())
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    last_login = db.Column(db.DateTime(), default=db.func.now())
    is_active = db.Column(db.Boolean(), default=True)
    is_admin = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f"<User {self.email}>"
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

