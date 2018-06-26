#!/usr/bin/python3
# coding: utf-8
from flask import Flask

from pySabaWorker import config
from pySabaWorker.apis import api


def initialize_app():
    app = Flask(__name__)
    api.init_app(app)

    return app


def main():
    app = initialize_app()
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
