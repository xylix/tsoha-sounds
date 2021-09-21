from os import getenv
import secrets

from werkzeug.security import generate_password_hash

from App.app import db as database


def insert_file(user_id: int, project_id: int):
    FILENAME = "sample_track.mp3"
    with open(f"./{FILENAME}", "rb") as file:
        mp3_data = file.read()
    files_insert_sql = "INSERT INTO Files(owner, data, name) VALUES (:owner, :data, :name) RETURNING id"
    files_result = database.session.execute(
        files_insert_sql,
        {
            "owner": user_id,
            "data": mp3_data,
            "name": FILENAME,
        },
    )

    fp_insert_sql = (
        "INSERT INTO FileProject(file_id, project_id) VALUES (:file_id, :project_id)"
    )
    database.session.execute(
        fp_insert_sql,
        {"file_id": files_result.first().id, "project_id": project_id},
    )


def insert_project(user_id: int) -> int:
    sql = "INSERT INTO Projects (name, owner) VALUES (:name, :owner) RETURNING id"
    result = database.session.execute(
        sql, {"name": "Esimerkkiprojekti", "owner": user_id}
    )
    return result.first().id


def insert_user() -> int:
    # If the env var is not set, set a random generated PW for the admin account
    admin_pw = getenv("ADMIN_PASSWORD") or secrets.token_hex(16)
    sql = "INSERT INTO AppUsers(username, password,email) VALUES (:username, :password, :email) RETURNING id"
    result = database.session.execute(
        sql,
        {
            "username": "admin",
            "email": "admin@/dev/null",
            "password": generate_password_hash(admin_pw),
            "is_admin": True,
        },
    )
    return result.first().id


def insert_comment(sender_id: int, project_id: int):
    sql = "INSERT INTO Comments(sender, containing_project, content) VALUES (:sender,:containing_project,:content)"
    database.session.execute(
        sql,
        {
            "sender": sender_id,
            "containing_project": project_id,
            "content": "Eka testikommentti",
        },
    )


if __name__ == "__main__":
    user_id = insert_user()
    project_id = insert_project(user_id)
    insert_file(user_id, project_id)
    insert_comment(user_id, project_id)
    database.session.commit()
