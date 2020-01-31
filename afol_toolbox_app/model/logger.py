# coding=utf-8
import logging
import sys

level = logging.DEBUG

_LOG_FORMAT = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [%(module)s ] %(message)s "
_formatter = logging.Formatter(_LOG_FORMAT)

log = logging.Logger("AFOL Toolbox")
_print_handler = logging.StreamHandler(sys.stdout)
_print_handler.setFormatter(_formatter)
_print_handler.setLevel(level)
log.addHandler(_print_handler)
