#!/usr/bin/env python3
"""0. Writing strings to Redis
   1. Reading from Redis and recovering original type
   2. Incrementing values
   3. Storing lists
   4. Retrieving lists
"""
import redis
import uuid
from typing import Callable, Union
from functools import wraps


class Cache:
    """A Cache class"""
    def __init__(self):
        """__init__ method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """A store methode should generate a random key (e.g. using uuid)"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: callable = None) -> Union[str, bytes, int, float]:
        """Get data from redis db"""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Get data from cache as string"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """Get data from cache as integer"""
        return self.get(key, int)
