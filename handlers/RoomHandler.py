from flask import Flask, jsonify
from flask_restful import Api, Resource

rooms = [
	{
		'id':'1',
		'lenght':100,
		'width':100,
		'height':100,
		'sensorList':[
			{
				'id':'1',
				'x':0,
				'y':0,
				'z':0
			},
			{
				'id':'2',
				'x':0,
				'y':0,
				'z':0
			},
			{
				'id':'3',
				'x':0,
				'y':0,
				'z':0
			}
		]
	},
	{
		'id':'2',
		'lenght':100,
		'width':100,
		'height':100,
		'sensorList':[
			{
				'id':'1',
				'x':0,
				'y':0,
				'z':0
			},
			{
				'id':'2',
				'x':0,
				'y':0,
				'z':0
			},
			{
				'id':'3',
				'x':0,
				'y':0,
				'z':0
			}
		]
	},
	{
		'id':'3',
		'lenght':100,
		'width':100,
		'height':100,
		'sensorList':[
			{
				'id':'1',
				'x':0,
				'y':0,
				'z':0
			},
			{
				'id':'2',
				'x':0,
				'y':0,
				'z':0
			},
			{
				'id':'3',
				'x':0,
				'y':0,
				'z':0
			}
		]
	}
]

class RoomHandler(Resource):
	
	def get(self):
		pass

class RoomsHandler(Resource):

	def get(self):
		return jsonify(rooms)