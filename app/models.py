from hashlib import md5
from app import db

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140)) 
	body = db.Column(db.String(255)) 
	timestamp = db.Column(db.DateTime) 
	
	def __repr__(self):
		return '<Post %r>' %(self.title)

