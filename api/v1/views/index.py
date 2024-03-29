#!/usr/bin/python3
''''Index module create variable app_views which is instance of Blueprint'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    'return a JSON status representation'
    return jsonify({"status": "OK"})
