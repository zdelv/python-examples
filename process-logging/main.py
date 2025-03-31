from concurrent.futures import ProcessPoolExecutor
from types import TracebackType
from typing import override, Self
import log


LOG_LEVEL = log.DEBUG


def init_worker(log_queue: log.LogQueue) -> None:
    log.setup_process_logger(log_queue, log_level=LOG_LEVEL)


def work():
    logger = log.get_logger()
    logger.info("Log from process")
    return 1


if __name__ == "__main__":
    log.setup_main_logger(log_level=LOG_LEVEL)
    logger = log.get_logger()

    logger.info("Test from main thread before starting workers")
    with ProcessPoolExecutor(
        max_workers=2,
        initializer=init_worker,
        initargs=(log.get_queue(),)
    ) as executor:
        fut = executor.submit(work)
        logger.info(fut.result())
