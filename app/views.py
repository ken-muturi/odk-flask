from __future__ import with_statement
import os, os.path, xmltodict, json
from sqlite3 import dbapi2 as sqlite3
from flask import render_template, Response, request, session, g, redirect, url_for, abort, flash, _app_ctx_stack, make_response
from app import app

# @Todo's
# add form download as xls
# add Xform download
# add jsonform download
# add xformsManifest
# Form xls/xml upload
# 

# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     top = _app_ctx_stack.top
#     if not hasattr(top, 'sqlite_db'):
#         top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
#     return top.sqlite_db

# @app.before_request
# def before_request():
#     method = request.form.get('_method', '').upper()
#     if method:
#         request.environ['REQUEST_METHOD'] = method
#         ctx = flask._request_ctx_stack.top
#         ctx.url_adapter.default_method = method
#         assert request.method == method
    
#     g.user = current_user
#     if( g.user.is_authenticated ):
#         g.user.last_seen = datetime.utcnow()
#         db.session.add(g.user)
#         db.session.commit()

# @app.teardown_appcontext
# def close_db_connection(exception):
#     """Closes the database again at the end of the request."""
#     top = _app_ctx_stack.top
#     if hasattr(top, 'sqlite_db'):
#         top.sqlite_db.close()

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Kenneth'}  # fake user
    return render_template('home.html')

@app.route('/formList',methods=['HEAD','POST','GET'])
def formList():
    _forms = ["<?xml version='1.0' encoding='UTF-8' ?>"]
    _forms.append( '<xforms xmlns="http://openrosa.org/xforms/xformsList">' )
    path =  app.static_folder + '/uploads/odk/'
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f) ) ]
    for f in files :
        if f.endswith('.xml') :
            basename = os.path.basename(f)
            url =  'https://flask-odk.herokuapp.com/static/uploads/odk/'+ f
            _forms.append( "<xform>" )
            _forms.append( "<formID>"+ basename +"</formID>" )
            _forms.append( "<name>"+ basename +"</name>" )
            _forms.append( "<version>1.1</version>" )
            _forms.append( "<downloadUrl>"+ url +"</downloadUrl>" )
            _forms.append( "</xform>" )

    _forms.append("</xforms>")
    xml = "".join(_forms)
    response = Response(xml, mimetype='text/xml')
    response.headers['X-OpenRosa-Version'] = '1'
    return response

@app.route('/submission',methods=['HEAD','POST','GET'])
def submission():
    print request.values
    if request.environ['REQUEST_METHOD'] == 'HEAD':
        response = make_response(render_template('head_request.txt'))
        response.headers['X-OpenRosa-Version'] = '1'
        return response, 204
    elif request.environ['REQUEST_METHOD'] == 'POST':
        deviceid = request.args.get('deviceID')
        print deviceid

        _post_values = request.form.values
        print _post_values
        
        media_files = request.files.values()
        print media_files

        xml = ""
        upFile = request.files['xml_submission_file']
        print upFile.name
        xml = upFile.read()
        o = xmltodict.parse(xml)
        print json.dumps( o )
    
        #return response
        response = make_response(render_template('home.html'))
        response.headers['X-OpenRosa-Version'] = '1'
        return response, 201
    elif request.environ['REQUEST_METHOD'] == 'GET':
        response = make_response(render_template('home.html'))
        return response, 200

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
# @app.route('/login',methods=['GET','POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     username = request.form['username']
#     password = request.form['password']
#     registered_user = User.query.filter_by(username=username,password=password).first()
#     if registered_user is None:
#         flash('Username or Password is invalid' , 'error')
#         return redirect(url_for('login'))
#     login_user(registered_user)
#     flash('Logged in successfully')
#     return redirect(request.args.get('next') or url_for('index'))

# @app.route('/register' , methods=['GET','POST'])
# def register():
#     if request.method == 'GET':
#         return render_template('register.html')
#     user = User(request.form['username'] , request.form['password'],request.form['email'])
#     db.session.add(user)
#     db.session.commit()
#     flash('User successfully registered')
#     return redirect(url_for('login'))
 
# @lm.user_loader
# def load_user(id):
#     return User.query.get(int(id))

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))
