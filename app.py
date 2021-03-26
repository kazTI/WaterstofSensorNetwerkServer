from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from handlers.RoomHandler import RoomHandler, RoomsHandler

app = Flask(__name__)
api = Api(app)


api.add_resource(RoomsHandler, '/room/all')

if __name__ == '__main__':
    app.run(debug=True)