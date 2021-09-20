from flask import make_response

from ..app import app, db
from ..helpers import auth_required


@app.route("/audio/<int:audio_id>")
@auth_required(db)
def audio_file(audio_id: int):

    file = db.session.execute(
        "SELECT id,data,name FROM Files WHERE id=:id", {"id": audio_id}
    ).first()
    print(file)
    print(dir(file))
    response = make_response(bytes(file.data))
    response.headers.set("Content-Type", "audio/mpeg")
    return response
