from os import getenv

from flask import Flask
from flask import render_template, session
from flask_sqlalchemy import SQLAlchemy

from . import models
from .helpers import is_admin, logged_in_user

app = Flask(__name__)

# Heroku provides an old postgres format which doesn't work with new SQLAlchemy
REWRITTEN_DATABASE_URL = getenv("DATABASE_URL").replace("postgres://", "postgresql://")
app.config["SQLALCHEMY_DATABASE_URI"] = REWRITTEN_DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)
models.initialize_models(db)

# fmt: off
# This needs to be _after_ the `app` and db are defined to avoid circular import problems
from .routes import file, project, user, audio # pylint: disable=wrong-import-position,unused-import
# fmt: on


@app.route("/")
def index():
    if not logged_in_user(db):
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


if __name__ == "__main__":
    app.run()
