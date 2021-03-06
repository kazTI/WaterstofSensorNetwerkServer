from flask import Flask, Flask, jsonify, abort, make_response, _app_ctx_stack
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from database import SessionLocal, engine
from sqlalchemy.orm import scoped_session
import json
import models
import threading
import random
import time 

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
    emit('sendAllRooms', json.dumps(roomsList))

'''function gets all ids ands sends all data individualy'''
@socketio.on('ready')
def sendAllData():
    for roomId in app.session.query(models.Room.id).distinct():
        sendARoom(roomId)

    for sensorId in app.session.query(models.Sensor.id).distinct():
        sendASensor(sensorId)

    for obstacleId in app.session.query(models.Obstacle.id).distinct():
        sendAObstacle(obstacleId)

def ack(data):
    print('message from a client was received! ' + '"' + data + '"')

@socketio.on('message')
def handle_message(msg):
    emit('message', msg, callback=ack(msg))

def updateSensorValue():
    emit('updateSensorValue', json.dumps([{'id': 1, 'value': random.random()}]))

'''takes int, bool and gets a room from the database and sends it to client bool is true to send to all'''
def sendARoom(roomId, broadcast=False):
    result = app.session.query(models.Room).get(roomId)
    
    room = {
        'id': result.id,
        'name': result.name,
        'width': result.width,
        'length': result.length,
        'height': result.height
    }
    emit('sendARoom', json.dumps(room), broadcast=broadcast)
    
'''takes int, bool and gets a sensor from the database and sends it to client bool is true to send to all'''
def sendASensor(sensorId, broadcast=False):
    result = app.session.query(models.Sensor).get(sensorId)
    
    sensor = {
        'id':result.id,
        'roomId': result.room_id,
        'name':result.name, 
        'x':result.x, 
        'y':result.y, 
        'z':result.z
    }

    emit('sendASensor', json.dumps(sensor), broadcast=broadcast)

'''takes int, bool and gets a obstacle from the database and sends it to client bool is true to send to all'''
def sendAObstacle(obstacleId, broadcast=False):
    result = app.session.query(models.Obstacle).get(obstacleId)

    obstacle = {
        'id':result.id,
        'roomId': result.room_id,
        'name':result.name, 
        'x1':result.x1, 
        'y1':result.y1, 
        'z1':result.z1, 
        'x2':result.x2, 
        'y2':result.y2, 
        'z2':result.z2
    }
    emit('sendAObstacle', json.dumps(obstacle), broadcast=broadcast)

'''sends all sensors in a dict to a client that requests it'''
@socketio.on('getAllSensorIds')
def sendAllSensorIds():
    sensorIds = []
    for sensorInfo in app.session.query(models.Sensor.id, models.Sensor.room_id).distinct():
        sensorIds.append({
            "sensor_id":sensorInfo[0],
            "room_id": sensorInfo[1]
            })
    
    response = json.dumps(sensorIds)

    emit('sendAllSensorIds', response)

'''gets dict with sensor values and sends it to all connected clients'''
@socketio.on('sendSensorValueToServer')
def handleSensorValue(data):
    emit('sendSensorValue', data, broadcast=True)

'''gets Sting with json data containing room info and adds it to the database'''
@socketio.on('createRoom')
def createRoom(jsonData):
    data = json.loads(jsonData)
    room = models.Room(name = data['name'],
    width = data['width'],
    length = data['length'],
    height = data['height'])
    app.session.add(room)
    app.session.commit()
    sendARoom(room.id, broadcast=True)

'''gets Sting with json data containing room info and edits it in the database'''
@socketio.on('editRoom')
def editRoom(jsonData):
    data = json.loads(jsonData)
    
    app.session.query(models.Room).filter(models.Room.id == data['id']).update({
        'name': data['name'],
        'width': data['width'],
        'length': data['length'],
        'height': data['height']})
    app.session.commit()
    sendARoom(data['id'], broadcast=True)

'''gets Sting with json data containing sensor info and adds it to the database'''
@socketio.on('createSensor')
def createSensor(jsonData):
    data = json.loads(jsonData)
    sensor = models.Sensor(room_id = data['room_id'],
    name = data['name'],
    x = data['x'],
    y = data['y'],
    z = data['z'])
    app.session.add(sensor)
    app.session.commit()
    sendASensor(sensor.id, broadcast=True)

'''gets Sting with json data containing sensor info and edits it in the database'''
@socketio.on('editSensor')
def editSensor(jsonData):
    data = json.loads(jsonData)
    
    app.session.query(models.Sensor).filter(models.Sensor.id == data['id']).update({
        'name': data['name'],
        'x': data['x'], 
        'y': data['y'],
        'z': data['z']})
    app.session.commit()
    sendASensor(data['id'], broadcast=True)

'''gets Sting with json data containing obstacle info and adds it to the database'''
@socketio.on('createObstacle')
def createObstacle(jsonData):
    data = json.loads(jsonData)
    obstacle = models.Obstacle(room_id = data['room_id'],
    name = data['name'],
    x1 = data['x1'],
    y1 = data['y1'],
    z1 = data['z1'],
    x2 = data['x2'],
    y2 = data['y2'],
    z2 = data['z2'])
    app.session.add(obstacle)
    app.session.commit()
    sendAObstacle(obstacle.id, broadcast=True)

'''gets Sting with json data containing obstacle info and edits it in the database'''
@socketio.on('editObstacle')
def editObstacle(jsonData):
    data = json.loads(jsonData)

    app.session.query(models.Obstacle).filter(models.Obstacle.id == data['id']).update({
        'name': data['name'],
        'x1': data['x1'], 
        'y1': data['y1'],
        'z1': data['z1'],
        'x2': data['x2'], 
        'y2': data['y2'],
        'z2': data['z2']})
    app.session.commit()
    sendAObstacle(data['id'], broadcast=True)

if __name__ == '__main__':
    socketio.run(app, port=5001, debug=True)