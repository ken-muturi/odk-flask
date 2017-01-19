from __future__ import with_statement
import os, os.path, xmltodict, json
from sqlite3 import dbapi2 as sqlite3
from flask import Blueprint, render_template, Response, request, session, redirect, url_for, abort, flash, _app_ctx_stack, make_response

from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime

from app import app, db, lm
from app.user.model import User

logger_blueprint = Blueprint('logger', __name__)

# @Todo's
# add form download as xls
# add Xform download
# add jsonform download
# add xformsManifest
# Form xls/xml upload
# add user forms

@logger_blueprint.route('/formList', methods=['HEAD','POST','GET'])
# @login_required
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

@logger_blueprint.route('/submission',methods=['HEAD','POST','GET'])
# @login_required
def submission(username=None):
    print username
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
