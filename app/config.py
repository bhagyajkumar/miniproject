import os
from dotenv import load_dotenv

load_dotenv()


SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///app.db'
SECRET_KEY=os.environ.get('SECRET_KEY') or "secret"
DEBUG=True
FLASK_ADMIN_SWATCH='cosmo'