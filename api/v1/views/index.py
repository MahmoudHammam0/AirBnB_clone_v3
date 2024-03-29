#!/usr/bin/python3
''''Index module create variable app_views which is instance of Blueprint'''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


@app_views.route('/status')
def status():
    'return a JSON status representation'
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats_count():
    """ retrieves the number of each objects by type """
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    }
    return jsonify(stats)
