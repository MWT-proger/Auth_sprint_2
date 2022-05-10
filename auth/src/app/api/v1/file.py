from flask import render_template, Blueprint

file_api = Blueprint("file_api", __name__)


@file_api.route("/receiver.html")
def receiver_google_oauth():
    return render_template("_receiver.html")
