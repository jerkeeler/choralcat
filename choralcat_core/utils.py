import logging
import random
import time
from functools import wraps
from typing import Callable

from django.utils.text import slugify

from .consts import SLUG_TOKEN_LENGTH, TOKEN_CHARS, TOKEN_LENGTH


def gen_token(token_length: int = TOKEN_LENGTH) -> str:
    return "".join([random.choice(TOKEN_CHARS) for _ in range(token_length)])


def gen_slug(attr: str, max_length: int = 32) -> str:
    token = gen_token(token_length=SLUG_TOKEN_LENGTH)
    slug = slugify(attr)[: max_length - SLUG_TOKEN_LENGTH - 1]
    slug += f"-{token}"
    return slug


def timer(func: Callable) -> Callable:
    """
    Time how long a function takes to run and log it
    :param func: Function to time
    :return: Wrapper function
    """
    logger = logging.getLogger(f"{func.__module__}.{func.__name__}")

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        response = func(*args, **kwargs)
        length = time.time() - start
        logger.info(f"Took {length:.8f} seconds")
        return response

    return wrapper
