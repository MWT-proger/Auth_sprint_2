from flask import Flask, jsonify
from database import init_db

app = Flask(__name__)


@app.get("/")
def hello():
    return jsonify({"message": "Hello world"})


init_db(app)

app.app_context().push()
