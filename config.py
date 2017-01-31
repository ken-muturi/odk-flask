# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

#: The title of this site
SITE_TITLE='ODK Server App'

#: Support contact email
SITE_SUPPORT_EMAIL = 'mymail@mydomain.com'

#: TypeKit code for fonts
TYPEKIT_CODE=''

#: Google Analytics code UA-XXXXXX-X
GA_CODE=''

#: Google Maps code 
GMAPS_CODE=''

#: Database backend
if os.environ.get('FLASK_ODK') is None:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
else:
	SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'database/app.db'))

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')

SQLALCHEMY_RECORD_QUERIES = True
WHOOSH_BASE = os.path.join(basedir, 'database/search.db')

# Whoosh does not work on Heroku
WHOOSH_ENABLED = os.environ.get('HEROKU') is None

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

#: Secret key
SECRET_KEY = '57Kcy/5DZwch7ZiW4shRzEfFjWMlzldz6GAEwHVkbgk='

#: Timezone
TIMEZONE = 'Africa/Nairobi'

#: webforms
WTF_CSRF_ENABLED = True

#: Log file
LOGFILE='error.log'

# administrator list
ADMINS = ['you@example.com']

XFORM_UPLOAD_FOLDER = 'app/static/uploads/odk/'
XFORM_UPLOAD_FOLDER_ = '/static/uploads/odk/'
UPLOAD_FOLDER = 'app/static/uploads/tmp/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xml', 'csv', 'json'])