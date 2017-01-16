import datetime
from hashlib import md5
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    registered_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @property
    def is_authenticated(self):
        return True    

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id) # python 2
        except NameError:
            return str(self.id) #python 3

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    def __init__(self, social_id, nickname, email):
        self.social_id = social_id
        self.nickname = nickname
        self.email = email

    def __repr__(self):
        return '<User %r>' %(self.nickname)
