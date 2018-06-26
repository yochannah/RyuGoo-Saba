#!/usr/bin/python3
# coding: utf-8
from flask_restplus import Resource, Namespace

api = Namespace("Admin", description="Endpoint of admin")


@api.route("/")
@api.response(404, "The specified resource was not found.")
class Root(Resource):
    @api.doc("Confirm existence of API server")
    def get(self):
        return "RSS server is running.", 200
