import json
import random
from abc import ABC, abstractmethod

from flask import current_app, redirect, request, session, url_for
from rauth import OAuth1Service, OAuth2Service


class OAuthSignIn(ABC):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config["OAUTH_CREDENTIALS"][provider_name]
        self.consumer_id = credentials["id"]
        self.consumer_secret = credentials["secret"]

    @property
    @abstractmethod
    def authorize(self):
        pass

    @property
    @abstractmethod
    def callback(self):
        pass

    def get_callback_url(self):

        return url_for("oauth_api.oauth_callback", provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class YandexSignIn(OAuthSignIn):
    def __init__(self):
        super(YandexSignIn, self).__init__("yandex")
        self.service = OAuth2Service(
            name="yandex",
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url="https://oauth.yandex.ru/authorize",
            access_token_url="https://oauth.yandex.ru/token",
            base_url="https://oauth.yandex.ru"
        )

    def authorize(self):
        print(self.get_callback_url())
        return redirect(self.service.get_authorize_url(
            scope="login:email login:info",
            response_type="code",
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode("utf-8"))

        if "code" not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={"code": request.args["code"],
                  "response_type": "code",
                  "grant_type": "authorization_code",
                  "redirect_uri": self.get_callback_url()},
            decoder=decode_json
        )
        info = oauth_session.get(url="https://login.yandex.ru/info").json()
        social_id = info.get("id")
        login = info.get("login")
        email = info.get("default_email")
        return social_id, login, email


class MailSignIn(OAuthSignIn):
    state = None

    def __init__(self):
        super(MailSignIn, self).__init__("mail")
        self.service = OAuth2Service(
            name="mail",
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url="https://oauth.mail.ru/login",
            access_token_url="https://oauth.mail.ru/token",
            base_url="https://oauth.mail.ru"
        )

    def authorize(self):
        print(self.get_callback_url())

        self.state = str(random.getrandbits(256))
        return redirect(self.service.get_authorize_url(
            response_type="code",
            scope="userinfo",
            state=self.state,
            prompt_force="prompt_force",
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode("utf-8"))

        if "code" not in request.args:
            return None, None, None
        if request.args["state"] != self.state:
            return None
        oauth_session = self.service.get_auth_session(
            data={"code": request.args["code"],
                  "grant_type": "authorization_code",
                  "redirect_uri": self.get_callback_url()},
            decoder=decode_json
        )
        info = oauth_session.get('userinfo', params={"access_token": oauth_session.access_token}).json()
        social_id = info.get("id")
        login = info.get("email").split('@')[0]
        email = info.get("email")
        return social_id, login, email


class VKSignIn(OAuthSignIn):
    state = None

    def __init__(self):
        super(VKSignIn, self).__init__("vk")
        self.service = OAuth2Service(
            name="vk",
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url="https://oauth.vk.com/authorize",
            access_token_url="https://oauth.vk.com/access_token",
            base_url="https://oauth.vk.com"
        )

    def authorize(self):
        print(self.get_callback_url())

        self.state = str(random.getrandbits(256))
        return redirect(self.service.get_authorize_url(
            response_type="code",
            scope="email",
            state=self.state,
            display="page",
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode("utf-8"))

        if "code" not in request.args:
            return None, None, None
        if request.args["state"] != self.state:
            return None
        info = self.service.get_raw_access_token(
            data={"code": request.args["code"],
                  "grant_type": "authorization_code",
                  "redirect_uri": self.get_callback_url()}
        )
        info = info.json()
        social_id = str(info.get("user_id"))
        login = info.get("email").split('@')[0]
        email = info.get("email")
        return social_id, login, email

