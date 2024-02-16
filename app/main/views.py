from . import main as view
from .models import Test

@view.route("/")
def home():
    return "main"