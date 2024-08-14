#!/usr/bin/env python3
""" task 5"""
from datetime import datetime, timedelta
from requests import get

# Define a cache dictionary with expiration times
cache = {}


def get_page(url: str) -> str:
  """
  Fetches the HTML content of a URL with caching and tracking.

  Args:
      url: The URL to fetch.

  Returns:
      The HTML content of the URL.
  """

  # Build the cache key with a prefix for "count"
  count_key = f"count:{url}"
  cache_key = f"url:{url}"

  # Check if the URL is already in cache and hasn't expired
  now = datetime.utcnow()
  if cache_key in cache and cache[cache_key]["expire"] > now:
    # Update access count if cached
    cache[count_key]["count"] += 1
    return cache[cache_key]["content"]

  # Not cached or expired, fetch from the web
  response = get(url)
  response.raise_for_status()  # Raise error for non-2xx status codes

  # Update access count and store in cache with expiration
  cache[count_key] = {"count": 1}
  cache[cache_key] = {
      "content": response.text,
      "expire": now + timedelta(seconds=10),
  }

  return response.text


# Bonus: Decorator for caching functionality
def cache_and_track(func):
  """
  Decorator to cache and track function calls.

  Args:
      func: The function to decorate.

  Returns:
      A decorated function with caching and tracking.
  """

  def wrapper(url):
    # Call the original get_page function with caching
    content = get_page(url)
    return content

  return wrapper


# Example usage with decorator (uncomment to use)
# get_page = cache_and_track(get_page)

if __name__ == "__main__":
  # Example usage
  url = "http://slowwly.robertomurray.co.uk"
  content = get_page(url)
  print(f"Content fetched: {content[:100]}...")

  # Check access count (stored in separate key)
  count_key = f"count:{url}"
  if count_key in cache:
    print(f"URL '{url}' accessed {cache[count_key]['count']} times.")
  else:
    print(f"No access count available for '{url}'.")
