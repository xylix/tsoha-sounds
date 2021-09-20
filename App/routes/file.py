from typing import Optional

from flask import render_template, session, request, redirect
from werkzeug.exceptions import abort
from werkzeug.datastructures import FileStorage


from ..helpers import auth_required, form_token_required
from ..app import app, db


@app.route("/add_file")
@auth_required(db)
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
@auth_required(db)
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
