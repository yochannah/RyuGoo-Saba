#!/usr/bin/python3
# coding: utf-8
from flask_restplus import abort
from pySabaWorker.core.util import Redis, get_logger


r = Redis()
logger = get_logger(__file__)


def get_job_info():
    if r.exists("SRA_accession_nums") is False:
        abort(404, "Pram SRA_accession_nums is None.")
    if r.exists("CWL_filepaths") is False:
        abort(404, "Pram CWL_filepaths is None.")
    if r.exists("output_base_path") is False:
        abort(404, "Pram output_base_path is None.")
    if r.exists("status") is False:
        abort(404, "Pram status is None.")

    job_info = dict()
    job_info["SRA_accession_nums"] = r.get_list("SRA_accession_nums")
    job_info["CWL_filepaths"] = r.get_list("CWL_filepaths")
    job_info["output_base_path"] = r.get("output_base_path")
    job_info["status"] = r.get("status")
    logger.debug(job_info)

    return job_info


def resister_job_info(data):
    if "SRA_accession_nums" not in data:
        abort(404, "Pram SRA_accession_nums is None.")
    if "CWL_filepaths" not in data:
        abort(404, "Pram CWL_filepaths is None.")
    if "output_base_path" not in data:
        abort(404, "Pram output_base_path is None.")
    logger.debug("SRA_accession_nums: {}".format(data["SRA_accession_nums"]))
    logger.debug("CWL_filepaths: {}".format(data["CWL_filepaths"]))
    logger.debug("output_base_path: {}".format(data["output_base_path"]))

    r.set_list("SRA_accession_nums", data["SRA_accession_nums"])
    r.set_list("CWL_filepaths", data["CWL_filepaths"])
    r.set("output_base_path", data["output_base_path"])
    r.set("status", "Pending")

    # TODO kick cwl pipeline

    return {"message": "Complete to post job info."}
