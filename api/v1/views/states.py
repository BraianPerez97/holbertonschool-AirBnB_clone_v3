#!/usr/bin/python3
"""State view"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = [state.to_dict() for state in storage.all('State').values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    storage.delete(state)
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a State"""
    json = request.get_json()
    if not json:
        abort(400, 'Not a JSON')
    if 'name' not in json:
        abort(400, 'Missing name')
    state = State(**json)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    json = request.get_json()
    if not json:
        abort(400, 'Not a JSON')
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in json.items():
        if key not in ignore:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
