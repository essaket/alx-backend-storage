#!/usr/bin/env python3
"""Module for redis exercise
"""

from unittest.mock import call
import redis
import uuid
from typing import Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a function is called
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a function
    """
    @wraps(method)
    def wrapper(self, *args):
        """Wrapper function
        """
        input = str(args)
        self._redis.rpush(f"{method.__qualname__}:inputs", input)

        output = method(self, *args)
        self._redis.rpush(f"{method.__qualname__}:outputs", output)

        return output
    return wrapper


class Cache:
    """Cache class
    """

    def __init__(self):
        """Constructor method
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in redis db
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: callable = None) -> Union[str, bytes, int, float]:
        """Get data from redis db
        """
        data = self._redis.get(key)
        if data is None:
            return None

        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Get data from cache as string
        """
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """Get data from cache as integer
        """
        return self.get(key, int)


def replay(method: Callable):
    """Replay history of calls to method
    """
    method_name = method.__qualname__
    r = redis.Redis()
    count_key = f"{method_name}"
    inputs_key = f"{method_name}:inputs"
    outputs_key = f"{method_name}:outputs"

    count = r.get(count_key)
    inputs = r.lrange(inputs_key, 0, -1)
    outputs = r.lrange(outputs_key, 0, -1)

    print(f"{method_name} was called {count.decode('utf-8')} times:")

    for input, output in zip(inputs, outputs):
        print(f"{method_name}(*{input.decode('utf-8')}) -> "
              f"{output.decode('utf-8')}")
