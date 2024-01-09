from flask import Flask,redirect,url_for,render_template,request,flash,Blueprint

app=Flask(__name__)
auth = Blueprint('auth', __name__)

@app.route("/",)
def home():
    return render_template("index.html")

@app.route("/login.html",methods=['GET','POST'])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        username=request.form.get("username")
        password=request.form.get("password")
    return render_template("login.html")

if __name__=='__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)