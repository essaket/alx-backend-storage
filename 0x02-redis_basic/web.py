#!/usr/bin/env python3
"""
This module provides a simple web caching system using Redis.
If Redis is not available, the script will still fetch the content but without caching.
"""

import redis
import requests
from functools import wraps
from typing import Callable

# Attempt to connect to Redis
try:
    r = redis.Redis()
    r.ping()  # Check if Redis is available
    redis_available = True
except (redis.exceptions.ConnectionError, redis.exceptions.RedisError):
    redis_available = False
    print("Redis is not available. Caching is disabled.")

def cache_page(func: Callable) -> Callable:
    """
    Decorator that caches the result of the function in Redis with a 10-second expiration time.
    If Redis is not available, caching is skipped.
    Also tracks how many times a particular URL was accessed.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        if redis_available:
            # Increment the access count for the URL
            r.incr(f"count:{url}")

            # Check if the result is cached in Redis
            cached = r.get(url)
            if cached:
                return cached.decode('utf-8')

        # If not cached or Redis not available, fetch the HTML content from the URL
        html_content = func(url)

        if redis_available:
            # Cache the result in Redis with an expiration time of 10 seconds
            r.setex(url, 10, html_content)

        return html_content
    return wrapper

@cache_page
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL.
    """
    response = requests.get(url)
    return response.text
