#!/usr/bin/env python3

"""Writing strings to redis
"""
import redis
import uuid
from typing import Union, Callable


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


cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value
