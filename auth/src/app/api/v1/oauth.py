from http import HTTPStatus

from api.v1.response_code import get_error_response
from flask import (Blueprint, jsonify, render_template, request)
from models import SocialAccount
from services.account import get_account_service as account_service
from services.oauth import OAuthSignIn
from services.user import get_user_service as user_service

oauth_api = Blueprint("oauth_api", __name__)


@oauth_api.route('/')
def index():
    return render_template('index.html')


@oauth_api.route('/authorize/<provider>')
def oauth_authorize(provider):
    # if not current_user.is_anonymous:
    #     return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@oauth_api.route('/callback/<provider>')
def oauth_callback(provider):
    # TODO # Проверка авторизован ли пользователь
    # if not current_user.is_anonymous:
    #     return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, login, email = oauth.callback()

    if social_id is None:
        get_error_response.error("Authentication failed.", status_code=HTTPStatus.UNAUTHORIZED)

    social_account = SocialAccount.query.filter_by(social_id=social_id, social_name=provider).first()

    if not social_account:
        user = user_service.create_oauth(login=login, email=email, social_id=social_id, social_name=provider)

    else:
        user = social_account.user
    login = account_service.login(user=user,
                                  user_agent=request.user_agent,
                                  without_verification=True)
    if login:
        access, refresh = login
        return jsonify(access_token=access, refresh_token=refresh)
    get_error_response.error("Authentication failed.", status_code=HTTPStatus.UNAUTHORIZED)
