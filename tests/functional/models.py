from datetime import datetime
from enum import Enum
from uuid import uuid4

from flask_security import RoleMixin, UserMixin
from functional.config import DatabaseConfig
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, MetaData,
                        String, Text, UniqueConstraint, create_engine)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import backref, relationship

db_config = DatabaseConfig()
metadata_obj = MetaData(schema=db_config.SCHEMA)
Base = declarative_base(db_config.ENGINE, metadata=metadata_obj)


class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"


class DateTimeMixin:
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())


class User(Base, DateTimeMixin, UserMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login = Column(String(128), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    _password = Column("password", String(255), nullable=False)
    active = Column(Boolean(), default=True)
    roles = relationship("Role", secondary="content.roles_users", backref=backref("users", lazy="dynamic"))

    def __str__(self):
        return f"User >>> {self.login}"


class Role(Base, RoleMixin):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(64), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

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


class RolesUsers(Base):
    __tablename__ = "roles_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"))
    role_id = Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id"))

    UniqueConstraint("user_id", "role_id", name="role_user_inx")


class LoginHistory(Base):
    __tablename__ = "auth_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    datetime = Column(DateTime, default=datetime.now())
    user_agent = Column(Text, nullable=False)
    ip = Column(String(64), nullable=True)


class AuthToken(Base):
    __tablename__ = "auth_token"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user_agent = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=False)


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("content.users.id"), nullable=False)
    user = relationship(User, backref=backref("social_accounts", lazy=True))

    social_id = Column(String(255), nullable=False)
    social_name = Column(String(255), nullable=False)

    __table_args__ = (UniqueConstraint("social_id", "social_name", name="social_uc"), )

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'


class MultiFactorAuthentication(Base):
    __tablename__ = "mf_authentication"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("content.users.id"), nullable=False)
    user = relationship(User, backref=backref("mf_authentication", lazy=True))

    secret = Column(String(255), nullable=False)
    status = Column(Boolean(), default=False)
