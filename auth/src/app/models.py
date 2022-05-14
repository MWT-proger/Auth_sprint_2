from datetime import datetime
from enum import Enum
from uuid import uuid4

from database import db
from flask_security import RoleMixin, UserMixin
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.inspection import inspect


class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"


class DateTimeMixin:
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())


class User(db.Model, DateTimeMixin, UserMixin):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship("Role", secondary="content.roles_users", backref=db.backref("users", lazy="dynamic"))

    def __str__(self):
        return f"User >>> {self.login}"


class Role(db.Model, RoleMixin):
    __tablename__ = "roles"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __str__(self):
        return f"Role >>> {self.name}"

    def serialize(self):
        role = {c: getattr(self, c) for c in inspect(self).attrs.keys()}
        del role["users"]
        return role

    class Meta:
        PROTECTED_ROLE_NAMES = (
            RoleEnum.user,
            RoleEnum.admin,
        )


class RolesUsers(db.Model):
    __tablename__ = "roles_users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("users.id"))
    role_id = db.Column("role_id", UUID(as_uuid=True), db.ForeignKey("roles.id"))

    UniqueConstraint("user_id", "role_id", name="role_user_inx")


class LoginHistory(db.Model):
    __tablename__ = "auth_history"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    datetime = db.Column(db.DateTime, default=datetime.now())
    user_agent = db.Column(db.Text, nullable=False)
    ip = db.Column(db.String(64), nullable=True)


class AuthToken(db.Model):
    __tablename__ = "auth_token"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    user_agent = db.Column(db.Text, nullable=False)
    refresh_token = db.Column(db.Text, nullable=False)


def create_partition(target, connection, **kw) -> None:
    """ creating partition by user_sign_in """
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "social_accounts_yandex" PARTITION OF "social_accounts" FOR VALUES IN ('yandex')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "social_accounts_mail" PARTITION OF "social_accounts" FOR VALUES IN ('mail')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "social_accounts_vk" PARTITION OF "social_accounts" FOR VALUES IN ('vk')"""
    )


class SocialAccount(db.Model):
    __tablename__ = "social_accounts"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("content.users.id"), nullable=False)
    user = db.relationship(User, backref=db.backref("social_accounts", lazy=True))

    social_id = db.Column(db.String(255), nullable=False)
    social_name = db.Column(db.String(255), nullable=False, primary_key=True)

    __table_args__ = (db.UniqueConstraint("social_id", "social_name", name="social_uc"),
                      db.UniqueConstraint("id", "social_name"),
                      {
                          'postgresql_partition_by': 'LIST (social_name)',
                          'listeners': [('after_create', create_partition)],
                      }
                      )

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'


class MultiFactorAuthentication(db.Model):
    __tablename__ = "mf_authentication"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("content.users.id"), nullable=False)
    user = db.relationship(User, backref=db.backref("mf_authentication", lazy=True))

    secret = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean(), default=False)
