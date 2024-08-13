#!/usr/bin/env python3
"""9. Insert a document in Python"""


def insert_school(mongo_collection, **kwargs):
    """A Python function that inserts a new document in a collection based on kwargs"""
    result = mongo_collection.insert_one(kwargs)
    if result.inserted_id:
        return result.inserted_id
    else:
        return None
