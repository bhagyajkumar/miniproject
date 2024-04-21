from flask import Flask, session
from .main import main as main_blueprint, events
from .auth import auth as auth_blueprint
from .ext import db, login_manager, bcrypt, admin, migrate, socketio


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    app.debug = True
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    socketio.init_app(app)
    
    return app