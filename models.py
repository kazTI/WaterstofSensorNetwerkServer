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
	obstacles = relationship("Obstacle", backref="Room")

class Sensor(Base):
	__tablename__ = "Sensors"

	id = Column(Integer, primary_key=True, index=True)
	room_id = Column(Integer, ForeignKey('Rooms.id'))
	name = Column(String)
	x = Column(Integer)
	y = Column(Integer)
	z = Column(Integer)

class Obstacle(Base):
	__tablename__ = "Obstacles"

	id = Column(Integer, primary_key=True, index=True)
	room_id = Column(Integer, ForeignKey('Rooms.id'))
	name = Column(String)
	x1 = Column(Integer)
	y1 = Column(Integer)
	z1 = Column(Integer)
	x2 = Column(Integer)
	y2 = Column(Integer)
	z2 = Column(Integer)