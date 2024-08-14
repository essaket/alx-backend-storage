#!/usr/bin/env python3
"""okokokokokokokokokok"""
import requests
import redis
from functools import wraps
from cachetools import TTLCache, cached

# Connect to Redis (ensure you have Redis running locally or provide your Redis connection details)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Create an in-memory cache with a TTL of 10 seconds for caching page content
cache = TTLCache(maxsize=100, ttl=10)

# Decorator to handle counting and caching
def cache_page(func):
    @wraps(func)
    def wrapper(url):
        # Increment the access count for the URL in Redis
        redis_client.incr(f"count:{url}")
        
        # Check if the page is already cached in TTLCache
        if url in cache:
            print("Cache hit")
            return cache[url]
        
        # If not cached, call the function to get the page and cache the result
        print("Cache miss")
        result = func(url)
        cache[url] = result
        return result
    
    return wrapper

@cache_page
def get_page(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text
