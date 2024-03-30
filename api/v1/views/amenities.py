#!/usr/bin/python3
'''create view for Amenity objects that handles default RESTFul API actions'''
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    '''Retrieves the list of all Amenity objects'''
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    '''Retrieves a Amenity object by id'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    '''Deletes a Amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        for key, value in storage.all(Amenity).items():
            if value == amenity:
                storage.delete(amenity)
                storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_Amenity():
    'Creates an Amenity'
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")
    if data is None:
        abort(400, description="Not a JSON")
    if "name" not in request.json:
        abort(400, description="Missing name")
    new_amenity = Amenity(name="{}".format(request.get_json()['name']))
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    'Updates an Amenity object'
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
