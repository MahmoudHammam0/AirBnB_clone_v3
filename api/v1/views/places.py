#!/usr/bin/python3
""" Place API Blueprint """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.place import Place
from models.city import City
from models.state import State
from models.user import User
from models.amenity import Amenity
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """ returns a list of all the places in a specified city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ returns the place with the specified id """
    retrieved_place = storage.get(Place, place_id)
    if retrieved_place:
        return jsonify(retrieved_place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ deletes a place with the sepcified id """
    retrieved_place = storage.get(Place, place_id)
    if retrieved_place:
        storage.delete(retrieved_place)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ creates a new place """
    try:
        place_dict = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    place_dict = request.get_json()

    if not place_dict:
        abort(400, "Not a JSON")

    if "user_id" not in place_dict.keys():
        abort(400, "Missing user_id")

    user_id = place_dict['user_id']

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if "name" not in place_dict.keys():
        abort(400, "Missing name")

    new_place = Place(**place_dict)
    setattr(new_place, 'city_id', city_id)
    storage.new(new_place)
    storage.save()

    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ updates a place """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    try:
        place_dict = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    place_dict = request.get_json()

    if not place_dict:
        abort(400, "Not a JSON")

    for key, value in place_dict.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()

    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def place_search():
    'Retrieves all Place objects depending of the JSON in the body of request'
    try:
        re_body = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    body_dict = request.get_json()
    if body_dict == {} or (body_dict['states'] == []
                         and body_dict['cities'] == []
                         and body_dict['amenities'] == []):
        places = storage.all(Place).values()
        places_list = []
        for place in places:
            places_list.append(place.to_dict())
        return jsonify(places_list)
    
    res = []
    for state_id in body_dict["states"]:
        state = storage.get(State, state_id)
        for city in state.cities:
            if city.id in body_dict["cities"]:
                continue
            for place in city.places:
                res.append(place)
    if body_dict['cities']:
        for city_id in body_dict['cities']:
            city = storage.get(City, city_id)
            for place in city.places:
                res.append(place)
    if body_dict['amenities']:
        amenities = []
        for amenity_id in body_dict['amenities']:
            amenity = storage.get(Amenity, amenity_id)
            amenities.append(amenity)
        for place in res:
            if place.amenities != amenities:
                res.remove(place)
    json_res = []
    for place in res:
        json_res.append(place.to_dict())
    print(len(json_res))
    return jsonify(json_res)
