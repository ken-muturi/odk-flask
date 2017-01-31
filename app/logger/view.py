from __future__ import with_statement
import os, os.path, xmltodict, json
from werkzeug.utils import secure_filename
from sqlite3 import dbapi2 as sqlite3
from flask import Blueprint, render_template, Response, request, session, g, redirect, url_for, abort, flash, send_from_directory, make_response

from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime

from app import app, db, lm
from app.user.model import User
from app.user.view import auth, verify_password
from model import *
from forms import XformUploadForm
from app.main.model import Project

logger_blueprint = Blueprint('logger', __name__)

# @Todo's
# add form download as xls
# add Xform download
# add jsonform download
# add xformsManifest
# Form xls/xml upload
# add user forms

@logger_blueprint.route('/formList', methods=['HEAD','POST','GET'])
@auth.login_required
def formList():
    user = User.query.get(int(g.user.id))
    _forms = ["<?xml version='1.0' encoding='UTF-8' ?>"]
    _forms.append( '<xforms xmlns="http://openrosa.org/xforms/xformsList">' )
    path =  app.static_folder + '/uploads/odk/'
    for user_projects in user.projects :
        for xform in user_projects.projects.all() :
            if( os.path.isfile(os.path.join(path, xform.filename) ) ) : # and xform.filename.endswith('.xml')
                basename = os.path.basename(xform.filename)
                url =  'https://flask-odk.herokuapp.com/static/uploads/odk/'+ xform.filename
                _forms.append( "<xform>" )
                _forms.append( "<formID>"+ basename +"</formID>" )
                _forms.append( "<name>"+ basename +"</name>" )
                _forms.append( "<version>"+ xform.version +"</version>" )
                _forms.append( "<downloadUrl>"+ url +"</downloadUrl>" )
                _forms.append( "</xform>" )

    _forms.append("</xforms>")
    xml = "".join(_forms)
    response = Response(xml, mimetype='text/xml')
    response.headers['X-OpenRosa-Version'] = '1'
    return response

@logger_blueprint.route('/submission',methods=['HEAD','POST','GET'])
@auth.login_required
def submission():
    auth = request.authorization
    if( verify_password(auth.username, auth.password) ) :
        if request.environ['REQUEST_METHOD'] == 'HEAD':
            response = make_response(render_template('head_request.txt'))
            response.headers['X-OpenRosa-Version'] = '1'
            return response, 204
        elif request.environ['REQUEST_METHOD'] == 'POST':
            deviceid = request.args.get('deviceID')
            print deviceid
            
            media_files = request.files.values()
            print media_files

            xml = ""
            upFile = request.files['xml_submission_file']
            print upFile.name
            xml = upFile.read()
            o = xmltodict.parse(xml)
            print json.dumps( o )
            
            instance = Instance(
                user_id = current_user.id,
                xform_id = project_id,
                json = json.dumps( o ),
                xml = xml,
                uuid = deviceid
            )
            db.session.add(instance)
            db.session.commit()
            #return response
            response = make_response(render_template('home.html'))
            response.headers['X-OpenRosa-Version'] = '1'
            return response, 201
    response = make_response(render_template('home.html'))
    return response, 200

@logger_blueprint.route('/projects/<project_id>/details', methods=['GET'])
@login_required
def xforms(project_id):
    project = Project.query.get(int(project_id))
    xforms = Xform.query.filter_by(project_id = int(project_id))
    return render_template('logger/project-xforms.html', project = project, xforms=xforms, title = 'Project Details')

@logger_blueprint.route('/projects/<project_id>/xform/upload/', methods=['GET', 'POST'])
@login_required
def upload_file( project_id = None):
    upload_form = XformUploadForm()
    if request.method == 'POST' and upload_form.validate() :
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['XFORM_UPLOAD_FOLDER'], filename))

            # p = Project.query.get(project_id)
            # u = User.query.get(current_user.id)
            #save file in db..
            xform = Xform(
                title = request.form['title'], 
                description = request.form['description'], 
                user_id = current_user.id,
                project_id = project_id,
                filename = filename
            )
            db.session.add(xform)
            db.session.commit()
            return redirect(url_for('logger.uploaded_file', project_id=project_id, filename=filename))
    return render_template('logger/xform-upload.html', upload_form = upload_form, project_id = project_id, title=app.config['SITE_TITLE'])

@logger_blueprint.route('/projects/<project_id>/uploads/<filename>')
@login_required
def uploaded_file(project_id, filename):
    return send_from_directory(app.config['XFORM_UPLOAD_FOLDER_'], filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
