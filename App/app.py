from functools import wraps
from os import getenv
from typing import Optional

from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.schema import CreateTable

from . import models

app = Flask(__name__)

REWRITTEN_DATABASE_URL = getenv("DATABASE_URL").replace('postgres://', 'postgresql://')
app.config["SQLALCHEMY_DATABASE_URI"] = REWRITTEN_DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)
models = models.initialize_models(db)


def is_logged_in_user():
    return session.get("username") is not None

def is_admin():
    return session.get("is_admin") == True


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
    if is_admin():
        result = db.session.execute("SELECT name,id FROM project WHERE NOT owner = :user_id", {"user_id": session["user_id"]})
    else:
        result = db.session.execute("SELECT name,id FROM project WHERE NOT owner = :user_id AND published=True", {"user_id": session["user_id"]})
    public_projects = result.fetchall()
    own_projects = db.session.execute("SELECT name,id FROM project WHERE owner=:id", {"id": session["user_id"]}).fetchall()
    return render_template("index.html", own_projects=own_projects, public_projects=public_projects) 


@app.route("/project/<int:id>")
@auth_required
def project(id: int):
    sql = "SELECT id, name, owner, published FROM project WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    project_info = result.fetchone()
    
    comment_sql = """SELECT f.id, f.data, f.name
        FROM file f
        JOIN file_project fp ON f.id = fp.file_id
        JOIN project p ON fp.project_id = p.id
        WHERE p.id = :id
    """

    result = db.session.execute(comment_sql, {"id": id})
    files = result.fetchall()

    sql = "SELECT sender, content FROM comment WHERE containing_project=:id"
    result = db.session.execute(sql, {"id": id})
    comments = result.fetchall()
    return render_template("project_view.html", name=project_info.name, project_id=project_info.id, current_files=files, published=project_info.published, comments=comments, is_owner=project_info.owner==session['user_id'])


@app.route("/project/<int:id>/send_publish", methods=["POST"])
@auth_required
def send_publish(id: int):
    published = request.form.get("published") == "selected"

    sql = "UPDATE project SET published=:published WHERE id=:id"
    result = db.session.execute(sql, {"id": id, "published": published})
    db.session.commit()
    print(f"Updated published status for project {id}, new value of publish: {published}")
    return redirect(f"/project/{id}")

# TODO: Does this benefit from ID since it offers change to add file to any project?
@app.route("/add_file/<int:id>")
@auth_required
def add_file(id):
    sql = "SELECT id, name FROM project WHERE owner=:user_id"
    user_id = session["user_id"]
    result = db.session.execute(sql, {"user_id":user_id})
    available_projects = result.fetchall()
    
    available_files = db.session.execute("SELECT id,name FROM file").fetchall()
    return render_template("new_file.html", available_projects=available_projects, available_files=available_files)


@app.route("/send_file", methods=["POST"])
@auth_required
def send_file():
    # FIXME: could we validate here not to send file from same project to same project?
    new_file: Optional[FileStorage] = request.files.get("new_file")
    old_file = request.form.get("old_file")
    project = request.form["project"]

    print(request.files)
    if new_file:
        print("Uploading new file")
        assert new_file

        sql = "INSERT INTO file(owner, data, name) VALUES (:owner, :data, :name) RETURNING id"
        result = db.session.execute(sql, {"owner":session["user_id"], "data":new_file.stream.read(), "name":new_file.filename})

        sql = "INSERT INTO file_project(file_id, project_id) VALUES (:file_id, :project_id)"
        result = db.session.execute(sql, {"file_id": result.first().id, "project_id": project})
        db.session.commit()
        return redirect(f"/project/{project}")

    if old_file:
        print("Appending existing file")
        file = File.query.filter_by(id=old_file).first()
        project_obj.files.append(file)
        db.session.commit()
        return redirect(f"/project/{project}")
    return abort(500)


@app.route("/add_project")
@auth_required
@auth_required
def add_project():
    return render_template("new_project.html")


@app.route("/send_project", methods=["POST"])
@auth_required
def send_project():
    name = request.form["name"]
    try:
        sql = "INSERT INTO project(name, owner) VALUES (:name, :owner)"
        result = db.session.execute(sql, {"name":name, "owner": session["user_id"]})
        db.session.commit()
        print(f"Succesfully created project {name}")
        return redirect("/")
    except BaseException as e:
        print(e)
        # FIXME: this could be any db error
        return render_template("error.html", error="Please select an unique name for your projct")


@app.route("/query_project", methods=["GET"])
@auth_required
def query_project():
    query = request.args["query"]
    sql = "SELECT id, name FROM project WHERE name LIKE :query AND published "
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    projects = result.fetchall()
    return render_template("search_results.html", projects=projects)


@app.route("/project/<int:id>/send_comment", methods=["POST"])
@auth_required
def send_comment(id: int):
    content = request.form["comment"]
    sample_comment = Comment(sender=session["user_id"], containing_project=id, content=content)
    db.session.add(sample_comment)
    db.session.commit()
    return redirect(f"/project/{id}")


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
    session["user_id"] = user.id
    session["is_admin"] = user["is_admin"] == True
    return redirect("/")



@app.route("/logout")
@auth_required
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register")
@auth_required
def register():
    return render_template("register.html")

@app.route("/send_register", methods=["POST"])
@auth_required
def send_register():
    username = request.form["username"]
    email = request.form["email"]
    password = generate_password_hash(request.form["password"])
    try:
        sql = "INSERT INTO app_user(username, password,email) VALUES (:username, :password, :email)"
        result = db.session.execute(sql, {"username":username, "password": password, "email": email})
        db.session.commit()
        return redirect("/")
    except BaseException as e:
        print(e)
        return render_template("error.html", error="Please select an unique username")

if __name__ == "__main__":
    app.run()
