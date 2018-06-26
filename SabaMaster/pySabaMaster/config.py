#!/usr/bin/python3
# coding: utf-8
DEBUG = True
PORT = 8080
HOST = "0.0.0.0"
SQLALCHEMY_DATABASE_URI = \
    "postgresql+psycopg2://postgres:passwd@postgres:5432/postgres?client_encoding=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEFAULT_INSTANCE_SIZE = "Standard_D2_v3"
DEFAULT_DISK_SIZE = "30GB"
