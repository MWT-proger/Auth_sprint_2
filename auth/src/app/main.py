from api.v1.account import auth_api
from api.v1.file import file_api
from api.v1.oauth import oauth_api
from api.v1.response_code import bp_errors
from api.v1.role import role_api
from api.v1.user import user_api
from config import Config
from database import init_db
from datastore import init_datastore
from error import handle_exception
from flask import Flask
from jwt_extended import init_jwt
from ma import init_ma
from middlewares import init_rate_limit, init_token_check, init_check_request_id
from oauth import init_oauth
from swagger import init_swagger
from werkzeug.exceptions import HTTPException
from jaeger_tracer import init_jaeger

config = Config()

app = Flask(__name__)
app.config["SECRET_KEY"] = config.APP.SECRET_KEY

app.register_blueprint(auth_api, url_prefix='/auth/api/v1/')
app.register_blueprint(role_api, url_prefix="/auth/role/api/v1")
app.register_blueprint(user_api, url_prefix='/auth/api/v1/users')
app.register_blueprint(oauth_api, url_prefix='/auth/api/v1/oauth')
app.register_blueprint(file_api, url_prefix='/')
app.register_blueprint(bp_errors)

app.register_error_handler(HTTPException, handle_exception)


init_oauth(app)
init_rate_limit(app)
init_token_check(app)
init_check_request_id(app)
init_db(app)
init_datastore(app)
init_ma(app)
init_jwt(app)
init_swagger(app)
init_jaeger(app)

app.app_context().push()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
