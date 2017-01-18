from sqlite3 import dbapi2 as sqlite3
from flask import Blueprint, render_template, Response, request, redirect, url_for, abort, flash

from flask_login import login_user, logout_user, current_user, login_required

from app import app, db, lm, bcrypt
from model import User
from forms import LoginForm, RegisterForm, ChangePasswordForm

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/register' , methods=['GET','POST'])
def register():
    register_form = RegisterForm(request.form)
    if register_form.validate_on_submit() :        
        user = User(
            username = register_form.username.data, 
            email = register_form.email.data,
            password = register_form.password.data
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('User successfully registered',  'success')
        return redirect(url_for('index'))
    return render_template('login/register.html', title=app.config['SITE_TITLE'], form=register_form)

@user_blueprint.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm( request.form )
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']) :
            remember_me = False
            if remember_me in request.form :
                remember_me = True
            login_user(registered_user, remember = remember_me)
            flash('Logged in successfully', 'success')
            return redirect(flask.request.args.get('next') or url_for('index'))
        else:
            flash('Username or Password is invalid' , 'error')
    return render_template('login/home.html', title=app.config['SITE_TITLE'], form=form)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@user_blueprint.route('/user/<nickname>', methods=['GET'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        flash('User %s not found.' % username, 'error')
        return redirect(url_for('index'))
    return render_template('user.html', user=user)

@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('Password successfully changed.', 'success')
            return redirect(url_for('user/'+ current_user.username ))
        else:
            flash('Password change was unsuccessful.', 'danger')
            return redirect(url_for('user/'+ current_user.username ))
    return render_template('user/profile.html', form=form)

@user_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
