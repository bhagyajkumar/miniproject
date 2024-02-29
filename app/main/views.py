from . import main as view
from flask import render_template

@view.route("/")
def home():
    return render_template("index.html")