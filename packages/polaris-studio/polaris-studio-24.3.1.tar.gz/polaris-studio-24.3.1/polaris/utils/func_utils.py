import logging


def can_fail(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logging.warning(f"Function {func.__name__} failed, but we're going to press on anyway", exc_info=True)
            logging.warning(e.args, exc_info=True)

    return inner_function
