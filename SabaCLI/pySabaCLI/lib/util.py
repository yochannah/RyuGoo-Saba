#!/usr/bin/python3
# coding: utf-8
import shlex
import sys
from logging import DEBUG, INFO, Formatter, StreamHandler, getLogger
from subprocess import PIPE, Popen

from pySabaCLI import config


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


def debug_arg(logger, arg_name, arg):
    logger.debug("{}: {}".format(arg_name, arg))


logger = get_logger(__file__)


def shell_execute(cmd, flush=True):
    """
    Input: str or list
    Output: status=int, stdout=unicode, stderr=unicode
    """
    if isinstance(cmd, str):
        logger.debug(cmd)
        pass
    elif isinstance(cmd, list):
        logger.debug(cmd)
        cmd = " ".join(map(str, cmd))
    else:
        logger.debug("Input str or list")
        sys.exit(1)
    l_cmd = shlex.split(cmd)

    proc = Popen(l_cmd, stdout=PIPE, stderr=PIPE)
    if flush:
        stdout = []
        while proc.poll() is None:
            out = proc.stdout.readline().decode("utf-8")
            sys.stdout.write(out)
            sys.stdout.flush()
            stdout.append(out)
        stdout = "".join(stdout)
        stderr = proc.communicate()[1]
        stderr = stderr.decode("utf-8")
    else:
        stdout, stderr = proc.communicate()
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")

    status = int(proc.returncode)
    logger.debug("status: {}".format(status))
    if config.DEBUG:
        logger.debug("=== stdout ===")
        print(stdout)
        logger.debug("=== stderr ===")
        print(stderr)

    return status, stdout, stderr
