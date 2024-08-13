#!/usr/bin/env python3
"""14. Top students"""
from pymongo import MongoClient


def top_students(mongo_collection):
    """A  Python function that returns all students sorted by average score"""
    pipeline = [
        {"$unwind": "$topics"},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "total_score": {"$sum": "$topics.score"},
            "total_topics": {"$sum": 1}
        }},
        {"$addFields": {
            "averageScore": {"$divide": ["$total_score", "$total_topics"]}
        }},
        {"$sort": {"averageScore": -1}}
    ]

    top_students = list(mongo_collection.aggregate(pipeline))
    return top_students
