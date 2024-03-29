#!/usr/bin/python3
'Hello Flask! module'
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    'Hello HBNB!'
    return 'Hello HBNB!'


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
