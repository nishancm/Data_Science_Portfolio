#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, redirect, render_template, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_login import (current_user, LoginManager, login_required,
                         login_user, logout_user, UserMixin)
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email
import os

from flask_mongoalchemy import MongoAlchemy
from flask_mongoengine import MongoEngine 
from werkzeug.security import check_password_hash, generate_password_hash
from plotly_example import plotly_map

# Create and configure an app.
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///week5.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
app = Flask(__name__)
# app.config['MONGOALCHEMY_DATABASE'] = 'find_your_path'
# db = MongoAlchemy(app)
app.config['MONGODB_SETTINGS'] = {"db": "find_your_path"}
db = MongoEngine(app)
login_manager = LoginManager()
bootstrap = Bootstrap(app)


class User(db.Document, UserMixin):
    #id = db.IntField(db.Integer, primary_key=True)
    meta = {"db": "find_your_path"}
    id = db.IntField(primary_key=True)
    username = db.StringField()
    email = db.StringField()
    password_hash = db.StringField()


    # def __init__(self, username, email, password):
    #     self.username = username
    #     self.email = email
    #     self.set_password(password)

    # def is_authenticated(self):
    #     return True

    # def is_active(self):
    #     return True

    # def is_anonymous(self):
    #     return False 

    # def get_id(self):
    #     return self.username 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LogInForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/register', methods=('GET', 'POST'))
def register():
    registration_form = RegistrationForm()
    # if registration_form.validate_on_submit():
    #     username = registration_form.username.data
    #     password = registration_form.password.data
    #     email = registration_form.email.data

    #     user_count = User.query.filter_by(username=username).count()
    #     + User.query.filter_by(email=email).count()
    #     if(user_count > 0):
    #         flash('Error - Existing user : ' + username + ' OR ' + email)
    #     else:
    #         user = User(username, email, password)
    #         db.session.add(user)
    #         db.session.commit()
    #         return redirect(url_for('login'))
    
    if registration_form.validate():
        existing_user = User.objects(email=registration_form.email.data).first()
        if existing_user is None:
            username = registration_form.username.data
            password = registration_form.password.data
            email = registration_form.email.data
            new_user = User(username, email, password).save()
            return redirect(url_for('login'))
    return render_template('register.html', form=registration_form)


# @login_manager.user_loader
# def load_user(id):  # id is the ID in User.
#     return User.query.get(int(id))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     login_form = LogInForm()
#     if login_form.validate_on_submit():
#         username = login_form.username.data
#         password = login_form.password.data
#         # Look for it in the database.
#         user = User.query.filter_by(username=username).first()

#         # Login and validate the user.
#         if user is not None and user.check_password(password):
#             login_user(user)
#             return redirect(url_for('examples'))
#         else:
#             flash('Invalid username and password combination!')
#     return render_template('login.html', form=login_form)


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('index'))


# @app.route('/examples', methods=('GET', 'POST'))
# @login_required
# def examples():
#     return render_template('examples_main.html')


# @app.route('/media_example', methods=('GET', 'POST'))
# @login_required
# def media_example():
#     return render_template('media_example.html')


# @app.route('/progress_example', methods=('GET', 'POST'))
# @login_required
# def progress_example():
#     return render_template('progress_example.html', progress=50)


# @app.route('/plotly_example', methods=('GET', 'POST'))
# @login_required
# def plotly_example():
#     output = plotly_map()
#     return render_template('plotly_map.html', source=output)


# @app.route('/google_example', methods=('GET', 'POST'))
# @login_required
# def google_example():
#     return render_template('google_wordtree.html')

@app.route('/fyp_example', methods = ('GET', 'POST'))
def fyp_example():
    return render_template('fyp_example.html')


@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html',
                           authenticated_user=current_user.is_authenticated)


if __name__ == '__main__':
    # login_manager needs to be initiated before running the app
    login_manager.init_app(app)
    # flask-login uses sessions which require a secret Key
    app.secret_key = os.urandom(24)

    # Create tables.
    #db.create_all()
    #db.session.commit()

    app.run(host='0.0.0.0', port=8080, debug=True)
