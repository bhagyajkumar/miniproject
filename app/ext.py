from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin, AdminIndexView
from flask_migrate import Migrate
from flask_socketio import SocketIO

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
admin = Admin(name="U-Connect",index_view=AdminIndexView(name="U-Admin", template="admin/index.html"),template_mode="bootstrap4")
migrate = Migrate()
socketio = SocketIO()