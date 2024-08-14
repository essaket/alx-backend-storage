#!/usr/bin/env python3
"""
This module provides a simple web caching system using Redis.
"""

import redis
import requests
from functools import wraps
from typing import Callable

# Connect to the local Redis instance
r = redis.Redis()

def cache_page(func: Callable) -> Callable:
    """
    Decorator that caches the result of the function in Redis with a 10-second expiration time.
    Also tracks how many times a particular URL was accessed.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        # Increment the access count for the URL
        r.incr(f"count:{url}")

        # Check if the result is cached in Redis
        cached = r.get(url)
        if cached:
            return cached.decode('utf-8')

        # If not cached, fetch the HTML content from the URL
        html_content = func(url)

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

if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk/delay/3000/url/https://example.com"
    
    # Fetch the page multiple times to test caching and access counting
    print(get_page(test_url))
    print(get_page(test_url))

    # Print the access count for the URL
    print(f"Access count for {test_url}: {r.get(f'count:{test_url}').decode('utf-8')}")
