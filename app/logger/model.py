import datetime
from app import db
from app.user.model import User

class Xform (db.Model):
    __tablename__ = 'logger_xforms'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(64), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('logger_projects.id'))
    uuid = db.Column(db.String(50))
    shared = db.Column(db.Boolean)
    shared_data = db.Column(db.Boolean)
    downloadable = db.Column(db.Boolean)
    has_geopoints = db.Column(db.Boolean)
    has_osm = db.Column(db.Boolean, nullable=False, default=0)
    has_start_time = db.Column(db.DateTime, nullable=True)
    num_of_submissions = db.Column(db.Integer, nullable=False, default=0)
    version = db.Column(db.String(10), nullable=False, default=0)
    last_submission_time = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    instances = db.relationship('Instance', backref='xform', lazy='dynamic')
    
    def __repr__(self):
        return '<Xform %r>' %(self.title)

    def __init__(self, filename, title, description, project_id, user_id, date_created= None):
        self.filename = filename
        self.title = title
        self.description = description
        self.user_id = user_id
        self.project_id = project_id
        if date_created is None :
            date_created = datetime.datetime.utcnow

class Instance (db.Model):
    __tablename__ = 'logger_instances'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    xform_id = db.Column(db.Integer, db.ForeignKey('logger_xforms.id'))
    survey_type_id = db.Column(db.Integer, db.ForeignKey('logger_survey_types.id'))
    json = db.Column(db.String(120), index=True)
    xml = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    uuid = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=True)

    instance_histories = db.relationship('Instancehistory', backref='instance', lazy='dynamic')
    attachments = db.relationship('Attachment', backref='instance', lazy='dynamic')
    notes = db.relationship('Note', backref='instance', lazy='dynamic')

class Instancehistory (db.Model):
    __tablename__ = 'logger_instancehistory'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    instance_id = db.Column(db.Integer, db.ForeignKey('logger_instances.id'))
    xml = db.Column(db.Text)
    uuid = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, note):
        self.note = note

    def __repr__(self):
        return '<Instance %r>' % self.note

class Note (db.Model):
    __tablename__ = 'logger_notes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    instance_id = db.Column(db.Integer, db.ForeignKey('logger_instances.id'))
    note = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, note):
        self.note = note

    def __repr__(self):
        return '<Instance %r>' % self.note

class Attachment (db.Model):
    __tablename__ = 'logger_attachments'
    id = db.Column(db.Integer, primary_key=True)
    instance_id = db.Column(db.Integer, db.ForeignKey('logger_instances.id'))
    media_file = db.Column(db.String(60))
    mimetype = db.Column(db.String(100), nullable=False)

    def __init__(self, questionniare_id, media_file, mimetype):
        self.questionniare_id = questionniare_id
        self.media_file = media_file
        self.mimetype = mimetype

    def __repr__(self):
        return '<User %r>' %(self.media_file)

class Survey_type (db.Model):
    __tablename__ = 'logger_survey_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    instances = db.relationship('Instance', backref='survey_type', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Survey Type %r>' % self.name
