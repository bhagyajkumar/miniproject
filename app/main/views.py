from app.auth.models import User
from . import main as view
from flask import render_template, request, session, redirect, url_for, jsonify
from .models import ChatMessage, ProjectPost, Tag, Ticket, Project, TicketStatus
from .forms import PostForm, TicketForm
from ..ext import db
from flask_login import current_user, login_required
from sqlalchemy import desc

@view.route("/")
def home():
    tag_filter = request.args.get("tag")
    if not tag_filter:
        posts = ProjectPost.query.all()
    else:
        posts = ProjectPost.query.filter(ProjectPost.tags.any(tag_name=tag_filter)).all()
    return render_template("posts.html", posts=posts)
    
@view.route("/view-post/<id>")    
def view_post(id):
    post = ProjectPost.query.get(id)
    print (post)
    return render_template ("pages/viewpost.html", post=post)

@view.route("/posts")
def browse_posts():
    tag_filter = request.args.get("tag")
    if not tag_filter:
        posts = ProjectPost.query.all()
    else:
        posts = ProjectPost.query.filter(ProjectPost.tags.any(tag_name=tag_filter)).all()
    return render_template("posts.html", posts=posts)

@view.route("/posts/tags/<tag>")
def browse_posts_by_tag(tag):
    posts = ProjectPost.query.filter(ProjectPost.tags.any(tag_name=tag)).all()
    return render_template("posts.html", posts=posts, tag=tag)

@view.route("/posts/create", methods=["GET", "POST"])
def create_post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        tag_ids = post_form.tags.data
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        print(tags)
        post = ProjectPost(title=post_form.title.data, description=post_form.description.data, tags=tags, user=current_user)
        db.session.add(post)
        db.session.commit()
        return "post created"
    return render_template("create_post.html", form=post_form)

@view.route("/project/<id>/ticket")
def ticket(id):
    tickets = Ticket.query.filter_by(project=Project.query.get(id)).all()   
   
    return render_template("pages/ticket.html", tickets=tickets, TicketStatus=TicketStatus)

@view.route("/project/<id>/ticket/create", methods=["GET", "POST"])
def create_ticket(id):
    project = Project.query.get(id)
    ticket_form = TicketForm(project=project)
    if ticket_form.validate_on_submit():
        ticket = Ticket(description=ticket_form.description.data, user=User.query.get(ticket_form.user.data), project=project)
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for("main.ticket", id=id))
    return render_template("/pages/create_ticket.html", form=ticket_form)

@view.route("/chat/<roomid>")
@login_required
def chat(roomid):
    session["roomid"] = roomid
    session["username"] = current_user.full_name
    session["chat_user_id"] = current_user.id
    return redirect(url_for("main.chat_room"))

@view.route("/chat")
def chat_room():
    user_id = current_user.id
    return render_template("chat.html", username=session.get("username"), roomid=session.get("roomid"), user_id=user_id)



@view.route("/chat/messages/<roomid>/<lastid>")
def chat_messages_by_last_id(roomid, lastid=None):
    print(current_user)
    messages = ChatMessage.query.filter(ChatMessage.chat_room_id == roomid, ChatMessage.id < lastid)\
                            .order_by(ChatMessage.id.desc())\
                            .limit(10)\
                            .all()
    return jsonify([{"text": message.text, "user": message.user.full_name, "user_id": message.user.id, "timestamp": message.timestamp, "id": message.id} for message in messages])


@view.route("/chat/messages/<roomid>")
def chat_messages(roomid):
    print(current_user)
    latest_messages = ChatMessage.query.filter(ChatMessage.chat_room_id == roomid)\
                                   .order_by(desc(ChatMessage.timestamp))\
                                   .limit(10)\
                                   .all()
    latest_messages.reverse()
    return jsonify([{"text": message.text, "user": message.user.full_name, "user_id": message.user.id,"timestamp": message.timestamp, "id": message.id} for message in latest_messages])
