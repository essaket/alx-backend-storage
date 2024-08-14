#!/usr/bin/env python3
"""5. Implementing an expiring web cache and tracker"""
import requests
import redis

r = redis.Redis()


def get_page(url: str) -> str:
    """A fucntion that Get the HTML content of a particular URL
       and returns it"""
    # Increment the access count for the URL in Redis
    r.incr(f"count:{url}")

    # Check if the URL is cached in Redis
    cached = r.get(url)
    if cached:
        # If cached, return the cached content
        return cached.decode('utf-8')

    # If not cached, fetch the HTML content from the URL
    html_content = requests.get(url).text

    # Cache the HTML content in Redis with a 10-second expiration time
    r.setex(url, 10, html_content)

    # Return the fetched HTML content
    return html_content
