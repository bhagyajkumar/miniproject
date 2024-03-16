from app.ext import socketio
from flask_socketio import emit, join_room, leave_room
import json
from flask import session

@socketio.on('join_room', namespace='/chat')
def joined(message):
    room = session.get('roomid')
    username = session.get('username')
    print(room, username)
    join_room(room)
    emit('status', {'msg': ' has entered the room.'}, room=room)



    
    