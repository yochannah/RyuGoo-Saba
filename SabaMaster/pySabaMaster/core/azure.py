#!/usr/bin/python3
# coding: utf-8
from flask_restplus import abort
from pySabaMaster.core.util import Redis, get_logger


r = Redis()
logger = get_logger(__file__)


# TODO ストレージアカウントの作成、アクセスキー
# TODO output base path の確認 blob_base_path
def resister_azure_info(data):
    if "user_name" not in data:
        abort(404, "Pram user_name is None.")
    if "password" not in data:
        abort(404, "Pram password is None.")
    if "subscription" not in data:
        abort(404, "Pram subscription is None.")
    logger.debug("user_name: {}".format(data["user_name"]))
    logger.debug("password: {}".format(data["password"]))
    logger.debug("subscription: {}".format(data["subscription"]))

    storage_account, access_key = get_storage_account(data)
    blob_base_path = get_blob_base_path(storage_account)

    r.set("user_name", data["user_name"])
    r.set("password", data["password"])
    r.set("subscription", data["subscription"])
    r.set("storage_account", storage_account)
    r.set("access_key", access_key)
    r.set("blob_base_path", blob_base_path)

    return {"message": "Complete to post azure info."}


# TODO
def get_storage_account(data):
    return "SA_example", "Access_Key_exa,ple"


# TODO
def get_blob_base_path(storage_account):
    return "blob_base_path_example"
