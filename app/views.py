from app import app
from .register import RegisterForm, register_user
from .login import check_user
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
			return 	redirect(url_for('login'))		
	return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password_candidate = request.form['password']
		result = check_user(username, password_candidate, mysql)
		if result == 1:
			error = 'User not found'
			return render_template('login.html', error=error)
		elif result == 2:
			error = 'Incorrect Password'
			return render_template('login.html', error=error)
		else:
			session['logged_in'] = True
			session['username'] = username
			flash('You are now logged in', 'success')
			return redirect(url_for('dashboard'))
	return render_template('login.html')			

@app.route('/agenda')
def agenda():
	if session['logged_in'] == True:
		return render_template('agenda.html')
	flash('Error: you need to be logged in order to access this service', 'warning')
	return redirect(url_for('index'))