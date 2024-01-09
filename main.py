from flask import Flask,redirect,url_for,render_template,request
import mysql.connector

app=Flask(__name__)

@app.route("/",)
def home():
    return render_template("index.html")

@app.route("/login.html")
def login():
    return render_template("login.html")

if __name__=='__main__':
    app.run(debug=True)