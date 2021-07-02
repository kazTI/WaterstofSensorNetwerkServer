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
        self.sio.on('sendASensor', self.handlesensorId)
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

    '''method uses data to add sensor to sensor list'''
    def handlesensorId(self, data):
        sensor = json.loads(data)
        sensorId = {
            "room_id": sensor['roomId'],
            "sensor_id":sensor['id']}
        if sensorId not in self.sensorIds:
            self.sensorIds.append(sensorId)

    '''send to server to receive all sensor ids'''
    def getSensorIds(self):
        self.sio.emit('getAllSensorIds')
    
    '''gets a dict containing all sensor ids'''
    def handleSensorIds(self, data):
        self.sensorIds = json.loads(data)
    
    '''returns float method generates random float'''
    def getRandomData(self):
        return random.random()
        
    '''method sends dict with random data and a corresponding sensor'''
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
#send continues data
while True:
    dataSimulator.sleep(1)
    dataSimulator.sendSensorValue()
