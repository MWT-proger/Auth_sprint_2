from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flasgger import Swagger


from datastore import init_datastore
from database import init_db
from models import *
from api.v1.account import auth_api

app = Flask(__name__)


#TODO Временно здесь
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWTManager(app)

app.register_blueprint(auth_api, url_prefix='/auth/api/v1/')


@app.get("/")
def hello():
    return jsonify({"message": "Hello world"})


swagger = Swagger(app)
init_db(app)
init_datastore(app)

app.app_context().push()
db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
