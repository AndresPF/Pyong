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

	def __init__(self, name, email=""):
		self.name = name
		self.email = email

	def insert(self):
		db.session.add(self)
		db.session.commit()
	
	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def format(self):
		matchesA = [match.format() for match in self.match_a]
		matchesB = [match.format() for match in self.match_b]
		return {
			'id': self.id,
			'name': self.name,
			'email': self.email,
			'match_a': matchesA[0:2],
			'match_b': matchesB[0:2]}

class Match(db.Model):  
	__tablename__ = 'Match'

	id = Column(Integer, primary_key=True)
	playerA_id = db.Column(db.Integer, db.ForeignKey('Player.id'), nullable=False)
	playerB_id = db.Column(db.Integer, db.ForeignKey('Player.id'), nullable=False)
	scoreA = Column(Integer)
	scoreB = Column(Integer)
	date = Column(DateTime(timezone=True))
	playerA = db.relationship(Player, lazy="joined", foreign_keys="Match.playerA_id", backref="match_a")
	playerB = db.relationship(Player, lazy="joined", foreign_keys="Match.playerB_id", backref="match_b")

	def __init__(self, scoreA, scoreB, date, playerA_id, playerB_id):
		self.scoreA = scoreA
		self.scoreB = scoreB
		self.date = date
		self.playerA_id = playerA_id
		self.playerB_id = playerB_id

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
			'scoreA': self.scoreA,
			'scoreB': self.scoreB,
			'date': self.date,
			'playerA': self.playerA.name,
			'playerB': self.playerB.name}