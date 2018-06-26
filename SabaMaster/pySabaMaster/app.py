#!/usr/bin/python3
# coding: utf-8
from flask import Flask

from pySabaMaster import config
from pySabaMaster.apis import api
from pySabaMaster.models import db


def initialize_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = \
        config.SQLALCHEMY_TRACK_MODIFICATIONS
    api.init_app(app)
    db.init_app(app)
    db.create_all(app=app)

    return app


def main():
    app = initialize_app()
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
