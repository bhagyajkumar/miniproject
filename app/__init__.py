from flask import Flask
from .main import main as main_blueprint
from .ext import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.cfg")
    app.register_blueprint(main_blueprint)
    db.init_app(app)
    login_manager.init_app(app)

    return app