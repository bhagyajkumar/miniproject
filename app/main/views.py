from app.auth.models import User
from . import main as view
from flask import render_template, request, session, redirect, url_for, jsonify, flash
from .models import ChatMessage, ChatRoom, ProjectPost, Role, Tag, Ticket, Project, TicketStatus
from .forms import AddUserToProjectForm, AssignTicketForm, CreateProjectForm, CreateRoleForm, PostForm, TicketForm, AddUserToRoleForm
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


@view.route("/projects/create", methods=["GET", "POST"])
def create_project():
    form = CreateProjectForm()
    if form.validate_on_submit():
        project = Project(title=form.title.data, description=form.description.data, admin=current_user)
        chat_room = ChatRoom(name=f"{project.title} chat")
        chat_room.project = project
        project.users.append(current_user)
        project.chat_room_id = chat_room.id
        db.session.add(project)
        db.session.commit()
        return redirect(url_for("main.projects"))
    return render_template("pages/create_project.html", form=form)


@view.route("/projects/")
def projects():
    projects = Project.query.filter(Project.users.any(id=current_user.id)).all()
    return render_template("pages/projects.html", projects=projects)



@view.route("/projects/<pid>")
def project(pid):
    project = Project.query.get(pid)
    chat_room = project.project_chat_room
    print(chat_room[0].id)
    role_creation_form = CreateRoleForm()
    user_add_form = AddUserToProjectForm()
    return render_template("pages/project.html", project=project, current_user=current_user, role_creation_form=role_creation_form, user_add_form=user_add_form, chat_room=chat_room[0].id)

@view.route("/projects/<pid>/add-user", methods=["POST"])
def add_user_to_project(pid):
    form = AddUserToProjectForm()
    if form.validate_on_submit():
        project = Project.query.get(pid)
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            project.users.append(user)
            db.session.commit()
            return redirect(url_for("main.project", pid=pid))
        return "User does not exist"
    return "Form not valid"


@view.route("/projects/<int:pid>/roles/<int:rid>/manage-users", methods=["GET","POST"])
def manage_role(pid:int, rid:int):
    
    project = Project.query.get(pid)
    role = Role.query.get(rid)
    form = AddUserToRoleForm(pid,rid)
    if form.validate_on_submit():
        user = User.query.get(form.user.data)
        role.users.append(user)
        db.session.commit()
        return redirect(url_for('main.manage_role', pid=project.id, rid=role.id))
    context = {
        "project": project, 
        "role":role,
        "form":form
    }
    if role is None or project is None:
        return "", 404
    return render_template("pages/manage_members.html", **context)

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
    print(project)
    tickets = Ticket.query.filter_by(project=project).all()
    assign_ticket_form = AssignTicketForm(project_id=id)
    is_admin = False
    if current_user == project.admin:
        is_admin = True
    return render_template("pages/ticket.html", project=project, tickets=tickets, TicketStatus=TicketStatus, is_admin=is_admin, assign_ticket_form=assign_ticket_form)

@view.route("/projects/<pid>/ticket/<tid>/assign", methods=["POST"])
def assign_ticket(pid, tid):
    form = AssignTicketForm(project_id=pid)
    if form.validate_on_submit():
        ticket = Ticket.query.get(tid)
        if form.assignee.data == "Unassigned":
            ticket.user_id = None
            ticket.status = TicketStatus.UNASSIGNED
            db.session.commit()
            return redirect(url_for("main.ticket", id=pid))
        ticket.user_id = form.assignee.data
        ticket.status = TicketStatus.ASSIGNED
        db.session.commit()
        return redirect(url_for("main.ticket", id=pid))
    return "Form not valid"

@view.route("/projects/<pid>/ticket/<tid>/delete")
def delete_ticket(pid,tid):
    ticket = Ticket.query.get(tid)
    db.session.delete(ticket)
    db.session.commit()
    return redirect(url_for("main.ticket", id=pid))

@view.route("/projects/<pid>/ticket/<tid>/complete")
def complete_ticket(pid, tid):
    ticket = Ticket.query.get(tid)
    ticket.status = TicketStatus.COMPLETED
    db.session.commit()
    return redirect(url_for("main.ticket", id=pid))

@view.route("/projects/<pid>/ticket/<tid>/reopen")
def reopen_ticket(pid, tid):
    ticket = Ticket.query.get(tid)
    ticket.status = TicketStatus.UNASSIGNED
    db.session.commit()
    return redirect(url_for("main.ticket", id=pid))

@view.route("/projects/<id>/ticket/create", methods=["GET", "POST"])
def create_ticket(id):
    project = Project.query.get(id)
    ticket_form = TicketForm(project=project)
    if ticket_form.validate_on_submit():
        ticket = Ticket(description=ticket_form.description.data,project=project)
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
