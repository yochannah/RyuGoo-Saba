#!/usr/bin/python3
# coding: utf-8
from flask_restplus import Resource, Namespace, fields
from pySabaMaster.core.azure import resister_azure_info

api = Namespace("azure", description="Endpoint of azure")
azure = api.model("Azure", {
    "user_name": fields.String(
        description="Azure User Name",
        example="user_name"
    ),
    "password": fields.String(
        description="Azure User Password",
        example="password"
    ),
    "subscription": fields.String(
        description="Azure Subscription",
        example="subscription"
    )
})


@api.route("/")
@api.response(404, "The specified resource was not found.")
class Azure(Resource):
    @api.doc("Post azure infomation.")
    @api.expect(azure)
    def post(self):
        return resister_azure_info(api.payload), 201
