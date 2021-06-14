from flask import Flask, Flask, jsonify, abort, make_response, _app_ctx_stack
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from database import SessionLocal, engine
from sqlalchemy.orm import scoped_session
import json
import models

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'waterStoffelaars!!!'
socketio = SocketIO(app)

app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

@socketio.on('connect')
def test_connect():
    print('A client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('A client disconnected')

#create and join room
@socketio.on('enterRoom')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send('"RoomID ' + username + '" has created & entered the room "' + room + '"')

#leave and delete room
@socketio.on('leaveRoom')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send('"RoomID ' + username + '" has left & deleted the room "' + room + '"')

#get all rooms
@socketio.on('getAllRooms')
def getAllRooms():
    rooms = app.session.query(models.Room).all()
    roomsList = []
    for room in rooms:
        roomsList.append({
            'id': room.id,
            'name': room.name,
            'width': room.width,
            'length': room.length,
            'height': room.height,
            'sensors': [{'id':sensor.id, 'name':sensor.name, 'x':sensor.x, 'y':sensor.y, 'z':sensor.z}for sensor in room.sensors],
            'obstacles': [{'id':obstacle.id, 'name':obstacle.name, 'x1':obstacle.x1, 'y1':obstacle.y1, 'z1':obstacle.z1, 'x2':obstacle.x2, 'y2':obstacle.y2, 'z2':obstacle.z2}for obstacle in room.obstacles]
        })
    emit('json',roomsList)

def ack(data):
    print('message from a client was received! ' + '"' + data + '"')

@socketio.on('message')
def handle_message(msg):
    emit('message', msg, callback=ack(msg))

if __name__ == '__main__':
    socketio.run(app, port=5001, debug=True)