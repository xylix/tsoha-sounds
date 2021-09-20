from functools import wraps
from os import getenv
from typing import Optional
import secrets

from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from . import models

app = Flask(__name__)

# Heroku provides an old postgres format which doesn't work with new SQLAlchemy
REWRITTEN_DATABASE_URL = getenv("DATABASE_URL").replace("postgres://", "postgresql://")
app.config["SQLALCHEMY_DATABASE_URI"] = REWRITTEN_DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)
models = models.initialize_models(db)


def logged_in_user() -> bool:
    if not session.get("user_id"):
        # There is no active session
        return False

    sql = "SELECT id FROM AppUsers WHERE id=:id"
    if not db.session.execute(sql, {"id": session.get("user_id")}).first():
        # Session has expired or comes from older database instance, delete it
        logout()
        return False
    return True


def is_admin():
    return session.get("is_admin")


def auth_required(func):
    @wraps(func)
    def decorated_function(*args, **kws):
        allow = False
        if is_admin():
            allow = True
        elif logged_in_user():
            allow = True
        if not allow:
            return render_template("error.html", error="Ei oikeutta nähdä sivua")
        return func(*args, **kws)

    return decorated_function


def form_token_required(func):
    @wraps(func)
    def decorated_function(*args, **kws):
        if session.get("csrf_token") != request.form["csrf_token"]:
            return abort(403)
        else:
            return func(*args, **kws)

    return decorated_function


@app.route("/")
def index():
    if not logged_in_user():
        return render_template("index.html")

    if is_admin():
        result = db.session.execute(
            "SELECT name,id FROM Projects WHERE NOT owner = :user_id",
            {"user_id": session["user_id"]},
        )
    else:
        result = db.session.execute(
            "SELECT name,id FROM Projects WHERE NOT owner = :user_id AND published=True",
            {"user_id": session["user_id"]},
        )
    public_projects = result.fetchall()
    own_projects = db.session.execute(
        "SELECT name,id FROM Projects WHERE owner=:id", {"id": session["user_id"]}
    ).fetchall()
    return render_template(
        "index.html", own_projects=own_projects, public_projects=public_projects
    )


@app.route("/project/<int:project_id>")
@auth_required
def project(project_id: int):
    # FIXME: combine the queries?
    projects_sql = "SELECT id, name, owner, published FROM Projects WHERE id=:id"
    result = db.session.execute(projects_sql, {"id": project_id})
    project_info = result.fetchone()

    files_sql = """SELECT f.id, f.data, f.name
        FROM Files f
        JOIN FileProject fp ON f.id = fp.file_id
        JOIN Projects p ON fp.project_id = p.id
        WHERE p.id = :id
    """
    result = db.session.execute(files_sql, {"id": project_id})
    files = result.fetchall()

    comments_sql = """SELECT AppUsers.username, Comments.sender, Comments.content
        FROM Comments 
        INNER JOIN AppUsers
        ON AppUsers.id = Comments.sender
        WHERE containing_project=:id"""
    result = db.session.execute(comments_sql, {"id": project_id})
    comments = result.fetchall()
    allowed_to_modify = project_info.owner == session["user_id"] or is_admin()
    return render_template(
        "project_view.html",
        name=project_info.name,
        project_id=project_info.id,
        current_files=files,
        published=project_info.published,
        comments=comments,
        allowed_to_modify=allowed_to_modify,
    )


@app.route("/project/<int:project_id>/send_publish", methods=["POST"])
@auth_required
@form_token_required
def send_publish(project_id: int):
    published = request.form.get("published") == "selected"

    sql = "UPDATE Projects SET published=:published WHERE id=:id"
    db.session.execute(sql, {"id": project_id, "published": published})
    db.session.commit()
    print(
        f"Updated published status for project {project_id}, new value of publish: {published}"
    )
    return redirect(f"/project/{project_id}")


