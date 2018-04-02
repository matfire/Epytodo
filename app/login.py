from app import app
from flask import flash, redirect, url_for, session, logging, request, render_template
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

def check_user(username, password_candidate, mysql):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM User WHERE username = %s", [username])
    if result >= 1:
        data = cur.fetchone()
        app.logger.info(data)
        password = data['password']
        cur.close()
        if sha256_crypt.verify(password_candidate, password):
            app.logger.info("password correct")
            return 0
        else:
            return 2
    else:
        cur.close()
        app.logger.info("NO USER")
        return 1
