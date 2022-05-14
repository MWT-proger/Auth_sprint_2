from http import HTTPStatus

import pyotp
from api.v1.base import BaseAPI
from api.v1.response_code import get_error_response as error_response
from api.v1.swag import account as swag
from flasgger import swag_from
from flask import Blueprint, jsonify, render_template, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_wtf import FlaskForm
from flask_wtf import RecaptchaField
from models import MultiFactorAuthentication
from schemes.user import UserLoginSchema
from services.account import get_account_service as account_service
from services.auth_token import get_auth_token_service as auth_token_service

auth_api = Blueprint("auth_api", __name__)


class LoginView(BaseAPI):
    schema = UserLoginSchema()
    service = account_service

    @swag_from(swag.login_swagger)
    def post(self):
        data = self.get_data()
        if self.data_validation(data):
            login = data.get("login")
            password = data.get("_password")
            code_2fa = data.get("code_2fa")

            login = self.service.login(login=login, password=password, user_agent=request.user_agent, code_2fa=code_2fa)

            if login:
                access, refresh = login
                return jsonify(access_token=access, refresh_token=refresh)

            self.error("Wrong login or password", status_code=HTTPStatus.UNAUTHORIZED)


@auth_api.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
@swag_from(swag.refresh_token_swagger)
def refresh_token():
    identity = get_jwt_identity()
    authorization = request.headers.get("Authorization")
    old_refresh = authorization.split()[1]

    access_token, new_refresh = auth_token_service.update_refresh_token(user_id=identity, refresh_token=old_refresh)

    if new_refresh and access_token:
        return jsonify(access_token=access_token, refresh_token=new_refresh)

    return error_response.error("Token has been revoked", status_code=HTTPStatus.UNAUTHORIZED)


@auth_api.route("/logout", methods=["POST"])
@jwt_required()
@swag_from(swag.logout_swagger)
def logout():
    user_id = get_jwt_identity()
    jti = get_jwt()["jti"]
    account_service.logout(user_id=user_id, jti=jti, user_agent=request.user_agent)
    return jsonify({"msg": "Success logout."})


@auth_api.route("/full_logout", methods=["POST"])
@jwt_required()
@swag_from(swag.full_logout_swagger)
def full_logout():
    user_id = get_jwt_identity()
    account_service.full_logout(user_id=user_id)
    return jsonify({"msg": "Success logout."})


@auth_api.route("/protected", methods=["GET"])
@jwt_required()
@swag_from(swag.protected_swagger)
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user)


@auth_api.route("/2fa/add", methods=["GET"])
@jwt_required()
def add_2fa():
    current_user = get_jwt_identity()
    mf_auth = account_service.add_or_update_mf_auth(user_id=current_user)

    totp = pyotp.TOTP(mf_auth.secret)
    provisioning_url = totp.provisioning_uri(name=current_user + '@test_project.ru', issuer_name='test_name')

    return render_template('totp_sync_template.html', provisioning_url=provisioning_url)


@auth_api.route("/2fa/confirm", methods=['POST'])
@jwt_required()
def confirm_2fa():

    code_2fa = request.json.get("code_2fa")
    if not code_2fa:
        return error_response.fail({"code_2fa": "Enter a valid 2FA code"}, status_code=HTTPStatus.BAD_REQUEST)

    current_user = get_jwt_identity()
    mf_auth = account_service.get_mf_auth(user_id=current_user)
    if not mf_auth:
        return error_response.error({"msg": "2FA не подключена"}, status_code=HTTPStatus.BAD_REQUEST)

    totp = pyotp.TOTP(mf_auth.secret)

    if not totp.verify(code_2fa):
        return error_response.fail({"code_2fa": "Enter a valid 2FA code"}, status_code=HTTPStatus.BAD_REQUEST)

    account_service.update_mf_auth(mf_auth=mf_auth, status=True)
    return jsonify(msg="2FA successfully connected")


class ContactForm(FlaskForm):
    recaptcha = RecaptchaField()


@auth_api.route('/recaptcha', methods=['GET', 'POST'])
def recaptcha():
    """Метод просто, чтобы проверить работу Recaptcha"""
    form = ContactForm()
    message = ''
    if request.method == 'POST':
        if form.validate_on_submit():
            message = 'Спасибо за заполнение формы!'
        else:
            message = 'Пожалуйста, заполните ReCaptcha!'
    return render_template('recaptcha.html', form=form, msg=message)


auth_api.add_url_rule("/login", view_func=LoginView.as_view("login"), methods=["POST"])
