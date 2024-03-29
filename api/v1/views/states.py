#!/usr/bin/python3
""" State API Blueprint """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.state import State
from models import storage
import json


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ returns the state with the specified id """
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ returns the state with the specified id """
    retrieved_state = storage.get(State, state_id)
    if retrieved_state:
        return jsonify(retrieved_state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ deletes a state with the sepcified id """
    retrieved_state = storage.get(State, state_id)
    if retrieved_state:
        storage.delete(retrieved_state)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """ creates a new state """
    try:
        state_dict = json.loads(request.data)
    except json.JSONDecodeError:
        abort(400, "Not a JSON")

    state_dict = request.get_json()

    if not state_dict:
        abort(400, "Not a JSON")

    if "name" not in state_dict.keys():
        abort(400, "Missing name")

    new_state = State(**state_dict)
    storage.new(new_state)
    storage.save()

    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updates a state """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    try:
        state_dict = json.loads(request.data)
    except json.JSONDecodeError:
        abort(400, "Not a JSON")

    state_dict = request.get_json()

    if not state_dict:
        abort(400, "Not a JSON")

    for key, value in state_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    storage.save()

    return make_response(jsonify(state.to_dict()), 200)
