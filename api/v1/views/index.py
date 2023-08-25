#!/usr/bin/python3
"""Status route on app_views"""
from api.v1.views import app_views
from models import storage


@app_views.route('/stats')
def stats():
    stats = {}
    classes = {"Amenity": "amenities",
               "City": "cities",
               "Place": "places",
               "Review": "reviews",
               "State": "states",
               "User": "users"}

    for cls in classes:
        stats[classes[cls]] = storage.count(cls)

    return stats
