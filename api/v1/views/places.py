#!/usr/bin/python3
'''Contains the places view for the API.'''
from flask import abort, jsonify, make_response, request
import requests
from api.v1.views import app_views
from api.v1.views.amenities import amenities
from api.v1.views.places_amenities import place_amenities
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
import json
from os import getenv
places_bp = Blueprint('places', __name__)

@places_bp.route('/api/v1/cities/<int:city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    city = City.query.get(city_id)
    if not city:
        return jsonify({'error': 'City not found'}), 404

    places = Place.query.filter_by(city_id=city_id).all()
    return jsonify([place.to_dict() for place in places]), 200

@places_bp.route('/api/v1/places/<int:place_id>', methods=['GET'])
def get_place(place_id):
    place = Place.query.get(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    return jsonify(place.to_dict()), 200

@places_bp.route('/api/v1/places/<int:place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = Place.query.get(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    db.session.delete(place)
    db.session.commit()

    return jsonify({}), 200

@places_bp.route('/api/v1/cities/<int:city_id>/places', methods=['POST'])
def create_place(city_id):
    city = City.query.get(city_id)
    if not city:
        return jsonify({'error': 'City not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in data:
        return jsonify({'error': 'Missing user_id'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400

    user_id = data['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    place = Place(name=data['name'], city_id=city_id, user_id=user_id)
    db.session.add(place)
    db.session.commit()

    return jsonify(place.to_dict()), 201

@places_bp.route('/api/v1/places/<int:place_id>', methods=['PUT'])
def update_place(place_id):
    place = Place.query.get(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)

    db.session.commit()

    return jsonify(place.to_dict()), 200
