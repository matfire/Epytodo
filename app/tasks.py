from app import app
from wtforms import Form, StringField, TextAreaField, PasswordField, DateField, validators
from flask import flash, redirect, url_for, session, logging, request, render_template
from flask_mysqldb import MySQL

class TaskForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    start_date = DateField('start date (dd/mm/YYYY)', format='%d/%m/%Y')
    end_date = DateField('end date (dd/mm/YYYY)', format='%d/%m/%Y')

def create_task(mysql, title, start_date, end_date):
    cur = mysql.connection.cursor()
    if start_date == None and end_date != None:
        end_date_convert = str(end_date)
        cur.execute("INSERT INTO Task(title, created_by, end) VALUES(%s, %s, %s)", (title, session['username'], end_date_convert))
    elif start_date == None and end_date == None:
        cur.execute("INSERT INTO Task(title, created_by VALUES(%s, %s)", (title, session['username']))
    else:
        start_date_convert = str(start_date)
        end_date_convert = str(end_date)
        cur.execute("INSERT INTO Task(title, created_by, begin, end) VALUES(%s, %s, %s, %s)", (title, session['username'], start_date_convert, end_date_convert))
    mysql.connection.commit()
    cur.close()
    flash('task added successfully', 'success')

def get_tasks(mysql):
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM Task WHERE created_by LIKE %s', [session['username']])
    tasks = cur.fetchall()
    return tasks

def delete_task(mysql, id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Task WHERE task_id = %s", [id])
    mysql.connection.commit()
    cur.close()