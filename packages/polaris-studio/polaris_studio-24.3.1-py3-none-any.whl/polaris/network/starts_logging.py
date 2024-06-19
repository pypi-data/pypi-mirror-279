import logging


def starts_logging():
    polaris_logger = logging.getLogger("polaris")
    polaris_logger.setLevel(logging.INFO)
    return polaris_logger


logger = starts_logging()
