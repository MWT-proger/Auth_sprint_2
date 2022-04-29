from api.v1.account import auth_api
from api.v1.response_code import bp_errors
from database import init_db
from datastore import init_datastore
from flask import Flask
from jwt_extended import init_jwt
from ma import init_ma
from swagger import init_swagger
from middlewares import init_token_check

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret"

app.register_blueprint(auth_api, url_prefix='/auth/api/v1/')
app.register_blueprint(bp_errors)

init_token_check(app)
init_db(app)
init_datastore(app)
init_ma(app)
init_jwt(app)
init_swagger(app)

app.app_context().push()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
