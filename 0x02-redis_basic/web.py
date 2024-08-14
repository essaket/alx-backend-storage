#!/usr/bin/env python3
"""Module for redis exercise with fallback in case Redis is not available.
"""

import requests
import redis

# Try to connect to Redis, but handle the case where Redis isn't available.
try:
    r = redis.Redis()
    r.ping()  # Check if Redis is available
    redis_available = True
    print("Redis connected successfully.")
except (redis.exceptions.ConnectionError, redis.exceptions.RedisError) as e:
    redis_available = False
    print(f"Redis connection failed: {e}. Caching is disabled.")


def get_page(url: str) -> str:
    """Get the HTML content of a particular URL and return it.
       If Redis is available, cache the content and track access count.
    """
    if redis_available:
        try:
            # Increment the access count for the URL
            r.incr(f"count:{url}")

            # Check if the result is cached in Redis
            cached = r.get(url)
            if cached:
                return cached.decode('utf-8')
        except redis.exceptions.RedisError as e:
            print(f"Error with Redis: {e}. Continuing without caching.")

    # If not cached or Redis is unavailable, fetch the HTML content from the URL
    html_content = requests.get(url).text

    if redis_available:
        try:
            # Cache the result in Redis with an expiration time of 10 seconds
            r.setex(url, 10, html_content)
        except redis.exceptions.RedisError as e:
            print(f"Error with Redis while caching: {e}. Continuing without caching.")

    return html_content
