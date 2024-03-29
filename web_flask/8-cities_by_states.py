#!/usr/bin/python3
'List of Cities module'
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def list_states():
    'display list cities by states'
    states = storage.all(State).values()
    cities = storage.all(City).values()
    return render_template('8-cities_by_states.html', states=states,
                           cities=cities)


@app.teardown_appcontext
def app_teardown(exception):
    'close sql alchemy session after each request'
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
