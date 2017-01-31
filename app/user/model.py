import datetime
from app import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True)
    password = db.Column(db.String, nullable=False)
    about_me = db.Column(db.String(140), nullable=True)
    last_seen = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    xforms = db.relationship('Xform', backref='author', lazy='dynamic')
    instances = db.relationship('Instance', backref='author', lazy='dynamic')
    instance_histories = db.relationship('Instancehistory', backref='author', lazy='dynamic')
    notes = db.relationship('Note', backref='author', lazy='dynamic')

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

    def __init__(self, username, email, password, is_active):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.is_active = is_active

    def __repr__(self):
        return '<User %r>' %(self.username)

    def projects(self):
        return self.projects.filter(project_users.c.user_id == self.id)
