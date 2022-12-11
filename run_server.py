import os
import json
import pathlib
import tempfile
import pickle
from utils import process_input
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    abort,
    send_from_directory,
    url_for,
)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = (pathlib.Path(".") / "uploads").resolve()
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # Limit uploads to 25 MB.
app.config["PREFERRED_URL_SCHEME"] = "https"
app.add_url_rule("/uploads/<name>", endpoint="uploads", build_only=True)



@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/uploads/<name>")
def uploads(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.after_request
def close_connection(resp):
    resp.headers["Connection"] = "close"
    return resp


@app.route("/api/submit", methods=["POST"])
def submit_video_api():
    if "file" not in request.files:
        return abort(400)

    _, path = tempfile.mkstemp(prefix="in", dir=app.config["UPLOAD_FOLDER"])

    try:
        data = request.files["file"]
        data.save(path)
        print("file saved...", path)
        output_name = process_input(path)
    finally:
        Path(path).unlink()

    return redirect(url_for("uploads", name=output_name))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True, threaded=True)



