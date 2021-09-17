from os import getenv

from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from models import initialize_models

app = Flask(__name__)

# app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
# Lets use sqlite for development
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
initialize_models(db)

print(db.engine.table_names())

@app.route("/")
def index():
    result = db.session.execute("SELECT username FROM user")
    messages = result.fetchall()
    return render_template("index.html", count=len(messages), messages=messages) 

@app.route("/projects")
def projects():
    pass


@app.route("/new")
def new():
    return render_template("new.html")


@app.route("/send", methods=["POST"])
def send():
    content = request.form["file"]
    sql = "INSERT INTO messages (content) VALUES (:content)"
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return redirect("/")


@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    session["username"] = username
    return redirect("/")



@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

