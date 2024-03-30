#!/usr/bin/python3
""" Place-Amenity API Blueprint """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.place import Place
from models.amenity import Amenity
from models import storage
import os

storage_type = os.getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """ returns a list of all amenities linked to a place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if storage_type == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = []
        for amenity_id in place.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenities.append(amenity.to_dict())

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_place(place_id, amenity_id):
    """ deletes a link between a place and an amenity
        removes a certain amenity from a certain place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    if storage_type == 'db':
        if amenity not in place.amenities:
            abort(404)
        else:
            place.amenities.remove(amenity)
            amenity.delete()
    else:
        if amenity_id in place.amenity_ids:
            place.amenity_ids.remove(amenity_id)
        else:
            abort(404)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """ links an amenity to a place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage_type == 'db':
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
