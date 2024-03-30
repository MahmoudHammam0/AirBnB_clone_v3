#!/usr/bin/python3
""" Review API Blueprint """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """ returns a list of all the reviews for a specified place """
    place = storage.get(Place, city_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ returns the review with the specified id """
    retrieved_review = storage.get(Review, review_id)
    if retrieved_review:
        return jsonify(retrieved_review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ deletes a review with the sepcified id """
    retrieved_review = storage.get(Review, review_id)
    if retrieved_review:
        storage.delete(retrieved_review)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ creates a new review """
    try:
        review_dict = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    review_dict = request.get_json()

    if not review_dict:
        abort(400, "Not a JSON")

    if "user_id" not in review_dict.keys():
        abort(400, "Missing user_id")

    user_id = review_dict['user_id']

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if "text" not in review_dict.keys():
        abort(400, "Missing text")

    new_review = Review(**review_dict)
    setattr(new_review, 'place_id', place_id)
    storage.new(new_review)
    storage.save()

    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ updates a review """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    try:
        review_dict = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    review_dict = request.get_json()

    if not review_dict:
        abort(400, "Not a JSON")

    for key, value in review_dict.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)

    storage.save()

    return make_response(jsonify(review.to_dict()), 200)
