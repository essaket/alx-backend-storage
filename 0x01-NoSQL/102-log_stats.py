#!/usr/bin/env python3
"""15. Log stats - new version"""


def nginx_log_stats(mongo_collection):
    """Displays stats about Nginx logs from a MongoDB collection"""
    total_logs = mongo_collection.count_documents({})

    method_counts = {}
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = mongo_collection.count_documents({"method": method})
        method_counts[method] = count

    status_checks = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})

    pipeline_ips = [
        {"$group": {
            "_id": "$ip",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    top_ips = list(mongo_collection.aggregate(pipeline_ips))

    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_checks} status check")

    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    nginx_log_stats(collection)
