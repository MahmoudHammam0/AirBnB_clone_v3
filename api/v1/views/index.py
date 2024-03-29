#!/usr/bin/python3
''''Index module create variable app_views which is instance of Blueprint'''
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    'return a JSON status representation'
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats_count():
    """ retrieves the number of each objects by type """
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
