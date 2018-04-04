from app import app
from .register import RegisterForm, register_user
from .login import check_user
from .tasks import TaskForm, create_task, get_tasks, delete_task
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask import flash, redirect, url_for, session, logging, request, render_template
from functools import wraps

mysql = MySQL(app)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

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
@is_logged_in
def agenda():
	data = get_tasks(mysql)
	return render_template('agenda.html', tasks=data)
	
@app.route('/add_task', methods=['GET', 'POST'])
@is_logged_in
def add_article():
	form = TaskForm(request.form)
	if request.method == 'POST' and form.validate():
		title = form.title.data
		start_date = form.start_date.data
		end_date = form.end_date.data
		create_task(mysql, title, start_date, end_date)
		return redirect(url_for('agenda'))
	return render_template('add_task.html', form=form)

@app.route('/delete_task/<string:id>', methods=['POST'])
@is_logged_in
def delete(id):
	delete_task(mysql, id)
	app.logger.info('deleting task')
	flash('Task deleted', 'success')
	return redirect(url_for('agenda'))

@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You have successfully disconnected from the session', 'success')
	return redirect(url_for('route_home'))

@app.route('/faq')
def faq():
	return render_template('faq.html')