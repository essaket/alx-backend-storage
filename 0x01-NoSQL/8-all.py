#!/usr/bin/env python3
"""8. List all documents in Python"""


def list_all(mongo_collection):
    """A Python function that lists all documents in a collection"""
    return [result for result in mongo_collection.find()]
