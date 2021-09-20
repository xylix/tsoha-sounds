import secrets

from flask import request, render_template, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError

from ..app import app, db


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
    session.clear()
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
