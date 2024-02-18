from flask import Blueprint
from .models import User

auth = Blueprint("auth", __name__, url_prefix="/auth")

from . import views

