from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.secret_key = 'ket'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:HwzsqdcjsodCQ5Qs@db.djaqphyiavlljtllpurl.supabase.co:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)    

class User(db.Model):
    __tablename__ = 'user-system' 
    userid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
      
@app.route("/")
def home():
    return render_template("login.html")

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        name = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(name=name, password=password).first()
        if user:
            session['loggedin'] = True
            session['userid'] = user.userid
            session['name'] = user.name
            session['email'] = user.email
            mesage = 'Logged in successfully!'
            return render_template('index.html', mesage=mesage)
        else:
            mesage = 'Please enter you correct credentials if registered, if not please register'
    return render_template("login.html", mesage=mesage)

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        user_name = request.form['name']
        password = request.form['password']
        email = request.form['email']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            mesage = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address!'
        elif not user_name or not password or not email:
            mesage = 'Please fill out the form!'
        else:
            new_user = User(name=user_name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            mesage = 'You have successfully registered!'
    elif request.method == 'POST':
        mesage = 'Please fill out the form!'
    return render_template('register.html', mesage=mesage)

@app.route("/search.html")
def search():
    return render_template("search.html")

if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)
