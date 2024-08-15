#!/usr/bin/env python3
"""5. Implementing an expiring web cache and tracker"""
import requests
import redis

r = redis.Redis()


def get_page(url: str) -> str:
    """Get the HTML content of a particular URL and returns it"""
    r.incr(f"count:{url}")

    cached = r.get(url)
    if cached:
        return cached.decode('utf-8')

    html_content = requests.get(url).text

    r.setex(url, 10, html_content)

    return html_content
