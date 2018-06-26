#!/usr/bin/python3
# coding: utf-8
from flask_restplus import Resource, Namespace, fields
from pySabaMaster.core.jobs import get_job_table, resister_job, get_job_info, delete_job


api = Namespace("jobs", description="Endpoint of jobs")

dict_job = {
    "job_id": fields.Integer(
        description="Job ID",
        example=1
    ),
    "job_name": fields.String(
        description="Job Name",
        example="bowtie2-pipeline"
    ),
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
        description="Azure blob storage base",
        example="http://myaccount.blob.core.windows.net/ryugoo-saba/1"
    ),
    "status": fields.String(
        description="Job status",
        example="Running"
    ),
    "instance_size": fields.String(
        description="Instance Size",
        example="Standard_D2_v3"
    ),
    "disk_size": fields.String(
        description="Disk Size",
        example="40GB"
    ),
    "log_path": fields.String(
        description="Log path",
        example="http://myaccount.blob.core.windows.net/ryugoo-saba/1/job.log"
    ),
    "start_timestamp": fields.String(
        description="Start Timestamp",
        example="Wed, 02 Oct 2002 13:00:00 GMT"
    ),
    "finish_timestamp": fields.String(
        description="Finish Timestamp",
        example="Wed, 02 Oct 2002 17:00:00 GMT"
    )
}
job = api.model("Job", dict_job)

dict_jobs = {
    "jobs": fields.List(
        fields.Nested(job)
    )
}
jobs = api.model("Jobs", dict_jobs)


@api.route("/")
@api.response(404, "The specified resource was not found.")
class JobTable(Resource):
    @api.doc("Output the registered job table")
    @api.marshal_with(jobs, code=200)
    def get(self):
        return get_job_table(), 200

    @api.doc("Register job")
    @api.expect(job)
    @api.marshal_with(job, code=201)
    def post(self):
        return resister_job(api.payload), 201


@api.route("/<int:job_id>")
@api.response(404, "The specified resource was not found.")
class Job(Resource):
    @api.doc("Get the job Information")
    @api.marshal_with(job, code=200)
    def get(self, job_id):
        return get_job_info(job_id), 200

    @api.doc("Register the job")
    @api.marshal_with(job, code=201)
    def delete(self, job_id):
        return delete_job(job_id), 204
