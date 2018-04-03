from app import app
from .register import RegisterForm, register_user
from .login import check_user
from .tasks import TaskForm, create_task, get_tasks, delete_task
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
			return redirect(url_for('agenda'))
	return render_template('login.html')			

@app.route('/agenda')
def agenda():
	if session['logged_in'] == True:
		data = get_tasks(mysql)
		return render_template('agenda.html', tasks=data)
	flash('Error: you need to be logged in in order to access this service', 'warning')
	return redirect(url_for('route_home'))

@app.route('/add_task', methods=['GET', 'POST'])
def add_article():
	form = TaskForm(request.form)
	if request.method == 'POST' and form.validate() and session['logged_in'] == True:
		title = form.title.data
		start_date = form.start_date.data
		end_date = form.end_date.data
		create_task(mysql, title, start_date, end_date)
		return redirect(url_for('agenda'))
	elif session['logged_in'] == False:
		flash('Error: you need to be logged in in order to access this service', 'warning')
		return redirect(url_for('route_home'))
	return render_template('add_task.html', form=form)

@app.route('/delete_task/<string:id>', methods=['POST'])
def delete(id):
	delete_task(mysql, id)
	app.logger.info('deleting task')
	flash('Task deleted', 'success')
	return redirect(url_for('agenda'))

@app.route('/logout')
def logout():
	session.clear()
	flash('You have successfully disconnected from the session', 'success')
	return redirect(url_for('route_home'))
