from functools import wraps
from os import getenv

from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.schema import CreateTable

from . import models

app = Flask(__name__)

REWRITTEN_DATABASE_URL = getenv("DATABASE_URL").replace('postgres://', 'postgresql://')
app.config["SQLALCHEMY_DATABASE_URI"] = REWRITTEN_DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)
AppUser, Project, File = models.initialize_models(db)

print(db.engine.table_names())
print([print(CreateTable(item.__table__)) for item in [AppUser, Project, File]])

# TODO: implement selecting active project
current_project = "first_test_project"


def is_logged_in_user():
    return session["username"] is not None

def is_admin():
    return session["is_admin"] == True


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        allow = False
        if is_admin():
            allow = True
        elif is_logged_in_user():
            allow = True
        if not allow:
            return render_template("error.html", error="Ei oikeutta nähdä sivua")
        return f(*args, **kws)
    return decorated_function


@app.route("/")
def index():
    result = db.session.execute("SELECT username FROM app_user")
    messages = result.fetchall()
    return render_template("index.html", count=len(messages), messages=messages) 


@app.route("/projects")
def projects():
    # TODO: Fetch the projects from DB and give as parameter to render_template
    return render_template("projects.html")


@app.route("/project/<int:id>")
@auth_required
def project(id: int):
    sql = "SELECT id, name FROM project WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    name = result.fetchone().name
    sql = "SELECT id, data FROM file WHERE containing_project=:id"
    result = db.session.execute(sql, {"id": id})
    files = result.fetchall()
    return render_template("project_view.html", name=name, current_files=files)


@app.route("/add_file")
@auth_required
def add_file():
    sql = "SELECT id, name FROM project WHERE owner=:username"
    result = db.session.execute(sql, {"username":session["username"]})
    available_projects = result.fetchall()
    return render_template("new_file", available_projects=available_projects)


@app.route("/send_file", methods=["POST"])
def send_file():
    content = request.form["file"]
    new_file = File(owner=session["username"], containing_project=current_project, data=content )
    db.session.add(new_file)
    return redirect("/")


@app.route("/add_project")
@auth_required
def add_project():
    return render_template("new_project.html")



@app.route("/send_project", methods=["POST"])
def send_project():
    pass

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    print(f"Querying for user with username: {username}")
    # Check username and password
    sql = "SELECT id, password, is_admin FROM app_user WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        print(f"User not found, result of query: {user}")
        return render_template("invalid_credentials.html")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            pass
        else:
            return render_template("invalid_credentials.html")

    session["username"] = username
    session["is_admin"] = user["is_admin"]
    return redirect("/")



@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

if __name__ == "__main__":
    app.run()
