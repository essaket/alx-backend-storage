#!/usr/bin/env python3
"""5. Implementing an expiring web cache and tracker"""
import requests
import redis
redise = redis.Redis()


def get_page(url: str) -> str:
    """A fucntion that Get the HTML content of a particular URL and returns it"""
    redise.incr(f"count:{url}")

    cached = redise.get(url)
    if cached:
        return cached.decode('utf-8')

    html_content = requests.get(url).text
    redise.setex(url, 10, html_content)

    return html_content
