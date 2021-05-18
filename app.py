from flask import Flask, jsonify, abort, make_response, _app_ctx_stack
from flask_restful import Api, Resource, reqparse, fields, marshal, request
from sqlalchemy.orm import scoped_session
import json

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = Flask(__name__)
api = Api(app)

app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
class RoomHandler2(Resource):
	def get(self, roomId):
		roomModel = app.session.query(models.Room).get(roomId)
		if roomModel == None:
			return 'error no room found', 404
		# print(roomModel.sensors[0].x)
		room = {
			'id': roomModel.id,
			'name': roomModel.name,
			'width': roomModel.width,
			'length': roomModel.length,
			'height': roomModel.height,
			'sensors': [{'id':sensor.id, 'name':sensor.name, 'x':sensor.x, 'y':sensor.y, 'z':sensor.z}for sensor in roomModel.sensors]
		}
		return jsonify(room)

	def post(self, roomId):
		data = json.loads(request.data)
		sensor = models.Sensor(room_id = roomId,
		name = data['name'],
		x = data['x'],
		y = data['y'],
		z = data['z'])

		app.session.add(sensor)
		app.session.commit()
		return 'success',201

class SensorHandler(Resource):
	def put(self, sensorId):
		data = json.loads(request.data)
		
		app.session.query(models.Sensor).filter(models.Sensor.id == sensorId).update({
			'name': data['name'],
			'x': data['x'], 
			'y': data['y'],
			'z': data['z']})
		app.session.commit()
		return 'success',201


class RoomHandler(Resource):
	
	def get(self):
		pass
	
	def post(self):
		data = json.loads(request.data)
		room = models.Room(name = data['name'],
		width = data['width'],
		length = data['length'],
		height = data['height'])
		app.session.add(room)
		app.session.commit()
		print('name: ' +data['name'])
		print('width: '+data['width'])
		print('length: '+data['length'])
		print('height: '+data['height'])
		return 'success',201

class RoomsHandler(Resource):

	def get(self):
		rooms = app.session.query(models.Room).all()
		roomsList = []
		for room in rooms:
			roomsList.append({
				'id': room.id,
				'name': room.name,
				'width': room.width,
				'length': room.length,
				'height': room.height,
				'sensors': [{'id':sensor.id, 'name':sensor.name, 'x':sensor.x, 'y':sensor.y, 'z':sensor.z}for sensor in room.sensors]
			})
		return jsonify(roomsList)

api.add_resource(RoomsHandler, '/room/all')
api.add_resource(RoomHandler, '/room')
api.add_resource(RoomHandler2, '/room/<roomId>')
api.add_resource(SensorHandler, '/sensor/<sensorId>')

if __name__ == '__main__':
	app.run(debug=True)