#!/usr/bin/python3
# coding: utf-8
from flask_restplus import abort
from pySabaWorker.core.util import Redis, get_logger


r = Redis()
logger = get_logger(__file__)


def resister_blob_info(data):
    if "storage_account" not in data:
        abort(404, "Pram storage_account is None.")
    if "access_key" not in data:
        abort(404, "Pram access_key is None.")
    logger.debug("storage_account: {}".format(data["storage_account"]))
    logger.debug("access_key: {}".format(data["access_key"]))

    r.set("storage_account", data["storage_account"])
    r.set("access_key", data["access_key"])

    return {"message": "Complete to post blob info."}
