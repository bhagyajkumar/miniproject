from . import main as view
from flask import render_template
from .models import ProjectPost

@view.route("/")
def home():
    return render_template("index.html")

@view.route("/posts")
def browse_posts():
    posts = ProjectPost.query.all()
    return render_template("posts.html", posts=posts)

@view.route("/posts/tags/<tag>")
def browse_posts_by_tag(tag):
    posts = ProjectPost.query.filter(ProjectPost.tags.any(tag_name=tag)).all()
    return render_template("posts.html", posts=posts, tag=tag)