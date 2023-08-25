#!/usr/bin/python3
'''Contains the index view for the API.'''
from flask import jsonify
from api.v1.views import app_views
from models import storage

# Define a route to check the status of the API
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns JSON """
    return jsonify(status="OK")

# Define a route to get statistics about the objects
@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stat():
    """ Returns JSON with object counts """
    # Get the counts using the storage.count() method
    amenities_count = storage.count('Amenity')
    cities_count = storage.count('City')
    places_count = storage.count('Place')
    reviews_count = storage.count('Review')
    states_count = storage.count('State')
    users_count = storage.count('User')

    # Create a JSON response with the counts
    counts = {
        "amenities": amenities_count,
        "cities": cities_count,
        "places": places_count,
        "reviews": reviews_count,
        "states": states_count,
        "users": users_count
    }
    
    return jsonify(counts)
