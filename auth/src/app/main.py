from database import init_db
from datastore import init_datastore
from flask import Flask, jsonify
from models import *

app = Flask(__name__)


@app.get("/")
def hello():
    return jsonify({"message": "Hello world"})


init_db(app)
init_datastore(app)

app.app_context().push()
db.create_all()
