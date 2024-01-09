from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import mysql.connector
import MySQLdb.cursors
import re
import mysql

app=Flask(__name__)
app.secret_key = 'ket'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login_registration'

mysql=MySQL(app)

@app.route("/",)
def home():
    return render_template("index.html")

@app.route("/login.html",methods=['GET','POST'])
def login():
    return render_template("login.html")

@app.route("/register.html",methods=["GET","POST"])
def register():
    return render_template("register.html")


if __name__=='__main__':
    app.run(debug=True)