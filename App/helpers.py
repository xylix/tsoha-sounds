from functools import wraps

from flask import render_template, request, session
from werkzeug.exceptions import abort


def logged_in_user(db) -> bool:
    if not session.get("user_id"):
        # There is no active session
        return False

    sql = "SELECT id FROM AppUsers WHERE id=:id"
    if not db.session.execute(sql, {"id": session.get("user_id")}).first():
        # Session has expired or comes from older database instance, delete it
        session.clear()
        return False
    return True


def is_admin():
    return session.get("is_admin")


def auth_required(db):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kws):
            allow = False
            if is_admin():
                allow = True
            elif logged_in_user(db):
                allow = True
            if not allow:
                return render_template("error.html", error="Ei oikeutta nähdä sivua")
            return func(*args, **kws)

        return decorated_function

    return decorator


def form_token_required(func):
    @wraps(func)
    def decorated_function(*args, **kws):
        if session.get("csrf_token") != request.form["csrf_token"]:
            return abort(403)
        else:
            return func(*args, **kws)

    return decorated_function
