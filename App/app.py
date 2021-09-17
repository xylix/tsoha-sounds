from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/projects")
def projects():
    pass

@app.route("/upload")
def upload():
    return render_template("submit_file.html")

@app.route("/upload_result", methods=["POST"])
def result():
    data = request.form["file"]
    return data
