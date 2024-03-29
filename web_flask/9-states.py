#!/usr/bin/python3
'List of Cities module'
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def list_states(id=None):
    'display list cities by states'
    states = storage.all(State).values()
    cities = storage.all(City).values()
    ids = []
    for state in states:
        ids.append(state.id)
    if id in ids:
        x = 'found'
    else:
        x = 'not found'
    return render_template('9-states.html', states=states,
                           cities=cities, id=id, x=x)


@app.teardown_appcontext
def app_teardown(exception):
    'close sql alchemy session after each request'
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
