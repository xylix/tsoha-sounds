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
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)
User, Project, File = initialize_models(db)

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
    new_file = File(owner=session.username, containing_project=current_project, data=content )
    db.session.add(new_file)
    return redirect("/")


@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    print(f"Querying for user with username: {username}")
    # Check username and password
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f"User not found, result of query: {user}")
        return render_template("invalid_credentials.html")
    else:
        print(user.password)
        hash_value = user.password
        if check_password_hash(hash_value, password):
            pass
        else:
            return render_template("invalid_credentials.html")

    session["username"] = username
    return redirect("/")



@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

