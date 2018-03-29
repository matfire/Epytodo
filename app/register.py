from app import app
from flask import flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message="Passwords do not match")])
    confirm = PasswordField('Confirm password')

def register_user(form):
	name = form.name.data
	email = form.email.data
	username = form.email.data
	password = sha256_crypt.encrypt(str(form.password.data))
	mysql = MySQL(app)

	#create DictCursor
	cursor = mysql.connection.cursor()
	cursor.execute("INSERT INTO user(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

	#Commit to DB
	mysql.connection.commit()

	#Close connection
	cursor.close()

	flash('You are now registered and can log in', 'success')
