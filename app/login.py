from app import app
from flask import flash, redirect, url_for, session, logging, request, render_template
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

def check_user(username, password_candidate, mysql):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM User WHERE username = %s", [username])
    cur.close()
    if result > 0:
        data = cur.fetchone()
        password = data['password']
        if sha256_crypt.verify(password_candidate, password):
            app.logger.info("password correct")
            return 0
        else:
            return 2
    else:
        app.logger.info("NO USER")
        return 1
