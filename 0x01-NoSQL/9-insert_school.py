#!/usr/bin/env python3
"""9. Insert a document in Python"""


def insert_school(mongo_collection, **kwargs):
    """A Python function that inserts a new document in a collection based on kwargs"""
    return result.mongo_collection.insert_one(kwargs).inserted_id