@app.route("/add_file")
@auth_required
def add_file():
    sql = "SELECT id, name FROM Projects WHERE owner=:user_id"
    user_id = session["user_id"]
    result = db.session.execute(sql, {"user_id": user_id})
    available_projects = result.fetchall()

    available_files = db.session.execute("SELECT id,name FROM Files").fetchall()
    return render_template(
        "new_file.html",
        available_projects=available_projects,
        available_files=available_files,
    )


@app.route("/send_file", methods=["POST"])
@auth_required
@form_token_required
def send_file():
    new_file: Optional[FileStorage] = request.files.get("new_file")
    old_file = request.form.get("old_file")
    project_id = request.form["project"]

    print(request.files)
    if new_file:
        print("Uploading new file")
        assert new_file

        files_insert_sql = "INSERT INTO Files(owner, data, name) VALUES (:owner, :data, :name) RETURNING id"
        files_result = db.session.execute(
            files_insert_sql,
            {
                "owner": session["user_id"],
                "data": new_file.stream.read(),
                "name": new_file.filename,
            },
        )

        fp_insert_sql = "INSERT INTO FileProject(file_id, project_id) VALUES (:file_id, :project_id)"
        db.session.execute(
            fp_insert_sql,
            {"file_id": files_result.first().id, "project_id": project_id},
        )
        db.session.commit()
        return redirect(f"/project/{project_id}")
    elif old_file:
        # FIXME: could we validate here not to send file from same project to same project?
        print("Appending existing file")

        fp_insert_sql = "INSERT INTO FileProject(file_id, project_id) VALUES (:file_id, :project_id)"
        db.session.execute(
            fp_insert_sql, {"file_id": old_file, "project_id": project_id}
        )
        db.session.commit()
        return redirect(f"/project/{project_id}")
    return abort(500)


@app.route("/add_project")
@auth_required
def add_project():
    return render_template("new_project.html")


@app.route("/send_project", methods=["POST"])
@auth_required
@form_token_required
def send_project():
    name = request.form["name"]
    try:
        sql = "INSERT INTO Projects (name, owner) VALUES (:name, :owner)"
        db.session.execute(sql, {"name": name, "owner": session["user_id"]})
        db.session.commit()
        print(f"Succesfully created project {name}")
        return redirect("/")
    except IntegrityError as error:
        print(error)
        # FIXME: this could be any integrity error
        return render_template(
            "error.html", error="Please select an unique name for your projct"
        )


@app.route("/query_project", methods=["GET"])
@auth_required
def query_project():
    query = request.args["query"]
    sql = "SELECT id, name FROM Projects WHERE name LIKE :query AND published "
    result = db.session.execute(sql, {"query": "%" + query + "%"})
    projects = result.fetchall()
    return render_template("search_results.html", projects=projects)


@app.route("/project/<int:project_id>/send_comment", methods=["POST"])
@auth_required
@form_token_required
def send_comment(project_id: int):
    content = request.form["comment"]
    sql = "INSERT INTO Comments(sender, containing_project, content) VALUES (:sender,:containing_project,:content)"
    db.session.execute(
        sql,
        {
            "sender": session["user_id"],
            "containing_project": project_id,
            "content": content,
        },
    )
    db.session.commit()
    return redirect(f"/project/{project_id}")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    print(f"Querying for user with username: {username}")
    # Check username and password
    sql = "SELECT id, password, is_admin FROM AppUsers WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.first()
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
    session["is_admin"] = user["is_admin"] is True
    session["csrf_token"] = secrets.token_hex(16)
    return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    del session["is_admin"]
    del session["csrf_token"]
    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/send_register", methods=["POST"])
def send_register():
    username = request.form["username"]
    email = request.form["email"]
    password = generate_password_hash(request.form["password"])
    try:
        sql = "INSERT INTO AppUsers(username, password,email) VALUES (:username, :password, :email)"
        db.session.execute(
            sql, {"username": username, "password": password, "email": email}
        )
        db.session.commit()
        return redirect("/")
    except IntegrityError as error:
        print(error)
        return render_template("error.html", error="Please select an unique username")


if __name__ == "__main__":
    app.run()
