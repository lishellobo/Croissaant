from flask import Flask,redirect,url_for,render_template,request

app=Flask(_name_)

@app.route("/",methods=['POST','GET'])
def home():
    return render_template("index.html")

@app.route("/login.html",methods=['POST','GET'])
def login():
    return render_template("login.html")

if _name=='__main_':
    app.run(debug=True)