import logging.config
import sys
from typing import List, Optional

DEFAULT_FORMATTER = logging.Formatter("[%(asctime)s][%(levelname)8s][%(filename)12s:%(lineno)4s] %(message)s")
SIMPLE_FORMATTER = logging.Formatter("[%(asctime)s][%(levelname)8s] %(message)s")


def handler(hdlr: logging.Handler, formatter: logging.Formatter, level: int = logging.NOTSET):
    hdlr.setFormatter(formatter)
    hdlr.setLevel(level)
    return hdlr


STDOUT_HANDLER = handler(logging.StreamHandler(sys.stdout), DEFAULT_FORMATTER)
STDERR_HANDLER = handler(logging.StreamHandler(sys.stderr), DEFAULT_FORMATTER, logging.WARNING)

_loggers = {}


def init(name: str, *, handlers: Optional[List[logging.Handler]] = None, level: int = logging.INFO) -> logging.Logger:
    if name not in _loggers:
        if handlers is None:
            handlers = [STDOUT_HANDLER]
        logger = logging.getLogger(name)
        for hdlr in handlers:
            if hdlr not in logger.handlers:
                logger.addHandler(hdlr)
        logger.setLevel(level)
        _loggers[name] = logger
    return _loggers[name]
