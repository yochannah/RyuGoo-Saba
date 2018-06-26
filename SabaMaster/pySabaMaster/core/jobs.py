#!/usr/bin/python3
# coding: utf-8
from flask_restplus import abort
from pySabaMaster.core.util import Redis, get_logger
from pySabaMaster.models.JobTable import JobTable
from pySabaMaster import config
from pySabaMaster.models import db

r = Redis()
logger = get_logger(__file__)


def get_job_table():
    job_table = {"jobs": []}
    for row in JobTable.query.all():
        job_table["jobs"].append(row.as_dict())
    logger.debug(job_table)

    return job_table


def resister_job(data):
    if "SRA_accession_nums" not in data:
        abort(404, "Param SRA_accession_nums is None.")
    if "CWL_filepaths" not in data:
        abort(404, "Param CWL_filepaths is None.")
    if "instance_size" not in data:
        instance_size = config.DEFAULT_INSTANCE_SIZE
    else:
        instance_size = data["instance_size"]
    if "disk_size" not in data:
        disk_size = config.DEFAULT_DISK_SIZE
    else:
        disk_size = data["disk_size"]

    logger.debug("SRA_accession_nums: {}".format(data["SRA_accession_nums"]))
    logger.debug("CWL_filepaths: {}".format(data["CWL_filepaths"]))
    logger.debug("instance_size: {}".format(instance_size))
    logger.debug("disk_size: {}".format(disk_size))

    job_id = get_job_id()
    logger.debug("job_id: {}".format(job_id))
    output_base_path, log_path = get_output_base_path(job_id)
    logger.debug("output_base_path: {}".format(output_base_path))
    logger.debug("log_path: {}".format(log_path))

    if "job_name" not in data:
        job_name = "Job_{}".format(job_id)
    else:
        job_name = data["job_name"]
    logger.debug("job_name: {}".format(job_name))

    job = JobTable(job_id=job_id,
                   job_name=job_name,
                   SRA_accession_nums=",".join(data["SRA_accession_nums"]),
                   CWL_filepaths=",".join(data["CWL_filepaths"]),
                   output_base_path=output_base_path,
                   status="Pending",
                   instance_size=instance_size,
                   disk_size=disk_size,
                   log_path=log_path)
    db.session.add(job)
    db.session.commit()

    # TODO kick launch job

    return job.as_dict()


def get_job_info(job_id):
    return JobTable.query.filter_by(job_id=job_id).first_or_404().as_dict()


def delete_job(job_id):
    if exists_job_id(job_id) is False:
        abort(404, "Job ID {} is not found.".format(job_id))
    job = JobTable.query.get(job_id)
    if job.status == "Running":
        # TODO kill VM
        pass
    db.session.delete(job)
    db.session.commit()

    return ""


def get_job_id():
    l_job_id_exists = []
    for row in JobTable.query.order_by(JobTable.job_id).all():
        if row is None:
            break
        l_job_id_exists.append(int(row.job_id))
    job_id = 1
    while True:
        if job_id not in l_job_id_exists:
            break
        job_id += 1

    return job_id


# TODO 中身的な確認
def get_output_base_path(job_id):
    blob_base_path = r.get("blob_base_path")
    output_base_path = blob_base_path + "/{}".format(job_id)
    log_path = output_base_path + "/job.log"

    return output_base_path, log_path


def exists_job_id(job_id):
    l_job_id_exists = []
    for row in JobTable.query.all():
        if row is None:
            break
        l_job_id_exists.append(int(row.job_id))
    if job_id in l_job_id_exists:
        return True

    return False
