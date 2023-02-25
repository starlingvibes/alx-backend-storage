#!/usr/bin/env python3

"""Writing strings to redis
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Counts how many times methods of the Cache class are called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and outputs for a particular function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper
        """
        self._redis.rpush(method.__qualname__ + ':inputs', str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ':outputs', str(output))
        return output
    return wrapper


class Cache:
    """Cache class
    """

    def __init__(self):
        """Constructor
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Takes a data argument and returns a string
        """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(self, key: str, fn: Union[None, Callable] = None) -> Union[str, bytes, int, float]:
        """Takes a string key argument and an optional callable argument named fn
        """
        if fn is None:
            return self._redis.get(key)
        return fn(self._redis.get(key))

    def get_str(self, key: str) -> str:
        """Takes a string key argument and returns a string
        """
        return self._redis.get(key).decode('utf-8')

    def get_int(self, key: str) -> int:
        """Takes a string key argument and returns an int
        """
        return int(self._redis.get(key))
