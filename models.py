from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.types import Date
from sqlalchemy.orm import relationship
from database import Base

class Room(Base):
	__tablename__ = "Rooms"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)
	width = Column(Integer)
	length = Column(Integer)
	height = Column(Integer)
	sensors = relationship("Sensor", backref="Room")

class Sensor(Base):
	__tablename__ = "Sensors"

	id = Column(Integer, primary_key=True, index=True)
	room_id = Column(Integer, ForeignKey('Rooms.id'))
	name = Column(String)
	x = Column(Integer)
	y = Column(Integer)
	z = Column(Integer)