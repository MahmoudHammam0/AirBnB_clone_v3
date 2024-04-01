#!/usr/bin/python3
'''
API app module that return the status of your API
'''
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def tear_down(exception):
    '''close the storage at the end of each request'''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ returns a JSON-formatted 404 status code response """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=host, port=int(port), threaded=True, debug=True)
