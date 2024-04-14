from app.auth.models import User
from . import main as view
from flask import render_template, request, session, redirect, url_for, jsonify, flash
from .models import ChatMessage, ProjectPost, Role, Tag, Ticket, Project, TicketStatus
from .forms import CreateRoleForm, PostForm, TicketForm
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


@view.route("/projects")
def projects():
    projects = Project.query.filter(Project.users.any(id=current_user.id)).all()
    return render_template("pages/projects.html", projects=projects)

@view.route("/projects/<pid>")
def project(pid):
    project = Project.query.get(pid)
    role_creation_form = CreateRoleForm()
    return render_template("pages/project.html", project=project, current_user=current_user, role_creation_form=role_creation_form)

@view.route("/projects/<pid>/roles/<rid>/delete")
def delete_role(pid, rid):
    if current_user != Project.query.get(pid).admin:
        return "You are not authorized to delete roles", 403
    role = Role.query.get(rid)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for("main.project", pid=pid))

@view.route("/projects/<pid>/user/<uid>/remove")
def remove_user_from_project(pid, uid):
    project = Project.query.get(pid)
    if int(project.admin.id) == int(uid):
        flash("You cannot remove the admin from the project")
        return redirect(url_for("main.project", pid=pid))
    if current_user != project.admin:
        return "You are not authorized to remove users from this project", 403
    
    user = User.query.get(uid)
    project.users.remove(user)
    db.session.commit()
    return redirect(url_for("main.project", pid=pid))

@view.route("/projects/<pid>/roles/create", methods=["POST"])
def add_role_to_project(pid):
    form = CreateRoleForm()
    if form.validate_on_submit():
        project = Project.query.get(pid)
        role = Role(role_name=form.role_name.data, project=project)
        db.session.add(role)
        db.session.commit()
        return redirect(url_for("main.project", pid=pid))
    return "Form not valid"

@view.route("/projects/<id>/ticket")
def ticket(id):
    project = Project.query.get(id)
    tickets = Ticket.query.filter_by(project=project).all()   
    is_admin = False
    if current_user == project.admin:
        is_admin = True
    return render_template("pages/ticket.html", tickets=tickets, TicketStatus=TicketStatus, is_admin=is_admin)

@view.route("/projects/<pid>/ticket/<tid>/delete")

def delete_ticket(pid,tid):
    ticket = Ticket.query.get(tid)
    db.session.delete(ticket)
    db.session.commit()
    return redirect(url_for("main.ticket", id=pid))

@view.route("/projects/<id>/ticket/create", methods=["GET", "POST"])
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
