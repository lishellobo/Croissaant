from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import re

app=Flask(__name__)

headings =("Name", "Role", "Salary")
data = (
    ("rolf", "software owner", "$2323232"),
    ("shovin", "software owner", "$2323232"),
)

@app.route("/")
def table():

    return render_template("table.html", headings=headings, data=data)

if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)