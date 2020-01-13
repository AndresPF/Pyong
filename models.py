from sqlalchemy import Column, String, create_engine
from sqlalchemy import Column, Integer, String, DateTime
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
		binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
		app.config["SQLALCHEMY_DATABASE_URI"] = database_path
		app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
		db.app = app
		db.init_app(app)
		db.create_all()


class Player(db.Model):  
	__tablename__ = 'Player'

	id = Column(Integer, primary_key=True)
	name = Column(String, unique=True, nullable=False)
	email = Column(String)
	matches = db.relationship('Matches', cascade = "all, delete")

	def __init__(self, name, email="", matches=[]):
		self.name = name
		self.email = email
		self.matches = matches

	def insert(self):
		db.session.add(self)
		db.session.commit()
	
	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def format(self):
		return {
			'id': self.id,
			'name': self.name,
			'email': self.email,
			'matches': self.matches}

class Matches(db.Model):  
	__tablename__ = 'Matches'

	id = Column(Integer, primary_key=True)
	scoreA = Column(Integer)
	scoreB = Column(Integer)
	date = Column(DateTime)
	playerA = db.relationship("Player", back_populates="matches")
	playerB = db.relationship("Player", back_populates="matches")

	def __init__(self, scoreA, scoreB, date, playerA, playerB):
		self.scoreA = scoreA
		self.scoreB = scoreB
		self.date = date
		self.playerA = playerA
		self.playerB = playerB

	def format(self):
		return {
			'id': self.id,
			'scoreA': self.scoreA,
			'scoreB': self.scoreB,
			'date': self.date,
			'playerA': self.playerA,
			'playerB': self.playerB}