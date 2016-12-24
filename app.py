#!flask/bin/python
from app import app

app.config.from_object(__name__)
try:
    app.config.from_object('settings')
except ImportError:
    import sys
    print >> sys.stderr, "Please create a settings.py with the necessary settings."
    print >> sys.stderr, "You may use the site without these settings, but some features may not work."

app.run(debug=True)