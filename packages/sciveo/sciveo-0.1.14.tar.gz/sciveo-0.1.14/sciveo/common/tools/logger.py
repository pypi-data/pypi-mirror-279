#
# Pavlin Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact pavlin@softel.bg.
#
# 2023
#

import os
import logging
import traceback
from threading import Lock

from sciveo.common.tools.configuration import GlobalConfiguration


SCIVEO_LOGGER_NAME = "sciveo-log"

_sciveo_global_config = GlobalConfiguration.get()
_sciveo_log_min_level = _sciveo_global_config["LOG_MIN_LEVEL"]
_sciveo_log_lock = Lock()

def _sciveo_get_logger(name):
  logger = logging.getLogger(name)
  if not logger.hasHandlers():
    with _sciveo_log_lock:
      if not logger.hasHandlers():
        logger.setLevel(logging.getLevelName(_sciveo_log_min_level))
        formatter = logging.Formatter('%(asctime)s [%(thread)d] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.propagate = False
  return logger

def debug(*args):
  _sciveo_get_logger(SCIVEO_LOGGER_NAME).debug(args)
def info(*args):
  _sciveo_get_logger(SCIVEO_LOGGER_NAME).info(args)
def warning(*args):
  _sciveo_get_logger(SCIVEO_LOGGER_NAME).warning(args)
def error(*args):
  _sciveo_get_logger(SCIVEO_LOGGER_NAME).error(args)
def critical(*args):
  _sciveo_get_logger(SCIVEO_LOGGER_NAME).critical(args)
def exception(e, *args):
  e_str = ''.join(traceback.format_tb(e.__traceback__))
  _sciveo_get_logger(SCIVEO_LOGGER_NAME).error(e_str, args)