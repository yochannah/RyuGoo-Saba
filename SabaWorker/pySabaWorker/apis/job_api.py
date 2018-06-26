#!/usr/bin/python3
# coding: utf-8
from flask_restplus import Resource, Namespace, fields
from pySabaWorker.core.job import get_job_info, resister_job_info

api = Namespace("job", description="Endpoint of job")
job = api.model("Job", {
    "SRA_accession_nums": fields.List(
        fields.String(
            description="SRA accession number",
            example="SRA000001"
        )),
    "CWL_filepaths": fields.List(
        fields.String(
            description="CWL filepath",
            example="https://github.com/Rhelixa-inc/RyuGoo-Saba/blob/develop/tests/cwl_files/hisat2"
        )),
    "output_base_path": fields.String(
        description="Azure blob storage bas",
        example="http://myaccount.blob.core.windows.net/ryugoo-saba/1"
    ),
    "status": fields.String(
        description="Job status",
        example="Running"
    )
})


@api.route("/")
@api.response(404, "The specified resource was not found.")
class Job(Resource):
    @api.doc("Get the job Information")
    @api.marshal_with(job, code=200)
    def get(self):
        return get_job_info(), 200

    @api.doc("Register the job")
    @api.expect(job)
    @api.marshal_with(job, code=201)
    def post(self):
        return resister_job_info(api.payload), 201
