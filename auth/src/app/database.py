from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy import MetaData

config = Config()
metadata = MetaData(schema=config.DB.SCHEMA)

db = SQLAlchemy(metadata=metadata)


def init_db(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = config.DB.URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.DB.TRACK_MODIFICATIONS

    db.init_app(app)
