#!/usr/bin/python3
'HBNB module'
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    'Hello HBNB!'
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    'HBNB home'
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def C(text):
    'C + text'
    text = text.replace('_', ' ')
    return f'C {text}'


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    'python + text'
    text = text.replace('_', ' ')
    return f'Python {text}'


@app.route('/number/<int:n>', strict_slashes=False)
def num(n):
    'only integers'
    return f'{n} is a number'


@app.route('/number_template/<int:n>', strict_slashes=False)
def temp_num(n):
    'display template only if n was int'
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
