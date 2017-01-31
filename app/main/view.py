import os
from sqlite3 import dbapi2 as sqlite3
from flask import Blueprint, render_template, Response, request, redirect, url_for, abort, flash
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import app, db, lm, bcrypt
from forms import OrganizationForm, ProjectForm
from model import Organization, Project
from app.user.model import User

main_blueprint = Blueprint('main', __name__,)

@main_blueprint.route('/')
@login_required
def home():
	return render_template('main/home.html')

@main_blueprint.route('/main/organizations/', methods=['GET'])
@login_required
def organizations():
	organizations = Organization.query.all()
	return render_template('main/organization-home.html', organizations=organizations, title = 'Manage Organizations')

@main_blueprint.route('/main/create-organization/', methods=['GET', 'POST'])
@login_required
def create_organization():
	organization_form = OrganizationForm()
	if request.method == 'POST' and organization_form.validate() :
		organization = Organization(
			title = organization_form.title.data,
			description = organization_form.description.data,
			email = organization_form.email.data,
			address = organization_form.address.data,
			website = organization_form.website.data
		)
		db.session.add(organization)
		db.session.commit()
		flash('Organization successfully created',  'success')
		return redirect(url_for('main.organizations'))
	else :
		flash('Errors in saving Organization Data. Please review the errors',  'error')

	return render_template('main/create-organization.html', form=organization_form, title='Manage Organization: Create')

@main_blueprint.route('/main/projects/<organization_id>', methods=['GET'])
@login_required
def projects( organization_id ):
	projects = Project.query.filter_by(organization_id = int(organization_id))
	return render_template('main/project-home.html', projects=projects, title = 'Manage Organizations')

@main_blueprint.route('/main/create-project/', methods=['GET', 'POST'])
@login_required
def create_project():
	project_form = ProjectForm()
	populate_form_choices(project_form)
	if request.method == 'POST' and project_form.validate() :
		# organization = Organization(organization_id)
		project = Project(
			title = project_form.title.data,
			description = project_form.description.data,
			organization_id = project_form.organization.data
		)
		db.session.add(project)
		db.session.commit()
		flash('Project successfully registered',  'success')
		return redirect(url_for('main.projects', organization_id = project_form.organization.data))
	else :
		flash('Errors in saving Project Data. Please review the errors',  'error')
	return render_template('main/create-project.html', form=project_form, title=app.config['SITE_TITLE'])

@main_blueprint.route('/main/project-users/<organization_id>/<project_id>', methods=['GET', 'POST'])
@login_required
def project_users( organization_id, project_id ):
	users = User.query.all()
	if request.method == 'POST' :
		p = Project.query.get(int(project_id))
		users = request.form.getlist('users')
		for user in users :
			u = User.query.get(int(user))
			p.users.append(u)		
		db.session.add(p)
		db.session.commit()
		flash('Project users successfully Added',  'success')
		return redirect(url_for('main.project_users', organization_id = organization_id, project_id = project_id))
	else :
		flash('Errors in saving Project Data. Please review the errors',  'error')
	return render_template('main/project-users.html', users=users, title = 'Manage Project Users')

def populate_form_choices( project_form ):
	organizations = Organization.query.all()
	options = []
	for org in organizations :
		options.append( (org.id, org.title) ) 
	project_form.organization.choices = options
