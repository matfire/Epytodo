from app import app
from .register import RegisterForm, register_user
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask import flash, redirect, url_for, session, logging, request, render_template

mysql = MySQL(app)

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def route_home():
    return render_template("index.html")

@app.route('/user/<username>', methods=['GET'])
def route_user(username):
    return "Hello" + username

@app.route('/about')
def about_page():
    return render_template("about.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
			register_user(form, mysql)
			flash('You are now registered and can log in', 'success')
			return 	render_template('login.html')		
	return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password_candidate = request.form['password']
	return render_template('login.html')