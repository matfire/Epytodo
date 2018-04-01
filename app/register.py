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

def register_user(form, mysql):
	name = form.name.data
	email = form.email.data
	username = form.email.data
	password = sha256_crypt.encrypt(str(form.password.data))

	#create DictCursor
	cursor = mysql.connection.cursor()
	cursor.execute("INSERT INTO User(name, username, email, password) VALUES(%s, %s, %s, %s)", (name, username, email, password))

	#Commit to DB
	mysql.connection.commit()

	#Close connection
	cursor.close()