import random
import socketio
import json

class DataSimulator():
    #Initialize socketIO client
    sio = socketio.Client(logger=False, engineio_logger=False)

    def __init__(self):
        self.sio.connect('http://localhost:5001')
        self.sensorIds = []
        self.sio.on('sendAllSensorIds', self.handleSensorIds)
        pass
    #Default socketIO events
    #-------------------------------------------------------------------------#
    @sio.event
    def connect():
        print('Connected with SocketIO server')

    @sio.event
    def connect_error(data):
        print("Connection with SocketIO server failed!")

    @sio.event
    def disconnect():
        print('Disconnected from SocketO server')


    def getSensorIds(self):
        self.sio.emit('getAllSensorIds')
    
    def handleSensorIds(self, data):
        self.sensorIds = json.loads(data)
    
    def getRandomData(self):
        return random.random()
        
    def sendSensorValue(self):
        sensorData = {}
        for sensorId in self.sensorIds:
            sensorData[sensorId['sensor_id']] = {}
            sensorData[sensorId['sensor_id']]['value'] = self.getRandomData()
            sensorData[sensorId['sensor_id']]['room_id'] = sensorId['room_id']
        
        response = json.dumps(sensorData)

        self.sio.emit('sendSensorValueToServer', response)

    def sleep(self, time):
        self.sio.sleep(time)

dataSimulator = DataSimulator()
dataSimulator.getSensorIds()
while True:
    dataSimulator.sleep(1)
    dataSimulator.sendSensorValue()




        