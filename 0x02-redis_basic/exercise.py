#!/usr/bin/env python3

"""Writing strings to redis
"""
import redis
import uuid
from typing import Union


class Cache:
    """Cache class
    """

    def __init__(self):
        """Constructor
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Takes a data argument and returns a string
        """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

