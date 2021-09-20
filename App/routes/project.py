from flask import render_template, request, redirect, session


from ..app import app, db
from ..helpers import is_admin, auth_required, form_token_required


@app.route("/project/<int:project_id>")
@auth_required(db)
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
@auth_required(db)
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


@app.route("/add_project")
@auth_required(db)
def add_project():
    return render_template("new_project.html")


@app.route("/send_project", methods=["POST"])
@auth_required(db)
@form_token_required
def send_project():
    name = request.form["name"]
    already_exists = db.session.execute(
        "SELECT id FROM Projects WHERE name=:name", {"name": name}
    ).first()

    if already_exists:
        return render_template(
            "error.html", error="Please select an unique name for your projct"
        )

    sql = "INSERT INTO Projects (name, owner) VALUES (:name, :owner)"
    db.session.execute(sql, {"name": name, "owner": session["user_id"]})
    db.session.commit()
    print(f"Succesfully created project {name}")
    return redirect("/")


@app.route("/query_project", methods=["GET"])
@auth_required(db)
def query_project():
    query = request.args["query"]
    sql = "SELECT id, name FROM Projects WHERE name LIKE :query AND published "
    result = db.session.execute(sql, {"query": "%" + query + "%"})
    projects = result.fetchall()
    return render_template("search_results.html", projects=projects)


@app.route("/project/<int:project_id>/send_comment", methods=["POST"])
@auth_required(db)
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
