from app.ext import socketio, db
from flask_socketio import emit, join_room, leave_room
from ..auth.models import User
from .models import ChatRoom, ChatMessage
from flask import session
from flask_login import current_user

@socketio.on('join_room', namespace='/chat')
def joined(message):
    room = session.get('roomid')
    username = session.get('username')
    print(room, username)
    join_room(room)

@socketio.on('send_message', namespace='/chat')
def chat_message(message):
    roomid = session.get('roomid')
    room = ChatRoom.query.get(roomid)
    user = current_user
    user_id = user.id
    msg = ChatMessage(text=message['message'], user_id=user_id, chat_room=room)
    db.session.add(msg)
    db.session.commit()
    
    emit('message', {'message': message['message'], 'username': user.full_name, 'user_id' :user_id}, room=roomid)

    
    