#!/usr/bin/python3
"""City view"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Retrieves list of all City objects of a State"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a City object"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    storage.delete(city)
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a City object"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    json = request.get_json()
    if not json:
        abort(400, 'Not a JSON')
    if 'name' not in json:
        abort(400, 'Missing name')
    json['state_id'] = state_id
    city = City(**json)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a City object"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    json = request.get_json()
    if not json:
        abort(400, 'Not a JSON')
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in json.items():
        if key not in ignore:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
