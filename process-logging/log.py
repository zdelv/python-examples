import logging
from logging.handlers import QueueHandler, QueueListener
from multiprocessing import Queue


type LogQueue = Queue[logging.LogRecord]

_shared_queue: LogQueue | None = None
_listener: QueueListener | None = None


NOTSET = logging.NOTSET
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


def get_logger(name: str = "") -> logging.Logger:
    return logging.getLogger(name)


def _setup_logger(handler: logging.Handler | None = None) -> logging.Logger:
    logger = logging.getLogger()
    if not handler:
        handler = logging.StreamHandler()
        fmt = logging.Formatter(f"[%(asctime)s][%(processName)s:%(funcName)s][%(levelname)s] %(message)s")
        handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger


def setup_main_logger(listener: bool = True, log_level: int | None = None) -> None:
    """
    Setup the main logger. If listener is True, the a QueueListener is defined
    at the module level and hooked into all logger handlers.
    """
    global _listener

    logger = _setup_logger()
    if listener and _listener is None:
        queue = get_queue()
        _listener = QueueListener(queue, *logger.handlers)
        _listener.start()
    if log_level:
        logger.setLevel(log_level)
    logger.propagate = False


def setup_process_logger(queue: LogQueue, log_level: int | None = None) -> None:
    """
    Create the base logger and add a queue handler to it. The queue must be
    created in the main process and passed into this process. Use Process init
    functions for this.
    """
    handler = QueueHandler(queue)
    logger = _setup_logger(handler=handler)
    if log_level:
        logger.setLevel(log_level)


def get_queue() -> LogQueue:
    global _shared_queue
    if _shared_queue is None:
        _shared_queue = Queue(maxsize=1000)
    return _shared_queue
