#!/usr/bin/python3
# coding: utf-8
from flask_restplus import Resource, Namespace, fields
from pySabaWorker.core.blob import resister_blob_info

api = Namespace("blob", description="Endpoint of blob")
blob = api.model("Blob", {
    "storage_account": fields.String(
        description="Azure Storage Account",
        example="storage_account"
    ),
    "access_key": fields.String(
        description="Azure Blob Storage Access Key",
        example="access_key"
    )
})


@api.route("/")
@api.response(404, "The specified resource was not found.")
class Blob(Resource):
    @api.doc("Post azure blob storage infomation.")
    @api.expect(blob)
    def post(self):
        return resister_blob_info(api.payload), 201
