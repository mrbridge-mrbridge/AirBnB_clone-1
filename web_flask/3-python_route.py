#!/usr/bin/python3
"""starts a Flask application"""


from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """displays 'Hello HBNB'"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """displays 'HBNB'"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """displays 'C <text>'"""
    txt = text.split('-')
    return 'C {}'.format(txt)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
