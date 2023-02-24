#!/usr/bin/env python3

"""Writing strings to redis
"""
import redis


class Cache:
    """Cache class
    """

    def __init__(self):
        """Constructor
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data):
        """Takes a data argument and returns a string
        """
        self._redis.set("count", data)
        return self._redis.get("count").decode("utf-8")
