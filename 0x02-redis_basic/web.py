#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker
"""
import requests
import redis
from typing import Callable
from functools import wraps

redis_store = redis.Redis()
"""Module level instance of the Redis client
"""


def data_cacher(method: Callable) -> str:
    """caches the output of fetched data
    """
    @wraps(method)
    def wrapper(url) -> str:
        """wrapper function
        """
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """Function that takes in a URL, sends a request to the URL and returns the
    body of the response (decoded in utf-8).
    """
    r = requests.get(url)
    return r.text
