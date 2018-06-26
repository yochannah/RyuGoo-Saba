#!/usr/bin/python3
# coding: utf-8
import redis
from logging import getLogger, INFO, DEBUG, StreamHandler, Formatter
from pySabaMaster import config


class Redis:
    def __init__(self):
        self.r = redis.StrictRedis(host="redis", port=6379, db=0)

    def set(self, key, value):
        return self.r.set(key, value)

    def get(self, key):
        return self.r.get(key).decode()

    def delete(self, key):
        return self.r.delete(key)

    def set_list(self, key, lst):
        try:
            self.r.delete(key)
            for ele in lst:
                self.r.rpush(key, ele)
            return True
        except:
            return False

    def get_list(self, key):
        ret_list = []
        try:
            for val in self.r.lrange(key, 0, -1):
                ret_list.append(val.decode())
            if len(ret_list) == 0:
                return None
            return ret_list
        except:
            return False

    def exists(self, key):
        return self.r.exists(key)


def get_logger(logger_name):
    logger = getLogger(logger_name)
    stream_handler = StreamHandler()
    if config.DEBUG:
        logger.setLevel(DEBUG)
        stream_handler.setLevel(DEBUG)
    else:
        logger.setLevel(INFO)
        stream_handler.setLevel(INFO)
    handler_format = \
        Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(handler_format)
    logger.addHandler(stream_handler)

    return logger
