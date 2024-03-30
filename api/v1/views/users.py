#!/usr/bin/python3
'''create view for User objects that handles default RESTFul API actions'''
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    '''Retrieves the list of all User objects'''
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    '''Retrieves a User object by id'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''Deletes a User object'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        for key, value in storage.all(User).items():
            if value == user:
                storage.delete(user)
                storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    'Creates a User'
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")
    if data is None:
        abort(400, description="Not a JSON")
    if "email" not in request.json:
        abort(400, description="Missing email")
    if "password" not in request.json:
        abort(400, description="Missing password")
    new_user = User()
    for key, value in request.get_json().items():
        setattr(new_user, key, value)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    'Updates a User object'
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
