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

def replay(method: Callable) -> None:
    """doc doc class"""
    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)

    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    print("{} was called {} times:".format(method.__qualname__, len(inputs)))
    for inp, out in zip(inputs, outputs):
        print(
            "{}(*{}) -> {}".format(
                method.__qualname__, inp.decode("utf-8"), out.decode("utf-8")
            )
        )

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
