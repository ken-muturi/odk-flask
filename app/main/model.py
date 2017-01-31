import datetime
from app import db
from app.user.model import User

class Organization (db.Model):
    __tablename__ = 'organizations'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True, unique=True)
    description = db.Column(db.String(200))
    email = db.Column(db.String(60), unique=True)
    address = db.Column(db.String(100))
    website = db.Column(db.String(100), nullable=True)

    projects = db.relationship('Project', backref='organization', lazy='dynamic')
    
    def __init__(self, title, description, email, address, website):
        self.title = title
        self.description = description
        self.email = email
        self.address = address
        self.website = website

    def __repr__(self):
        return '<Organization %r>' % self.title

projects_users = db.Table('logger_projects_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key = True),
    db.Column('project_id', db.Integer, db.ForeignKey('logger_projects.id'), primary_key = True)
)

class Project (db.Model):
    __tablename__ = 'logger_projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True, unique=True)
    description = db.Column(db.String(200))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    shared = db.Column(db.Boolean, default=0)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=True)

    users = db.relationship('User', secondary=projects_users, backref='projects', lazy='dynamic')
    projects = db.relationship('Xform', backref='project', lazy='dynamic')

    def __init__(self, title, description, organization_id, date_created = None):
        self.title = title
        self.description = description
        self.organization_id = organization_id

        if date_created is None :
        	date_created = datetime.datetime.utcnow
    
    def __repr__(self):
        return '<Project %r>' % self.title
