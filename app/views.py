from app import app
from .register import RegisterForm, register_user
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask import flash, redirect, url_for, session, logging, request, render_template

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
		return 	render_template('index.html')
	return render_template('register.html', form=form)
