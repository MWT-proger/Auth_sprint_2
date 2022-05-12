from flask import Blueprint, render_template

file_api = Blueprint("file_api", __name__)


@file_api.route("/receiver.html")
def receiver_mail_oauth():
    return render_template("_receiver.html")
