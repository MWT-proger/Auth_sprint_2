from contextlib import contextmanager

from config import get_config as config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(schema=config.DB.SCHEMA)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()


def init_db(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = config.DB.URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.DB.TRACK_MODIFICATIONS

    db.init_app(app)
    migrate.init_app(app, db)


@contextmanager
def session_scope():
    try:
        yield db.session
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
